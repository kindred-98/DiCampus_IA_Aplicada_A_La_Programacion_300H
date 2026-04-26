"""
MVP EdTech NLP assistant in a single Python file.

Capabilities:
- Extract text from PDF notes
- Chunk and index content with embeddings
- Summarize notes
- Answer questions with simple RAG
- Detect likely knowledge gaps
- Suggest personalized exercises

Requirements:
- Python 3.10+
- pypdf
- OPENAI_API_KEY environment variable

This version avoids external SDK dependencies and uses direct HTTP calls
to keep the file portable for class delivery.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "No PDF reader library found. Install 'pypdf' or 'PyPDF2' in the Python "
            "environment you are using to run this script."
        ) from exc


API_BASE_URL = "https://api.openai.com/v1"
DEFAULT_CHAT_MODEL = "gpt-4o-mini"
DEFAULT_EMBED_MODEL = "text-embedding-3-small"


def safe_json_loads(raw_text: str) -> dict[str, Any]:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON returned by the model: {raw_text}") from exc


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    a = np.array(vec_a, dtype=float)
    b = np.array(vec_b, dtype=float)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


class OpenAIHttpClient:
    def __init__(
        self,
        api_key: str | None = None,
        chat_model: str = DEFAULT_CHAT_MODEL,
        embedding_model: str = DEFAULT_EMBED_MODEL,
        timeout_seconds: int = 60,
        max_retries: int = 3,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

        self.chat_model = chat_model
        self.embedding_model = embedding_model
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{API_BASE_URL}/{endpoint}"
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")

        for attempt in range(1, self.max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                response_body = exc.read().decode("utf-8", errors="replace")
                status_code = exc.code
                if status_code in (429, 500, 502, 503, 504) and attempt < self.max_retries:
                    time.sleep(min(2 ** attempt, 8))
                    continue
                raise RuntimeError(
                    f"API request failed with status {status_code}: {response_body}"
                ) from exc
            except urllib.error.URLError as exc:
                if attempt < self.max_retries:
                    time.sleep(min(2 ** attempt, 8))
                    continue
                raise RuntimeError(f"Network error calling API: {exc}") from exc

        raise RuntimeError("Request failed after retries.")

    def create_embedding(self, text: str) -> list[float]:
        payload = {
            "model": self.embedding_model,
            "input": text,
        }
        response = self._post("embeddings", payload)
        try:
            return response["data"][0]["embedding"]
        except (KeyError, IndexError) as exc:
            raise RuntimeError(f"Unexpected embedding response: {response}") from exc

    def chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
        max_output_tokens: int = 600,
        temperature: float = 0.1,
    ) -> dict[str, Any]:
        payload = {
            "model": self.chat_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_output_tokens,
            "response_format": {"type": "json_object"},
        }
        response = self._post("chat/completions", payload)
        try:
            content = response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise RuntimeError(f"Unexpected chat response: {response}") from exc
        return safe_json_loads(content)


class PdfIngestor:
    def extract_text(self, pdf_path: str | Path) -> str:
        reader = PdfReader(str(pdf_path))
        pages: list[str] = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        full_text = "\n".join(pages).strip()
        if not full_text:
            raise ValueError("No text could be extracted from the PDF.")
        return full_text


class TextPreprocessor:
    def clean(self, text: str) -> str:
        compact = " ".join(text.replace("\x00", " ").split())
        return compact.strip()

    def chunk(self, text: str, chunk_size: int = 1200, overlap: int = 150) -> list[str]:
        if chunk_size <= overlap:
            raise ValueError("chunk_size must be greater than overlap.")
        chunks: list[str] = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            if end >= len(text):
                break
            start = end - overlap
        return chunks


@dataclass
class DocumentChunk:
    chunk_id: int
    text: str
    embedding: list[float]


class EmbeddingIndex:
    def __init__(self, client: OpenAIHttpClient) -> None:
        self.client = client
        self.chunks: list[DocumentChunk] = []

    def build(self, chunks: Iterable[str]) -> None:
        self.chunks.clear()
        for idx, chunk_text in enumerate(chunks, start=1):
            embedding = self.client.create_embedding(chunk_text)
            self.chunks.append(DocumentChunk(idx, chunk_text, embedding))

    def search(self, query: str, top_k: int = 3) -> list[DocumentChunk]:
        query_embedding = self.client.create_embedding(query)
        scored = [
            (cosine_similarity(query_embedding, chunk.embedding), chunk)
            for chunk in self.chunks
        ]
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:top_k]]


class SummaryModule:
    SYSTEM_PROMPT = """
