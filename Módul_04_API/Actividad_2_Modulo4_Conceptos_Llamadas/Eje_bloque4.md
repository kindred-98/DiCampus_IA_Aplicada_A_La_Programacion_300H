# BLOQUE 4 — Integrando APIs de IA con GitHub Actions y Modularización

## Conceptos de integración segura

| Pregunta de integración | Respuesta |
|---|---|
| **¿Dónde guardarías la API key de OpenAI en un repositorio de GitHub? ¿Por qué no en el código?** | Se guarda en **GitHub Secrets** (Settings → Secrets and variables → Actions). No debe estar en el código porque el código se sube a GitHub y sería visible para cualquiera. Las API keys son credenciales sensibles que nunca deben exponerse en el repositorio. |
| **¿Cómo pasarías la API key de GitHub Secrets a tu script Python en un workflow de GitHub Actions?** | Se pasa como variable de entorno usando `env: OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}` en el workflow, y en Python se accede con `os.getenv("OPENAI_API_KEY")`. |
| **Si modularizas tu app con un módulo separado para las llamadas a la API, ¿qué ventajas tiene?** | 1) **Separación de responsabilidades**: el código de IA está aislado del resto. 2) **Reutilización**: puedes importar el módulo en diferentes partes. 3) **Mantenimiento**: cambios solo en un lugar. 4) **Testing**: puedes probar las llamadas a la API de forma independiente. |
| **¿Qué problema puede ocurrir si tu pipeline ejecuta la llamada a la API en un bucle sin límite?** | Puede generar **miles de llamadas accidentales**, eliminando el crédito gratuito o generando facturas enormes. Es lo que se conoce como "bucle infinito" o "ataque de rate limiting". Se debe implementar control de límites (rate limiting) y monitoreo. |

---

## Ejemplo de Workflow con GitHub Actions

```yaml
name: Chatbot con IA

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Instalar dependencias
        run: pip install -r requirements.txt

      - name: Ejecutar tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: pytest tests/
```

---

## Ejemplo de módulo separado (Python)

**cliente_ia.py**

```python
from openai import OpenAI
import os

class ClienteIA:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def chatear(self, mensaje, system_prompt=None, temperature=0.7, max_tokens=500):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": mensaje})
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
```

**app.py**

```python
from cliente_ia import ClienteIA

cliente = ClienteIA()
respuesta = cliente.chatear("¿Qué es una API?")
print(respuesta)
```

---

## Diferencias clave: Python vs JavaScript

| Aspecto | Python | JavaScript |
|---|---|---|
| **Gestión de API key** | `os.getenv("OPENAI_API_KEY")` | `process.env.OPENAI_API_KEY` |
| **Modularización** | Módulos `.py` con `import` | Módulos `.js` con `import/export` |
| **GitHub Secrets** | Se pasa por `env` en workflow yaml | Igual que Python |
| **Ejecución en CI/CD** | Compatible con cualquier runner | Compatible con Node.js runners |

---

## Configuración segura recomendada

| Archivo | Propósito | ¿GitHub? |
|---|---|---|
| `.env` | Variables locales (no subir) | NO → añadir a `.gitignore` |
| `.env.example` | Template de variables | SÍ |
| `secrets.OPENAI_API_KEY` | API key real | SÍ (solo en Secrets) |
| `requirements.txt` | Dependencias | SÍ |
| `config.py` | Lógica de configuración | SÍ |