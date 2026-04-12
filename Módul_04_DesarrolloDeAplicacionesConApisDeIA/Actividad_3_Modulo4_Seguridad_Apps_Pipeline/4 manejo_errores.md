# 4 — Manejo de errores en llamadas a la API

## Código con manejo de errores robusto

```python
from openai import OpenAI
import os
import time
import json
from typing import Optional

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ErrorAPI(Exception):
    """Errores personalizados"""
    def __init__(self, tipo, mensaje):
        self.tipo = tipo
        super().__init__(mensaje)

def clasificar_ticket(ticket_texto: str, max_retries: int = 3) -> dict:
    """
    Clasifica un ticket con manejo robusto de errores.
    """
    system_prompt = """Clasifica el ticket en JSON:
{"categoría": "técnico|facturación|cuenta|otro", "prioridad": "alta|media|baja"}"""
    
    for intento in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": ticket_texto}
                ],
                temperature=0.0,
                max_tokens=100,
                timeout=30  # 30 segundos timeout
            )
            
            # Validar respuesta
            contenido = response.choices[0].message.content
            resultado = json.loads(contenido)
            
            # Validar campos requeridos
            if "categoría" not in resultado or "prioridad" not in resultado:
                raise ErrorAPI("formato", "Faltan campos requeridos")
            
            return resultado
            
        except json.JSONDecodeError as e:
            # Error de parsing - reintentar
            if intento == max_retries - 1:
                return {"categoría": "otro", "prioridad": "media", "error": "formato_inválido"}
            
        except Exception as e:
            error_str = str(e)
            
            if "429" in error_str or "rate_limit" in error_str:
                # Rate limit - wait con backoff exponencial
                wait_time = 2 ** intento
                time.sleep(wait_time)
                
            elif "401" in error_str:
                raise ErrorAPI("auth", f"API key inválida: {e}")
                
            elif "500" in error_str or "502" in error_str:
                # Error del servidor - reintentar
                if intento == max_retries - 1:
                    return {"categoría": "otro", "prioridad": "media", "error": "servidor_caído"}
                time.sleep(2)
                
            elif "timeout" in error_str.lower():
                # Timeout - reintentar
                if intento == max_retries - 1:
                    return {"categoría": "otro", "prioridad": "media", "error": "timeout"}
                    
            else:
                raise ErrorAPI("desconocido", str(e))
    
    return {"categoría": "otro", "prioridad": "media", "error": "max_retries"}
```

---

## Backoff exponencial

```python
import random

def retry_with_backoff(func, max_retries=5, base_delay=1):
    """Decorador para reintentar con backoff exponencial"""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise e
            
            if "429" in str(e) or "rate_limit" in str(e):
                delay = (base_delay * 2 ** i) + random.uniform(0, 1)
                print(f"Rate limit. Esperando {delay:.1f}s...")
                time.sleep(delay)
            else:
                raise e
```

---

## Validación de entradas

```python
def validar_ticket(ticket_texto: str) -> bool:
    """Valida que el ticket no sea demasiado largo"""
    MAX_CARACTERES = 5000
    
    if not ticket_texto or len(ticket_texto.strip()) == 0:
        return False, "El ticket está vacío"
    
    if len(ticket_texto) > MAX_CARACTERES:
        return False, f"El ticket excede {MAX_CARACTERES} caracteres"
    
    return True, "OK"

def validar_respuesta(respuesta: dict) -> bool:
    """Valida que la respuesta tenga el formato esperado"""
    campos_requeridos = ["categoría", "prioridad"]
    valores_válidos = {
        "categoría": ["técnico", "facturación", "cuenta", "otro"],
        "prioridad": ["alta", "media", "baja"]
    }
    
    for campo in campos_requeridos:
        if campo not in respuesta:
            return False, f"Falta campo: {campo}"
        
        if respuesta[campo] not in valores_válidos[campo]:
            return False, f"Valor inválido para {campo}"
    
    return True, "OK"
```

---

## Logging y monitoreo

```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clasificar_con_log(ticket_texto: str) -> dict:
    inicio = datetime.now()
    
    try:
        resultado = clasificar_ticket(ticket_texto)
        
        logger.info(f"Ticket procesado en {(datetime.now()-inicio).total_seconds()}s")
        logger.info(f"Categoría: {resultado.get('categoría')}, Prioridad: {resultado.get('prioridad')}")
        
        return resultado
        
    except ErrorAPI as e:
        logger.error(f"Error API - Tipo: {e.tipo}, Mensaje: {e}")
        return {"categoría": "otro", "prioridad": "media", "error": str(e)}
```

---

## Resumen: Mejores Practicas

| Práctica | Implementación |
|---|---|
| **Timeouts** | Sempre definir timeout en llamadas |
| **Reintentos** | Backoff exponencial con máximo 3-5 intentos |
| ** Rate limiting** | Controlar frecuencia de llamadas en código |
| **Validación** | Verificar input y output antes de procesar |
| **Logging** | Registrar errores, tiempos y resultados |
| **Respuestas por defecto** | Tener un fallback sitodo falla |
| **Monitoreo** | Dashboard de errores y latencia |