You are an academic assistant.
Summarize study material accurately and conservatively.
Return only valid JSON with:
- summary: array of exactly 5 bullet-style strings
- topics: array of important topics
- difficulty_level: one of ["basic", "intermediate", "advanced"]
Do not invent content that is not supported by the source.
""".strip()

    def __init__(self, client: OpenAIHttpClient) -> None:
        self.client = client

    def summarize(self, source_text: str) -> dict[str, Any]:
        return self.client.chat_json(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=f"Material de estudio:\n\n{source_text}",
            max_output_tokens=500,
            temperature=0.1,
        )


class QAModule:
    SYSTEM_PROMPT = """
You are a tutor assistant for students.
Answer only using the provided context.
Return only valid JSON with:
- answer: concise answer for the student
- confidence: number from 0 to 1
- cited_chunk_ids: array of chunk ids used
- insufficient_context: boolean
If the answer is not clearly supported by context, say so.
""".strip()

    def __init__(self, client: OpenAIHttpClient, index: EmbeddingIndex) -> None:
        self.client = client
        self.index = index

    def answer_question(self, question: str, top_k: int = 3) -> dict[str, Any]:
        chunks = self.index.search(question, top_k=top_k)
        context_blocks = []
        for chunk in chunks:
            context_blocks.append(f"[Chunk {chunk.chunk_id}]\n{chunk.text}")
        context_text = "\n\n".join(context_blocks)

        prompt = (
            f"Pregunta del estudiante:\n{question}\n\n"
            f"Contexto recuperado:\n{context_text}"
        )
        return self.client.chat_json(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=prompt,
            max_output_tokens=450,
            temperature=0.1,
        )


class KnowledgeGapModule:
    SYSTEM_PROMPT = """
You are an academic diagnostic assistant.
Detect probable knowledge gaps from study material, student questions, and past answers.
Return only valid JSON with:
- weak_topics: array of strings
- evidence: array of short explanations
- mastery_estimate: one of ["low", "medium", "high"]
- recommended_next_focus: string
Base the diagnosis on the provided evidence and do not invent missing signals.
""".strip()

    def __init__(self, client: OpenAIHttpClient, index: EmbeddingIndex) -> None:
        self.client = client
        self.index = index

    def detect_gaps(
        self,
        study_goals: list[str],
        student_questions: list[str],
        wrong_answers: list[str],
    ) -> dict[str, Any]:
        query = " ".join(study_goals + student_questions + wrong_answers).strip()
        support_chunks = self.index.search(query, top_k=4) if query else self.index.chunks[:4]
        context_text = "\n\n".join(
            f"[Chunk {chunk.chunk_id}]\n{chunk.text}" for chunk in support_chunks
        )
        prompt = (
            f"Objetivos del material:\n{json.dumps(study_goals, ensure_ascii=False)}\n\n"
            f"Preguntas del estudiante:\n{json.dumps(student_questions, ensure_ascii=False)}\n\n"
            f"Respuestas incorrectas o dudas:\n{json.dumps(wrong_answers, ensure_ascii=False)}\n\n"
            f"Contexto académico relevante:\n{context_text}"
        )
        return self.client.chat_json(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=prompt,
            max_output_tokens=500,
            temperature=0.1,
        )


class ExerciseRecommendationModule:
    SYSTEM_PROMPT = """
You are an academic coach.
Generate personalized exercises from detected weak topics.
Return only valid JSON with:
- exercises: array of objects with fields:
  - title
  - objective
  - difficulty
  - prompt
  - expected_skill
