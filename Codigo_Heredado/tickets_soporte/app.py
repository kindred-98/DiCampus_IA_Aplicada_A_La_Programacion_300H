"""
SISTEMA DE ANÁLISIS DE TICKETS DE SOPORTE CON NLP
==================================================
Este es el código base completo y funcional.

OBJETIVOS DEL EJERCICIO:
1. Refactorizar este código en múltiples módulos
2. Crear una estructura de pipeline clara y modular
3. Implementar tests unitarios
4. Preparar el proyecto para GitHub
"""

import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple

# Cargar variables de entorno
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================
# MODELOS DE DATOS
# ============================================

class CategoriaTicket(Enum):
    """Enum para las categorías de tickets"""
    CUENTA = "cuenta"
    TECNICO = "tecnico"
    FACTURACION = "facturacion"
    PRODUCTO = "producto"
    OTRO = "otro"

class UrgenciaTicket(Enum):
    """Enum para los niveles de urgencia"""
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

class TicketAnalizado:
    """Representa un ticket después del análisis NLP"""
    
    def __init__(self, texto_original: str, categoria: CategoriaTicket, 
                 urgencia: UrgenciaTicket, intencion: str, 
                 accion_sugerida: str, entidades: Dict = None):
        self.texto_original = texto_original
        self.categoria = categoria
        self.urgencia = urgencia
        self.intencion = intencion
        self.accion_sugerida = accion_sugerida
        self.entidades = entidades or {}
        self.fecha_analisis = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convierte el ticket a diccionario para JSON"""
        return {
            "texto_original": self.texto_original[:100] + "..." if len(self.texto_original) > 100 else self.texto_original,
            "categoria": self.categoria.value if isinstance(self.categoria, Enum) else self.categoria,
            "urgencia": self.urgencia.value if isinstance(self.urgencia, Enum) else self.urgencia,
            "intencion": self.intencion,
            "accion_sugerida": self.accion_sugerida,
            "entidades": self.entidades,
            "fecha_analisis": self.fecha_analisis.isoformat()
        }

# ============================================
# PREPROCESAMIENTO
# ============================================

def preprocesar_texto(texto: str, max_caracteres: int = 10000) -> str:
    """
    Limpia y normaliza el texto antes del análisis
    
    Args:
        texto: Texto original del ticket
        max_caracteres: Longitud máxima permitida
    
    Returns:
        Texto preprocesado
    """
    # Eliminar HTML
    texto = re.sub(r'<[^>]+>', '', texto)
    
    # Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Eliminar caracteres de control
    texto = re.sub(r'[\x00-\x1f\x7f]', '', texto)
    
    # Truncar si es demasiado largo
    if len(texto) > max_caracteres:
        texto = texto[:max_caracteres] + "..."
    
    return texto

# ============================================
# PROMPT PARA LA IA
# ============================================

SYSTEM_PROMPT_CLASIFICACION = """
Eres un sistema de clasificación de tickets de soporte técnico.

Analiza el texto del usuario y devuelve ÚNICAMENTE un JSON con estos campos:
- categoria: una de ["cuenta", "tecnico", "facturacion", "producto", "otro"]
- urgencia: una de ["alta", "media", "baja"]
- intencion: descripción breve de qué quiere hacer el usuario
- accion_sugerida: qué debería hacer la aplicación (ej: "resetear contraseña", "escalar a tecnico", "reembolsar")
- entidades: objeto con información extraída como { "email": "...", "pedido_id": "...", "producto": "..." }

