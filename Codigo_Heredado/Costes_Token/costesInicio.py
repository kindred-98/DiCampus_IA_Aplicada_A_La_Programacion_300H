# EJEMPLO: Calculadora de costes de API
import os
from openai import OpenAI
import tiktoken



class CalculadoraCostes:
    """Calcula costes estimados de uso de APIs de IA"""
    
    # Precios por millón de tokens (actualizados 2025)
    PRECIOS = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "claude-3-sonnet": {"input": 3.00, "output": 15.00},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    }
    
    def __init__(self, modelo: str = "gpt-4o-mini"):
        self.modelo = modelo
        self.precios = self.PRECIOS.get(modelo, {"input": 0.15, "output": 0.60})
    
    def calcular_costes(self, tokens_input: int, tokens_output: int) -> dict:
        """Calcula el coste de una llamada específica"""
        
        coste_input = (tokens_input / 1_000_000) * self.precios["input"]
        coste_output = (tokens_output / 1_000_000) * self.precios["output"]
        coste_total = coste_input + coste_output
        
        return {
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "coste_input_usd": coste_input,
            "coste_output_usd": coste_output,
            "coste_total_usd": coste_total,
            "coste_input_cent": coste_input * 100,
            "coste_output_cent": coste_output * 100,
            "coste_total_cent": coste_total * 100
        }
    
    def estimar_tokens(self, texto: str) -> int:
        """Estima tokens de un texto usando tiktoken"""
        encoding = tiktoken.encoding_for_model(self.modelo)
        return len(encoding.encode(texto))
    
    def proyectar_uso_mensual(self, llamadas_por_dia: int, tokens_input_por_llamada: int, 
                              tokens_output_por_llamada: int, dias_mes: int = 30) -> dict:
        """Proyecta costes mensuales basados en uso estimado"""
        
        llamadas_mensuales = llamadas_por_dia * dias_mes
        tokens_input_mensual = llamadas_mensuales * tokens_input_por_llamada
        tokens_output_mensual = llamadas_mensuales * tokens_output_por_llamada
        
        coste_input = (tokens_input_mensual / 1_000_000) * self.precios["input"]
        coste_output = (tokens_output_mensual / 1_000_000) * self.precios["output"]
        
        return {
            "llamadas_mensuales": llamadas_mensuales,
            "tokens_input_mensual": tokens_input_mensual,
            "tokens_output_mensual": tokens_output_mensual,
            "coste_input_usd": coste_input,
            "coste_output_usd": coste_output,
            "coste_total_usd": coste_input + coste_output,
            "coste_por_llamada": (coste_input + coste_output) / llamadas_mensuales
        }

# Crear calculadora para GPT-4o-mini
calc = CalculadoraCostes("gpt-4o-mini")

print("=" * 60)
print("CALCULADORA DE COSTES DE APIs DE IA")
print("=" * 60)

# Ejemplo 1: Coste de una conversación típica
print("\n📊 EJEMPLO 1: Conversación típica (pregunta + respuesta)")
conversacion = calc.calcular_costes(tokens_input=200, tokens_output=300)
print(f"Tokens input: {conversacion['tokens_input']} → ${conversacion['coste_input_usd']:.6f}")
print(f"Tokens output: {conversacion['tokens_output']} → ${conversacion['coste_output_usd']:.6f}")
print(f"Coste total: ${conversacion['coste_total_usd']:.6f} ({conversacion['coste_total_cent']:.4f} céntimos)")

# Ejemplo 2: Proyección mensual para un chatbot educativo
print("\n📊 EJEMPLO 2: Chatbot educativo (100 consultas/día)")
proyeccion = calc.proyectar_uso_mensual(
    llamadas_por_dia=100,
    tokens_input_por_llamada=200,
    tokens_output_por_llamada=300
)
print(f"Llamadas mensuales: {proyeccion['llamadas_mensuales']}")
print(f"Coste total mensual: ${proyeccion['coste_total_usd']:.2f}")
print(f"Coste por llamada: ${proyeccion['coste_por_llamada']:.6f}")

# Ejemplo 3: Proyección para una aplicación de resúmenes
print("\n📊 EJEMPLO 3: Aplicación de resúmenes (500 documentos/mes)")
calc_documentos = CalculadoraCostes("gpt-4o-mini")
proyeccion_docs = calc_documentos.proyectar_uso_mensual(
    llamadas_por_dia=16,  # 500 al mes ≈ 16 al día
    tokens_input_por_llamada=3000,  # Documento de 2000 palabras
    tokens_output_por_llamada=400
)
print(f"Documentos procesados: {proyeccion_docs['llamadas_mensuales']}")
print(f"Coste total mensual: ${proyeccion_docs['coste_total_usd']:.2f}")
print(f"Coste por documento: ${proyeccion_docs['coste_por_llamada']:.6f}")

# Ejemplo 4: Comparativa entre modelos para una misma tarea
print("\n📊 EJEMPLO 4: Comparativa de modelos para 10.000 llamadas/mes")
print("Tarea: Clasificación de tickets (150 input + 50 output)")

modelos_a_comparar = ["gpt-4o-mini", "gpt-4o", "gemini-1.5-flash"]

for modelo in modelos_a_comparar:
    calc_modelo = CalculadoraCostes(modelo)
    coste = calc_modelo.proyectar_uso_mensual(333, 150, 50)  # 333 llamadas/día ≈ 10.000/mes
    print(f"\n{modelo.upper()}:")
    print(f"  Coste mensual: ${coste['coste_total_usd']:.2f}")
    print(f"  Coste por llamada: ${coste['coste_por_llamada']:.6f}")

print("\n" + "=" * 60)
print("💡 RECOMENDACIONES PARA OPTIMIZAR COSTES")
print("=" * 60)
print("1. Usa GPT-4o-mini para el 80% de las tareas")
print("2. Establece límites de max_tokens según la tarea")
print("3. Cachea respuestas repetidas")
print("4. Monitoriza el uso diario con alertas")
print("5. Activa límites mensuales en la consola de OpenAI")