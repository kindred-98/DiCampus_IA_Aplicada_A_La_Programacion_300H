# BLOQUE 5 — Pregunta de Síntesis

## Diseña una aplicación real con API de IA

> **Instrucción:** Diseña una aplicación real que use una API de IA. Indica: (1) qué problema resuelve, (2) qué proveedor y modelo elegirías, (3) qué parámetros clave usarías (temperature, max_tokens, system prompt), (4) cómo integrarías la API key de forma segura en un repositorio con pipeline CI/CD. Justifica cada decisión.

---

## Respuesta de ejemplo

### 1. Problema que resuelve

**Título:** Asistente de soporte técnico automatizado para tickets de helpdesk

**Descripción:** Un sistema que recibe tickets de soporte técnico, los clasifica automáticamente por categoría y prioridad, y genera una respuesta inicial personalizada para el usuario antes de que un agente humanoAtienda el caso.

**Beneficio:** Reduce el tiempo de respuesta inicial y permite a los agentes enfocarse en casos complejos.

### 2. Proveedor y modelo elegido

| Decisión | Justificación |
|---|---|
| **Proveedor: OpenAI** | Modelos GPT tienen el mejor rendimiento en comprensión de texto y clasificación. |
| **Modelo: GPT-4o-mini** | Coste muy bajo ($0.002/1K tokens). Suficiente para clasificación y generación de respuestas cortas. |
| **Alternativa: Claude 3 Haiku** | Si se necesita más rapidez y menor coste para tareas masivas. |

### 3. Parámetros clave

| Parámetro | Valor | Justificación |
|---|---|---|
| **temperature** | 0.2 | Respuestas consistentes y predecibles. Para clasificación queremos siempre el mismo resultado anteinputs similares. |
| **max_tokens** | 300 | Limitamos la longitud de la respuesta inicial. Suficiente para saludar y darnext steps. |
| **system prompt** | "Eres un asistente de soporte técnico. Clasifica el ticket en categoría [técnico/facturación/cuenta/otro] y prioridad [alta/media/baja]. Luego genera una respuesta inicial amigable de máximo 2 frases." | Define el rol, las categorías permitidas y el formato de salida. |
| **few-shot** | Incluir 2-3 ejemplos de clasificación en el prompt | Asegura que el modelo entienda exactamente las categorías. |

### 4. Integración segura con CI/CD

| Paso | Acción |
|---|---|
| **1. GitHub Secrets** | Guardar `OPENAI_API_KEY` en Settings → Secrets and variables → Actions |
| **2. Workflow yaml** | Pasar la key como variable de entorno: `env: OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}` |
| **3. Código** | Usar `os.getenv("OPENAI_API_KEY")` (nunca hardcodear) |
| **4. .gitignore** | Añadir `.env` para no subirlo nunca |
| **5. Rate limiting** | Añadir máximo de 100 llamadas/día en el pipeline |
| **6. Monitoreo** | Usar dashboard de OpenAI para контроль consumo |

---

## Proyecto estructura recomendada

```
mi-app-soporte/
├── .env                  # NO subir (en .gitignore)
├── .env.example          # Template
├── .gitignore
├── requirements.txt
├── config.py            # Configuración centralizada
├── cliente_ia.py       # Módulo de llamadas a la API
├── clasificador.py     # Lógica de clasificación
├── app.py              # Lógica principal
├── tests/
│   └── test_clasificador.py
├── .github/
│   └── workflows/
│       └── ci.yml
```

---

## Ejemplo de código (Python)

```python
# clasificador.py
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """Eres un asistente de soporte técnico.
Clasifica el ticket en categoría [técnico, facturación, cuenta, otro] y prioridad [alta, media, baja].
Responde SOLO en JSON con este formato:
{"categoría": "...", "prioridad": "...", "respuesta": "..."}"""

def clasificar_ticket(descripcion):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": descripcion}
        ],
        temperature=0.2,
        max_tokens=300
    )
    return json.loads(response.choices[0].message.content)
```

---

## Resumen de decisiones

| Aspecto | Decisión | Por qué |
|---|---|---|
| **Problema** | Clasificación automática de tickets | Optimiza el flujo de soporte |
| **Proveedor** | OpenAI | Mejor rendimiento en NLP |
| **Modelo** | GPT-4o-mini | Mejor equilibrio precio/calidad |
| **Temperature** | 0.2 | Consistencia en clasificación |
| **Max tokens** | 300 | Respuestas cortas iniciales |
| **Pipeline** | GitHub Actions + Secrets | Seguridad en CI/CD |