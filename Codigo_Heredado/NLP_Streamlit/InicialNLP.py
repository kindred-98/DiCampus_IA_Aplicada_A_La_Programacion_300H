# ============================================
# DEMOSTRACIÓN DE CAPACIDADES NLP CON OPENAI
# ============================================
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def demostrar_capacidades_nlp(texto: str):
    """Demuestra múltiples capacidades NLP sobre un mismo texto"""
    
    print("=" * 70)
    print(f"📝 TEXTO ORIGINAL: {texto}")
    print("=" * 70)
    
    # 1. ANÁLISIS DE SENTIMIENTO
    print("\n🔵 1. ANÁLISIS DE SENTIMIENTO")
    print("-" * 50)
    
    response_sentimiento = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
            Analiza el sentimiento del texto. Responde ÚNICAMENTE en formato JSON con:
            - sentimiento: positivo, negativo o neutral
            - puntuacion: número del 0 al 1 (0=muy negativo, 1=muy positivo)
            - emociones: lista de emociones detectadas (alegría, tristeza, enojo, sorpresa, miedo, etc.)
            - confianza: número del 0 al 1
            """},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    try:
        sentimiento = json.loads(response_sentimiento.choices[0].message.content)
        print(f"   Sentimiento: {sentimiento.get('sentimiento')}")
        print(f"   Puntuación: {sentimiento.get('puntuacion')}")
        print(f"   Emociones: {sentimiento.get('emociones')}")
        print(f"   Confianza: {sentimiento.get('confianza')}")
    except:
        print(f"   {response_sentimiento.choices[0].message.content}")
    
    # 2. EXTRACCIÓN DE ENTIDADES (NER)
    print("\n🔵 2. EXTRACCIÓN DE ENTIDADES (NER)")
    print("-" * 50)
    
    response_ner = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
            Extrae todas las entidades del texto. Responde ÚNICAMENTE en formato JSON con:
            - personas: lista de nombres de personas
            - organizaciones: lista de empresas/instituciones
            - lugares: lista de ubicaciones
            - fechas: lista de fechas mencionadas
            - cantidades: lista de números y precios
            - otros: otros identificadores relevantes
            """},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    try:
        entidades = json.loads(response_ner.choices[0].message.content)
        for categoria, valores in entidades.items():
            if valores:
                print(f"   {categoria.capitalize()}: {valores}")
    except:
        print(f"   {response_ner.choices[0].message.content[:200]}...")
    
    # 3. DETECCIÓN DE INTENCIÓN
    print("\n🔵 3. DETECCIÓN DE INTENCIÓN")
    print("-" * 50)
    
    response_intencion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
            Detecta la intención del usuario. Responde ÚNICAMENTE en formato JSON con:
            - intencion_principal: una de [informacion, compra, soporte, queja, sugerencia, otro]
            - subcategoria: más específica (ej: "problema de login", "consulta de precio")
            - urgencia: alta, media, baja
            - accion_sugerida: qué debería hacer la aplicación
            """},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    try:
        intencion = json.loads(response_intencion.choices[0].message.content)
        print(f"   Intención principal: {intencion.get('intencion_principal')}")
        print(f"   Subcategoría: {intencion.get('subcategoria')}")
        print(f"   Urgencia: {intencion.get('urgencia')}")
        print(f"   Acción sugerida: {intencion.get('accion_sugerida')}")
    except:
        print(f"   {response_intencion.choices[0].message.content}")
    
    # 4. RESUMEN
    print("\n🔵 4. RESUMEN (3 niveles de detalle)")
    print("-" * 50)
    
    niveles = {
        "ultracorto": "Resume en UNA frase corta.",
        "medio": "Resume en 3 puntos clave.",
        "detallado": "Haz un resumen estructurado con introducción, desarrollo y conclusión."
    }
    
    for nivel, instruccion in niveles.items():
        response_resumen = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instruccion},
                {"role": "user", "content": texto}
            ],
            max_tokens=300 if nivel == "detallado" else 150
        )
        print(f"\n   [{nivel.upper()}]:")
        print(f"   {response_resumen.choices[0].message.content}")
    
    # 5. CLASIFICACIÓN MULTICATEGORÍA
    print("\n🔵 5. CLASIFICACIÓN MULTICATEGORÍA")
    print("-" * 50)
    
    response_clasificacion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
            Clasifica el texto en las siguientes categorías. Responde ÚNICAMENTE en formato JSON con:
            - tema: tecnico, facturacion, cuenta, producto, servicio_cliente, otro
            - tipo: pregunta, queja, sugerencia, informacion, solicitud
            - canal_adecuado: email, chat, telefono, automatico
            - prioridad: 1 (urgente) a 5 (sin urgencia)
            """},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    try:
        clasificacion = json.loads(response_clasificacion.choices[0].message.content)
        print(f"   Tema: {clasificacion.get('tema')}")
        print(f"   Tipo: {clasificacion.get('tipo')}")
        print(f"   Canal adecuado: {clasificacion.get('canal_adecuado')}")
        print(f"   Prioridad: {clasificacion.get('prioridad')}")
    except:
        print(f"   {response_clasificacion.choices[0].message.content}")

# Probar con diferentes tipos de texto
print("\n" + "=" * 70)
print("📊 DEMOSTRACIÓN DE CAPACIDADES NLP")
print("=" * 70)

# Texto de ejemplo 1: Queja de cliente
texto_queja = """
Llevo tres días intentando contactar con soporte y nadie responde. 
Mi pedido #12345 debería haber llegado el martes y aún no ha llegado. 
Estoy muy molesto porque necesito el producto para un proyecto urgente. 
Si no me solucionan hoy, cancelo el pedido y pido devolución.
"""

demostrar_capacidades_nlp(texto_queja)

# Texto de ejemplo 2: Consulta técnica
print("\n" + "\n" + "=" * 70)
texto_tecnico = """
¿Alguien sabe cómo configurar el timeout en una conexión HTTP con Python? 
Estoy usando la librería requests y a veces se queda colgado cuando el servidor tarda más de 10 segundos. 
He visto que hay un parámetro timeout en requests.get(), pero no sé si ponerlo en segundos o milisegundos.
"""

demostrar_capacidades_nlp(texto_tecnico)