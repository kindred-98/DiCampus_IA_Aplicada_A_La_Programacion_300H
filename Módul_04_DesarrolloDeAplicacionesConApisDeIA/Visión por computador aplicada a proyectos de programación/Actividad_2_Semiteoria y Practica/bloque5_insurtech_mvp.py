import argparse
import base64
import json
import mimetypes
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib import error, request

from PIL import Image, ImageFilter, ImageStat


OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MIN_WIDTH = 900
MIN_HEIGHT = 700
BLUR_THRESHOLD = 350.0
DARKNESS_THRESHOLD = 40.0


@dataclass
class LocalQualityReport:
    file_name: str
    mime_type: str
    width: int
    height: int
    bytes_size: int
    sharpness_score: float
    brightness_score: float
    photo_valid: bool
    invalid_reasons: list[str] = field(default_factory=list)


@dataclass
class DamageAssessment:
    description_damage: str
    severity: str
    plate_number: str
    photo_valid: bool
    invalid_reasons: list[str]
    possible_manipulation: bool
    confidence: float
    recommended_action: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="MVP de peritaje visual automatico para el Bloque 5."
    )
    parser.add_argument("image_path", help="Ruta de la imagen del vehiculo.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Modelo multimodal a usar. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--detail",
        choices=("low", "high", "auto"),
        default="auto",
        help="Nivel de detalle para la imagen en la API.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=2,
        help="Numero maximo de reintentos ante errores temporales.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Timeout de la llamada HTTP en segundos.",
    )
    return parser.parse_args()


def validate_image_path(image_path: str) -> Path:
    path = Path(image_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"No existe la imagen: {path}")
    if not path.is_file():
        raise ValueError(f"La ruta no apunta a un archivo: {path}")
    return path


def compute_sharpness(gray_image: Image.Image) -> float:
    edged = gray_image.filter(ImageFilter.FIND_EDGES)
    stat = ImageStat.Stat(edged)
    variance = stat.var[0] if stat.var else 0.0
    return float(variance)


def compute_brightness(gray_image: Image.Image) -> float:
    stat = ImageStat.Stat(gray_image)
    return float(stat.mean[0]) if stat.mean else 0.0


def build_local_quality_report(image_path: Path) -> LocalQualityReport:
    bytes_size = image_path.stat().st_size
    mime_type = mimetypes.guess_type(str(image_path))[0] or "application/octet-stream"
    invalid_reasons: list[str] = []

    with Image.open(image_path) as img:
        img.verify()

    with Image.open(image_path) as img:
        rgb = img.convert("RGB")
        gray = rgb.convert("L")
        width, height = rgb.size
        sharpness_score = compute_sharpness(gray)
        brightness_score = compute_brightness(gray)

    if bytes_size > MAX_IMAGE_BYTES:
        invalid_reasons.append("La imagen supera el tamano maximo recomendado de 8 MB.")
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        invalid_reasons.append("La resolucion es demasiado baja para peritaje fiable.")
    if sharpness_score < BLUR_THRESHOLD:
        invalid_reasons.append("La imagen parece borrosa o con poco detalle.")
    if brightness_score < DARKNESS_THRESHOLD:
        invalid_reasons.append("La imagen esta demasiado oscura.")
    if mime_type not in {"image/jpeg", "image/png", "image/webp"}:
        invalid_reasons.append("Formato no recomendado. Usa JPG, PNG o WEBP.")

    return LocalQualityReport(
        file_name=image_path.name,
        mime_type=mime_type,
        width=width,
        height=height,
        bytes_size=bytes_size,
        sharpness_score=round(sharpness_score, 2),
        brightness_score=round(brightness_score, 2),
        photo_valid=not invalid_reasons,
        invalid_reasons=invalid_reasons,
    )


def image_to_data_url(image_path: Path, mime_type: str) -> str:
    raw = image_path.read_bytes()
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def assessment_schema() -> dict[str, Any]:
    return {
        "name": "vehicle_damage_assessment",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "description_damage": {"type": "string"},
                "severity": {
                    "type": "string",
                    "enum": ["leve", "moderada", "grave", "no_determinable"],
                },
                "plate_number": {"type": "string"},
                "photo_valid": {"type": "boolean"},
                "invalid_reasons": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "possible_manipulation": {"type": "boolean"},
                "confidence": {"type": "number"},
                "recommended_action": {
                    "type": "string",
                    "enum": ["aprobar", "pedir_nueva_foto", "revision_manual"],
                },
            },
            "required": [
                "description_damage",
                "severity",
                "plate_number",
                "photo_valid",
                "invalid_reasons",
                "possible_manipulation",
                "confidence",
                "recommended_action",
            ],
            "additionalProperties": False,
        },
    }


def build_prompt(local_report: LocalQualityReport) -> str:
    report_json = json.dumps(asdict(local_report), ensure_ascii=True)
    return (
        "Analiza una foto de un vehiculo para un MVP de peritaje visual.\n"
        "Debes responder SOLO con JSON valido siguiendo exactamente el esquema.\n"
        "Objetivos:\n"
        "1. Describir los danos visibles de forma breve y objetiva.\n"
        "2. Clasificar la gravedad como leve, moderada, grave o no_determinable.\n"
        "3. Extraer la matricula solo si es legible. Si no, devuelve cadena vacia.\n"
        "4. Indicar si la foto es valida para peritaje.\n"
        "5. Marcar possible_manipulation=true solo si observas indicios visuales claros.\n"
        "6. Ajustar recommended_action asi:\n"
        "- aprobar: foto valida y analisis suficiente.\n"
        "- pedir_nueva_foto: foto borrosa, oscura, cortada o sin detalle suficiente.\n"
        "- revision_manual: si hay incertidumbre relevante, danos ambiguos o posible manipulacion.\n"
        "7. No inventes matriculas ni danos no visibles.\n"
        "8. Usa esta validacion local como contexto adicional, sin repetirla literalmente: "
        f"{report_json}"
    )


