# ============================================
# CLASIFICACIÓN DE IMÁGENES CON OPENAI
# ============================================
import os
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clasificar_imagen(ruta_imagen: str, categorias: list) -> dict:
    """
    Clasifica una imagen en una de las categorías proporcionadas
    
    Args:
        ruta_imagen: Ruta al archivo de imagen
        categorias: Lista de categorías posibles (ej: ["gato", "perro", "pajaro"])
    
    Returns:
        Diccionario con clasificación y confianza
    """
    
    # Leer y codificar imagen
    with open(ruta_imagen, "rb") as f:
        imagen_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    # Construir prompt
    system_prompt = f"""
    Clasifica la imagen en UNA de estas categorías: {', '.join(categorias)}.
    
    Responde ÚNICAMENTE en formato JSON con:
    - categoria: la categoría seleccionada
    - confianza: número del 0 al 1
    - razones: breve explicación de por qué elegiste esa categoría
    
    Si no estás seguro o la imagen no coincide con ninguna categoría,
    responde con categoria: "desconocido"
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "¿Qué hay en esta imagen?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{imagen_base64}"}
                    }
                ]
            }
        ],
        max_tokens=200,
        temperature=0.0
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {
            "categoria": "error",
            "confianza": 0,
            "razones": "No se pudo parsear la respuesta",
            "raw": response.choices[0].message.content
        }

def clasificar_imagenes_lote(rutas_imagenes: list, categorias: list) -> list:
    """Clasifica múltiples imágenes y devuelve estadísticas"""
    
    resultados = []
    for ruta in rutas_imagenes:
        resultado = clasificar_imagen(ruta, categorias)
        resultados.append({
            "imagen": ruta,
            "resultado": resultado
        })
    
    # Estadísticas
    conteo = {}
    for r in resultados:
        cat = r["resultado"].get("categoria", "desconocido")
        conteo[cat] = conteo.get(cat, 0) + 1
    
    return {
        "resultados": resultados,
        "estadisticas": conteo,
        "total": len(resultados)
    }

# Ejemplo de uso (requiere tener imágenes)
# resultado = clasificar_imagen("mi_foto.jpg", ["gato", "perro", "pajaro", "desconocido"])
# print(json.dumps(resultado, indent=2, ensure_ascii=False))