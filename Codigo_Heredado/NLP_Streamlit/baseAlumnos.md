# Notas NLP — Guía Unificada

---

## 1. Corrección de errores — Instalación

Para instalar la librería de OpenAI en Python, ejecuta en tu terminal:

```bash
pip install openai
```

---

## 2. Creación del archivo `.env`

El archivo `.env` debe estar en la **raíz de tu proyecto**, al mismo nivel que tu script `.py`.

### ¿Qué poner en el `.env`?

Una vez que tengas tu clave, el archivo debe verse así:

```
OPENAI_API_KEY=sk-...
```

---

## 3. Cómo obtener tu `OPENAI_API_KEY`

1. **Acceder a la plataforma**
   Ve a [platform.openai.com](https://platform.openai.com) e inicia sesión con tu cuenta de OpenAI (la misma que usas para ChatGPT).

2. **Ir a la sección de API Keys**
   En el menú lateral izquierdo, busca el icono de llave o ve directamente a la sección **"API Keys"**.

3. **Crear una nueva clave (Secret Key)**
   - Haz clic en el botón **"+ Create new secret key"**.
   - Ponle un nombre identificativo (ejemplo: `"Clase NLP"`).
   - **IMPORTANTE:** En cuanto se genere, verás la clave comenzando por `sk-...`. Cópiala inmediatamente.

> ⚠️ **Advertencia:** Por seguridad, OpenAI no te permitirá volver a ver la clave completa una vez cierres esa ventana. Si la pierdes, tendrás que borrarla y crear una nueva.

---

## 4. Usar Ollama como alternativa local a OpenAI

Ollama emula la API de OpenAI, por lo que **solo tienes que cambiar dos líneas** de tu código original.

### Paso 1: Instalar Ollama

Descárgalo en [ollama.com](https://ollama.com) e instálalo.

### Paso 2: Ejecutar un modelo

Abre una terminal (PowerShell o CMD) y escribe:

```bash
ollama run llama3.2
```

### Modelos disponibles (ejemplos)

```python
model = "llama3.2"
model = "qwen2.5:0.5b"
model = "qwen2.5:0.8b"
```

---

## 5. Por qué cambia el mensaje en el análisis de sentimiento

### El problema

Los modelos de IA "conversan". Aunque les pidas JSON, a veces responden con texto adicional:

```
"Aquí tienes el JSON que me pediste: ```json ... ```"
```

### La consecuencia

Python intenta leer esa frase como si fuera un diccionario y lanza un error:

```
JSONDecodeError
```

### La solución

Usar `.replace()` para limpiar la respuesta y quedarnos solo con el contenido JSON, eliminando las etiquetas de Markdown:

```python
respuesta_limpia = respuesta.replace("```json", "").replace("```", "").strip()
```

---

## 6. Estructura de carpetas del proyecto

### Crear carpetas principales

```powershell
# Carpeta para logs (TXT con fechas)
New-Item -ItemType Directory -Path "logs" -Force

# Carpeta para resultados JSON
New-Item -ItemType Directory -Path "resultados_json" -Force

# Bloque 1 - Análisis
New-Item -ItemType Directory -Path "analisis" -Force

# Bloque 2 - Modularización
New-Item -ItemType Directory -Path "src" -Force
New-Item -ItemType Directory -Path "prompts" -Force

# Bloque 3 - Tests
New-Item -ItemType Directory -Path "tests" -Force

# Bloque 4 - CI/CD
New-Item -ItemType Directory -Path ".github/workflows" -Force

# Bloque 5 - Documentación
New-Item -ItemType Directory -Path "docs/api" -Force
New-Item -ItemType Directory -Path "docs/guides" -Force

# Bloque 6 - Interfaz
New-Item -ItemType Directory -Path "interface" -Force

# Bloques 7 y 8 - Reflexión
New-Item -ItemType Directory -Path "reflexiones" -Force
```

### Crear archivos iniciales (placeholders)

```powershell
# Logs con formato de fecha
New-Item -ItemType File -Path "logs/ejecucion_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt" -Force

# JSON de ejemplo
New-Item -ItemType File -Path "resultados_json/analisis_$(Get-Date -Format 'yyyyMMdd_HHmmss').json" -Force

# Archivos base por bloque
New-Item -ItemType File -Path "analisis/problemas_diseno.md" -Force
New-Item -ItemType File -Path "src/__init__.py" -Force
New-Item -ItemType File -Path "tests/__init__.py" -Force
New-Item -ItemType File -Path ".github/workflows/nlp_tests.yml" -Force
New-Item -ItemType File -Path "interface/__init__.py" -Force
New-Item -ItemType File -Path "reflexiones/Memoria_Final.md" -Force

# Archivos de prompts base
New-Item -ItemType File -Path "prompts/sentimiento.txt" -Force
New-Item -ItemType File -Path "prompts/entidades.txt" -Force
New-Item -ItemType File -Path "prompts/intencion.txt" -Force
New-Item -ItemType File -Path "prompts/resumen.txt" -Force
```

### Mover archivos existentes a su lugar

```powershell
# Guardar app_1.py como referencia heredada
Copy-Item "app_1.py" "heredado/app_original.py" -Force

# Mover documentación inicial al módulo de análisis
Copy-Item "docs/problemas_inicial.md" "analisis/problemas_inicial.md" -Force

# Crear README principal actualizado
New-Item -ItemType File -Path "README_PRINCIPAL.md" -Force
```

---

## 7. Estructura final del proyecto

```
📁 proyecto-nlp/
├── 📁 analisis/
│   ├── problemas_diseno.md
│   └── problemas_inicial.md
├── 📁 docs/
│   ├── 📁 api/
│   └── 📁 guides/
├── 📁 heredado/
│   └── app_original.py
├── 📁 interface/
│   └── __init__.py
├── 📁 logs/
├── 📁 prompts/
│   ├── sentimiento.txt
│   ├── entidades.txt
│   ├── intencion.txt
│   └── resumen.txt
├── 📁 reflexiones/
│   └── Memoria_Final.md
├── 📁 resultados_json/
├── 📁 src/
│   └── __init__.py
├── 📁 tests/
│   └── __init__.py
├── 📁 .github/
│   └── 📁 workflows/
│       └── nlp_tests.yml
├── .env
└── README_PRINCIPAL.md
```

## 8. Punto de partida: los dos archivos que tienes

| Archivo | Qué es | Para qué sirve |
|---------|--------|----------------|
| `heredado/Inicial.PY` | Versión original con OpenAI | **BLOQUE 1:** Analizar problemas de diseño |
| `heredado/app_1.py` | Versión adaptada a Ollama | **BLOQUE 2:** Punto de partida para modularizar |

> ⚠️ **Importante:** NO modifiques `Inicial.PY`. Trabajarás sobre `app_1.py` para crear las sucesivas versiones.

## 9. Flujo de trabajo por bloques

| Bloque | Tarea | Archivos implicados |
|--------|-------|---------------------|
| 1 | Análisis de código heredado | `analisis/problemas_diseno.md` |
| 2 | Modularización | `src/`, `prompts/`, `main.py` |
| 3 | Tests unitarios | `tests/` |
| 4 | CI/CD | `.github/workflows/nlp_tests.yml` |
| 5 | Documentación | `docs/`, `README.md` |
| 6 | Interfaz de empresa | `interface/` |
| 7-8 | Reflexión y Memoria Final | `reflexiones/Memoria_Final.md` |

## 10. Bloque 6 — Interfaz con Streamlit
 
El Bloque 6 consiste en crear una interfaz web para la demo NLP usando **Streamlit**.
 
### ¿Por qué Streamlit?
 
- No requiere conocimientos de HTML/CSS/JS.
- Permite construir apps web interactivas solo con Python.
- Ideal para prototipos y demos internas de empresa.
 
### Instalación
 
```bash
pip install streamlit
```
 
### Archivo a crear
 
Dentro de la carpeta `interface/`, crea el archivo `demo_app.py` con la lógica de la interfaz.
 
### Ejecución
 
```bash
streamlit run interface/demo_app.py
```
 
Streamlit abrirá automáticamente el navegador en `http://localhost:8501`.
 
---
 
## 11. El `.gitignore` — qué NO debe subirse al repositorio
 
> ⚠️ **Recuerda:** antes de hacer tu primer `git push`, crea el archivo `.gitignore` en la raíz del proyecto con el siguiente contenido mínimo:
 
```
.env
logs/
prompts/
resultados_json/
```
 
### ¿Por qué es importante?
 
| Carpeta / archivo | Motivo para excluirlo |
|---|---|
| `.env` | Contiene tu API Key — si la subes, cualquiera puede usarla y generarte costes |
| `logs/` | Archivos de traza locales, no relevantes para el repo |
| `prompts/` | Pueden contener instrucciones privadas o sensibles del negocio |
| `resultados_json/` | Datos generados en ejecución, pueden contener información confidencial |
 
### Cómo crearlo (PowerShell)
 
```powershell
New-Item -ItemType File -Path ".gitignore" -Force
```
 