def build_request_payload(
    *,
    model: str,
    prompt: str,
    image_data_url: str,
    detail: str,
) -> dict[str, Any]:
    return {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": (
                    "Eres un analista de siniestros para un MVP de seguros. "
                    "Respondes siempre con JSON estricto y sin texto extra."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": image_data_url,
                        "detail": detail,
                    },
                ],
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "vehicle_damage_assessment",
                "strict": True,
                "schema": assessment_schema()["schema"],
            }
        },
    }


def extract_text_from_response(response_body: dict[str, Any]) -> str:
    if isinstance(response_body.get("output_text"), str) and response_body["output_text"].strip():
        return response_body["output_text"]

    output_items = response_body.get("output", [])
    for item in output_items:
        for content in item.get("content", []):
            text = content.get("text")
            if isinstance(text, str) and text.strip():
                return text

    raise ValueError("No se encontro texto de salida en la respuesta del modelo.")


def call_openai_responses_api(
    *,
    api_key: str,
    payload: dict[str, Any],
    timeout: int,
    max_retries: int,
) -> dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = json.dumps(payload).encode("utf-8")
    last_error: Exception | None = None

    for attempt in range(max_retries + 1):
        req = request.Request(
            OPENAI_API_URL,
            data=body,
            headers=headers,
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            temporary = exc.code in {408, 409, 429, 500, 502, 503, 504}
            if temporary and attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(
                f"Error HTTP {exc.code} al llamar a OpenAI: {error_body}"
            ) from exc
        except error.URLError as exc:
            last_error = exc
            if attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
            break

    raise RuntimeError(f"No se pudo completar la llamada a OpenAI: {last_error}")


def validate_model_output(data: dict[str, Any]) -> DamageAssessment:
    required = {
        "description_damage": str,
        "severity": str,
        "plate_number": str,
        "photo_valid": bool,
        "invalid_reasons": list,
        "possible_manipulation": bool,
        "confidence": (int, float),
        "recommended_action": str,
    }

    for key, expected_type in required.items():
        if key not in data:
            raise ValueError(f"Falta la clave obligatoria: {key}")
        if not isinstance(data[key], expected_type):
            raise ValueError(f"Tipo invalido para {key}: {type(data[key]).__name__}")

    if data["severity"] not in {"leve", "moderada", "grave", "no_determinable"}:
        raise ValueError("Valor no permitido en severity.")
    if data["recommended_action"] not in {
        "aprobar",
        "pedir_nueva_foto",
        "revision_manual",
    }:
        raise ValueError("Valor no permitido en recommended_action.")

    confidence = float(data["confidence"])
    confidence = max(0.0, min(1.0, confidence))

    invalid_reasons = [str(item) for item in data["invalid_reasons"]]

    return DamageAssessment(
        description_damage=data["description_damage"].strip(),
        severity=data["severity"],
        plate_number=data["plate_number"].strip(),
        photo_valid=bool(data["photo_valid"]),
        invalid_reasons=invalid_reasons,
        possible_manipulation=bool(data["possible_manipulation"]),
        confidence=round(confidence, 3),
        recommended_action=data["recommended_action"],
    )


def merge_reports(
    local_report: LocalQualityReport, remote_assessment: DamageAssessment
) -> dict[str, Any]:
    merged_invalid_reasons = list(dict.fromkeys(
        local_report.invalid_reasons + remote_assessment.invalid_reasons
    ))

    final_photo_valid = local_report.photo_valid and remote_assessment.photo_valid
    recommended_action = remote_assessment.recommended_action

    if not final_photo_valid and recommended_action == "aprobar":
        recommended_action = "pedir_nueva_foto"
    if remote_assessment.possible_manipulation and recommended_action != "revision_manual":
        recommended_action = "revision_manual"

    return {
        "input_file": str(local_report.file_name),
        "local_quality_report": asdict(local_report),
        "assessment": {
            "description_damage": remote_assessment.description_damage,
            "severity": remote_assessment.severity,
            "plate_number": remote_assessment.plate_number,
            "photo_valid": final_photo_valid,
            "invalid_reasons": merged_invalid_reasons,
            "possible_manipulation": remote_assessment.possible_manipulation,
            "confidence": remote_assessment.confidence,
            "recommended_action": recommended_action,
        },
    }


def main() -> int:
    args = parse_args()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "Falta OPENAI_API_KEY en las variables de entorno.",
            file=sys.stderr,
        )
        return 1

    try:
        image_path = validate_image_path(args.image_path)
        local_report = build_local_quality_report(image_path)
        image_data_url = image_to_data_url(image_path, local_report.mime_type)
        prompt = build_prompt(local_report)
        payload = build_request_payload(
            model=args.model,
            prompt=prompt,
            image_data_url=image_data_url,
            detail=args.detail,
        )
        raw_response = call_openai_responses_api(
            api_key=api_key,
            payload=payload,
            timeout=args.timeout,
            max_retries=args.max_retries,
        )
        output_text = extract_text_from_response(raw_response)
        parsed = json.loads(output_text)
        remote_assessment = validate_model_output(parsed)
        final_output = merge_reports(local_report, remote_assessment)
        print(json.dumps(final_output, indent=2, ensure_ascii=True))
        return 0
    except Exception as exc:
        error_output = {
            "error": type(exc).__name__,
            "message": str(exc),
        }
        print(json.dumps(error_output, indent=2, ensure_ascii=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