Keep exercises practical and aligned with the source material.
""".strip()

    def __init__(self, client: OpenAIHttpClient, index: EmbeddingIndex) -> None:
        self.client = client
        self.index = index

    def recommend(self, weak_topics: list[str], top_k: int = 3) -> dict[str, Any]:
        query = " ".join(weak_topics).strip()
        chunks = self.index.search(query, top_k=top_k) if query else self.index.chunks[:top_k]
        context_text = "\n\n".join(
            f"[Chunk {chunk.chunk_id}]\n{chunk.text}" for chunk in chunks
        )
        prompt = (
            f"Temas débiles detectados: {json.dumps(weak_topics, ensure_ascii=False)}\n\n"
            f"Material de apoyo:\n{context_text}"
        )
        return self.client.chat_json(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=prompt,
            max_output_tokens=650,
            temperature=0.3,
        )


class EdTechMVPApp:
    def __init__(self, client: OpenAIHttpClient) -> None:
        self.client = client
        self.ingestor = PdfIngestor()
        self.preprocessor = TextPreprocessor()
        self.index = EmbeddingIndex(client)
        self.summary_module = SummaryModule(client)
        self.qa_module = QAModule(client, self.index)
        self.gap_module = KnowledgeGapModule(client, self.index)
        self.exercise_module = ExerciseRecommendationModule(client, self.index)
        self.cached_summary: dict[str, Any] | None = None

    def load_pdf(self, pdf_path: str | Path) -> None:
        raw_text = self.ingestor.extract_text(pdf_path)
        clean_text = self.preprocessor.clean(raw_text)
        chunks = self.preprocessor.chunk(clean_text)
        self.index.build(chunks)
        self.cached_summary = self.summary_module.summarize(clean_text[:12000])

    def summarize_notes(self) -> dict[str, Any]:
        if not self.cached_summary:
            raise RuntimeError("No PDF loaded yet.")
        return self.cached_summary

    def answer_question(self, question: str) -> dict[str, Any]:
        return self.qa_module.answer_question(question)

    def detect_knowledge_gaps(
        self,
        study_goals: list[str],
        student_questions: list[str],
        wrong_answers: list[str],
    ) -> dict[str, Any]:
        return self.gap_module.detect_gaps(study_goals, student_questions, wrong_answers)

    def suggest_exercises(self, weak_topics: list[str]) -> dict[str, Any]:
        return self.exercise_module.recommend(weak_topics)


def print_json(title: str, payload: dict[str, Any]) -> None:
    print(f"\n=== {title} ===")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def demo(pdf_path: str) -> None:
    app = EdTechMVPApp(OpenAIHttpClient())
    app.load_pdf(pdf_path)

    summary = app.summarize_notes()
    print_json("SUMMARY", summary)

    qa_result = app.answer_question(
        "¿Cuál es la diferencia entre búsqueda semántica y búsqueda por palabras clave?"
    )
    print_json("QA", qa_result)

    gap_result = app.detect_knowledge_gaps(
        study_goals=[
            "entender embeddings",
            "entender RAG",
            "aplicar NLP en software real",
        ],
        student_questions=[
            "No entiendo por qué embeddings encuentra frases distintas.",
            "¿RAG es lo mismo que resumir un PDF?",
        ],
        wrong_answers=[
            "Los embeddings buscan palabras exactas.",
            "RAG solo sirve para traducir textos.",
        ],
    )
    print_json("KNOWLEDGE_GAPS", gap_result)

    weak_topics = gap_result.get("weak_topics", [])
    exercise_result = app.suggest_exercises(weak_topics)
    print_json("EXERCISE_RECOMMENDATIONS", exercise_result)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "Usage: python bloque5_mvp_edtech.py <pdf_path>\n"
            "Example: python bloque5_mvp_edtech.py apuntes.pdf"
        )
        return 1

    pdf_path = Path(argv[1])
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        return 1

    try:
        demo(str(pdf_path))
        return 0
    except Exception as exc:
        print(f"Application error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