Reglas:
- Si el usuario menciona problemas de acceso/login/contraseña → categoria: "cuenta"
- Si menciona errores técnicos, bugs, la app no funciona → categoria: "tecnico"
- Si menciona pagos, facturas, reembolsos → categoria: "facturacion"
- Si menciona productos específicos, características → categoria: "producto"
- Urgencia alta si hay palabras como "urgente", "ya", "inmediatamente", "no funciona"
- No añadas texto fuera del JSON.
"""

# ============================================
# LLAMADA A LA API
# ============================================

def analizar_ticket_con_nlp(texto_usuario: str) -> Dict:
    """
    Analiza un ticket usando la API de OpenAI
    
    Args:
        texto_usuario: Texto del ticket a analizar
    
    Returns:
        Diccionario con el resultado del análisis
    """
    # Preprocesar texto
    texto_limpio = preprocesar_texto(texto_usuario)
    
    # Construir prompt
    mensajes = [
        {"role": "system", "content": SYSTEM_PROMPT_CLASIFICACION},
        {"role": "user", "content": texto_limpio}
    ]
    
    try:
        # Llamada a la API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensajes,
            temperature=0.0,
            max_tokens=300
        )
        
        # Parsear respuesta
        respuesta_texto = response.choices[0].message.content
        
        try:
            resultado = json.loads(respuesta_texto)
            
            # Validar campos requeridos
            campos_requeridos = ["categoria", "urgencia", "intencion", "accion_sugerida"]
            for campo in campos_requeridos:
                if campo not in resultado:
                    resultado[campo] = "desconocido"
            
            # Validar categoría
            categorias_validas = ["cuenta", "tecnico", "facturacion", "producto", "otro"]
            if resultado["categoria"] not in categorias_validas:
                resultado["categoria"] = "otro"
            
            # Validar urgencia
            urgencias_validas = ["alta", "media", "baja"]
            if resultado["urgencia"] not in urgencias_validas:
                resultado["urgencia"] = "media"
            
            return {
                "exito": True,
                "analisis": resultado,
                "tokens_usados": response.usage.total_tokens
            }
            
        except json.JSONDecodeError:
            return {
                "exito": False,
                "error": "La API no devolvió JSON válido",
                "respuesta_raw": respuesta_texto
            }
            
    except Exception as e:
        return {
            "exito": False,
            "error": str(e)
        }

# ============================================
# VALIDACIÓN Y TRANSFORMACIÓN
# ============================================

def transformar_a_ticket(texto_usuario: str, resultado_api: Dict) -> TicketAnalizado:
    """
    Transforma la respuesta de la API en un objeto TicketAnalizado
    
    Args:
        texto_usuario: Texto original del ticket
        resultado_api: Resultado de la API
    
    Returns:
        Objeto TicketAnalizado
    """
    analisis = resultado_api.get("analisis", {})
    
    # Mapear strings a Enums
    categoria_map = {
        "cuenta": CategoriaTicket.CUENTA,
        "tecnico": CategoriaTicket.TECNICO,
        "facturacion": CategoriaTicket.FACTURACION,
        "producto": CategoriaTicket.PRODUCTO,
        "otro": CategoriaTicket.OTRO
    }
    
    urgencia_map = {
        "alta": UrgenciaTicket.ALTA,
        "media": UrgenciaTicket.MEDIA,
        "baja": UrgenciaTicket.BAJA
    }
    
    categoria = categoria_map.get(analisis.get("categoria", "otro"), CategoriaTicket.OTRO)
    urgencia = urgencia_map.get(analisis.get("urgencia", "media"), UrgenciaTicket.MEDIA)
    
    return TicketAnalizado(
        texto_original=texto_usuario,
        categoria=categoria,
        urgencia=urgencia,
        intencion=analisis.get("intencion", "No especificada"),
        accion_sugerida=analisis.get("accion_sugerida", "Revisar manualmente"),
        entidades=analisis.get("entidades", {})
    )

# ============================================
# ACCIONES
# ============================================

def ejecutar_accion_segun_ticket(ticket: TicketAnalizado) -> None:
    """
    Ejecuta acciones basadas en el análisis del ticket
    
    Args:
        ticket: Ticket analizado
    """
    print("\n" + "=" * 60)
    print("⚡ ACCIONES A EJECUTAR")
    print("=" * 60)
    
    # Acciones según categoría y urgencia
    if ticket.categoria == CategoriaTicket.CUENTA:
        print("📌 CATEGORÍA: CUENTA")
        if ticket.urgencia == UrgenciaTicket.ALTA:
            print("   🔴 URGENCIA ALTA → Escalar a soporte inmediatamente")
            print("   📧 Enviar alerta al equipo de soporte")
            print("   💬 Mostrar al usuario: 'Un agente te contactará en menos de 5 minutos'")
        else:
            print("   🟡 URGENCIA MEDIA/BAJA → Enviar email con instrucciones automáticas")
            print("   📧 Enviar guía de recuperación de cuenta")
            
    elif ticket.categoria == CategoriaTicket.TECNICO:
        print("📌 CATEGORÍA: TÉCNICO")
        if ticket.urgencia == UrgenciaTicket.ALTA:
            print("   🔴 URGENCIA ALTA → Escalar a equipo técnico con prioridad máxima")
            print("   📊 Registrar incidencia en sistema de bugs")
        else:
            print("   🟡 URGENCIA MEDIA/BAJA → Sugerir artículos de la base de conocimiento")
            
    elif ticket.categoria == CategoriaTicket.FACTURACION:
        print("📌 CATEGORÍA: FACTURACIÓN")
        print("   💰 Derivar a departamento de facturación")
        print("   📧 Enviar email con instrucciones de pago/reembolso")
        
    elif ticket.categoria == CategoriaTicket.PRODUCTO:
        print("📌 CATEGORÍA: PRODUCTO")
        print("   📦 Registrar feedback de producto")
        print("   💬 Agradecer al usuario por su comentario")
        
    else:
        print("📌 CATEGORÍA: OTRO")
        print("   👤 Escalar a equipo general para revisión manual")
    
    print(f"\n🎯 INTENCIÓN DETECTADA: {ticket.intencion}")
    print(f"🔧 ACCIÓN SUGERIDA POR IA: {ticket.accion_sugerida}")
    
    if ticket.entidades:
        print(f"\n📋 ENTIDADES EXTRAÍDAS:")
        for key, value in ticket.entidades.items():
            print(f"   {key}: {value}")

# ============================================
# PIPELINE COMPLETO
# ============================================

def pipeline_procesamiento_ticket(texto_usuario: str) -> Optional[TicketAnalizado]:
    """
    Pipeline completo de procesamiento de tickets
    
    Args:
        texto_usuario: Texto del ticket a procesar
    
    Returns:
        TicketAnalizado o None si hay error
    """
    print("\n" + "=" * 70)
    print("🚀 PIPELINE DE PROCESAMIENTO NLP")
    print("=" * 70)
    
    # Paso 1: Preprocesamiento
    print("\n📥 PASO 1: PREPROCESAMIENTO")
    texto_limpio = preprocesar_texto(texto_usuario)
    print(f"   Texto original: {texto_usuario[:100]}...")
    print(f"   Texto limpio: {texto_limpio[:100]}...")
    
    # Paso 2: Análisis con IA
    print("\n🤖 PASO 2: ANÁLISIS CON IA")
    resultado = analizar_ticket_con_nlp(texto_usuario)
    
    if not resultado["exito"]:
        print(f"   ❌ Error: {resultado.get('error')}")
        return None
    
    print(f"   ✅ Análisis completado")
    print(f"   Tokens usados: {resultado['tokens_usados']}")
    
    # Paso 3: Transformación
    print("\n🔄 PASO 3: TRANSFORMACIÓN")
    ticket = transformar_a_ticket(texto_usuario, resultado)
    print(f"   Categoría: {ticket.categoria.value}")
    print(f"   Urgencia: {ticket.urgencia.value}")
    
    # Paso 4: Ejecutar acciones
    ejecutar_accion_segun_ticket(ticket)
    
    return ticket

# ============================================
# PROCESAMIENTO POR LOTES
# ============================================

def procesar_tickets_lote(tickets: List[str]) -> List[TicketAnalizado]:
    """
    Procesa múltiples tickets en lote
    
    Args:
        tickets: Lista de textos de tickets
    
    Returns:
        Lista de tickets analizados
    """
    resultados = []
    
    for i, ticket in enumerate(tickets, 1):
        print(f"\n📝 Procesando ticket {i}/{len(tickets)}")
        resultado = pipeline_procesamiento_ticket(ticket)
        if resultado:
            resultados.append(resultado)
    
    return resultados

# ============================================
# EXPORTAR RESULTADOS
# ============================================

def exportar_resultados_json(tickets: List[TicketAnalizado], archivo: str = "resultados.json") -> None:
    """
    Exporta los resultados a un archivo JSON
    
    Args:
        tickets: Lista de tickets analizados
        archivo: Nombre del archivo de salida
    """
    datos = [ticket.to_dict() for ticket in tickets]
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados exportados a {archivo}")

# ============================================
# EJEMPLOS DE USO
# ============================================

def ejecutar_ejemplos():
    """Ejecuta ejemplos de uso del sistema"""
    
    # Ejemplo 1: Ticket de cuenta urgente
    print("\n" + "🔹" * 35)
    print("EJEMPLO 1: TICKET DE CUENTA URGENTE")
    print("🔹" * 35)
    
    ticket1 = pipeline_procesamiento_ticket(
        "¡URGENTE! Llevo 3 días sin poder acceder a mi cuenta. "
        "Ya restablecí la contraseña dos veces y sigue sin funcionar. "
        "Mi email es usuario@ejemplo.com. Necesito solución YA."
    )
    
    # Ejemplo 2: Ticket técnico
    print("\n" + "\n" + "🔹" * 35)
    print("EJEMPLO 2: TICKET TÉCNICO")
    print("🔹" * 35)
    
    ticket2 = pipeline_procesamiento_ticket(
        "La aplicación se cierra sola cuando intento subir una imagen. "
        "Uso la versión 2.3.1 en Windows 11. El error dice 'MemoryError'."
    )
    
    # Ejemplo 3: Ticket de facturación
    print("\n" + "\n" + "🔹" * 35)
    print("EJEMPLO 3: TICKET DE FACTURACIÓN")
    print("🔹" * 35)
    
    ticket3 = pipeline_procesamiento_ticket(
        "Me cobraron dos veces la suscripción de este mes. "
        "El pedido es #12345 y el cargo apareció el 15 de marzo. "
        "Necesito que me devuelvan el dinero."
    )
    
    return [t for t in [ticket1, ticket2, ticket3] if t]

# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def main():
    """Función principal del programa"""
    
    print("🎯 SISTEMA DE ANÁLISIS DE TICKETS DE SOPORTE")
    print("=" * 50)
    
    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("1. Ejecutar ejemplos")
        print("2. Procesar ticket personalizado")
        print("3. Procesar múltiples tickets")
        print("4. Salir")
        
        opcion = input("\n👉 Elige una opción (1-4): ").strip()
        
        if opcion == "1":
            tickets = ejecutar_ejemplos()
            if tickets:
                exportar_resultados_json(tickets)
                
        elif opcion == "2":
            print("\n📝 Escribe tu ticket (o 'salir' para volver):")
            texto = input("> ").strip()
            if texto.lower() != 'salir':
                ticket = pipeline_procesamiento_ticket(texto)
                if ticket:
                    exportar_resultados_json([ticket], "ticket_personalizado.json")
                    
        elif opcion == "3":
            tickets_texto = []
            print("\n📝 Escribe varios tickets (línea vacía para terminar):")
            while True:
                linea = input(f"Ticket {len(tickets_texto)+1}: ").strip()
                if not linea:
                    break
                tickets_texto.append(linea)
            
            if tickets_texto:
                resultados = procesar_tickets_lote(tickets_texto)
                if resultados:
                    exportar_resultados_json(resultados, "tickets_lote.json")
                    
        elif opcion == "4":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    # Verificar que existe la API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: No se encontró OPENAI_API_KEY en el archivo .env")
        print("📝 Crea un archivo .env con: OPENAI_API_KEY=tu_api_key_aqui")
    else:
        main()