# 🖼️ VisionXComputadora — Clasificador de Imágenes Local con Ollama

> Herramienta educativa para clasificar imágenes usando modelos de visión por computador de forma **100% local, gratuita y privada** — sin API keys y sin enviar datos a internet.

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Objetivo de la práctica](#objetivo-de-la-práctica)
- [Características](#características)
- [Comparativa de Modelos](#comparativa-de-modelos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Actividad guiada](#actividad-guiada)
- [Entregables](#entregables)
- [Criterios de evaluación](#criterios-de-evaluación)
- [Evolución del Proyecto](#evolución-del-proyecto)
- [Tecnologías](#tecnologías)
- [Licencia](#licencia)

---

## 📌 Descripción

**VisionXComputadora** es un proyecto educativo que demuestra cómo pasar de una solución de clasificación de imágenes basada en la API de OpenAI (de pago y con dependencia de internet) a una solución completamente local usando [Ollama](https://ollama.com) y modelos de visión abiertos como `llava` o `moondream`.

El proyecto incluye todas las versiones intermedias del código, desde el código heredado hasta la interfaz final configurable mediante `config.py`.

---

## 🎯 Objetivo de la práctica

El objetivo de este ejercicio es que el alumno:

- Comprenda cómo funciona la clasificación de imágenes con IA.
- Compare distintos modelos de visión locales.
- Analice diferencias en resultados.
- Desarrolle o mejore una interfaz gráfica.
- Genere salidas estructuradas en distintos formatos.

---

## ✨ Características

- ✅ **Gratuito** — sin coste por uso ni tarjeta de crédito.
- ✅ **Privado** — las imágenes nunca salen de tu máquina.
- ✅ **Sin internet** — funciona completamente offline una vez instalado.
- ✅ **Multi-modelo** — compatible con `llava`, `moondream`, `llava:13b`, `bakllava`, `llava-phi3`.
- ✅ **Configurable** — cambia de modelo con una sola variable en `config.py`.
- ✅ **Robusto** — reintentos automáticos, timeouts, redimensionado de imágenes y manejo de errores.
- ✅ **Educativo** — pensado para comparar soluciones, estudiar el flujo y mejorar la interfaz.

---

## 📊 Comparativa de Modelos

| Modelo | Velocidad | Precisión | RAM Mínima | Mejor Para |
|---|---|---|---|---|
| `llava` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 8 GB | ✅ Recomendado — balance calidad/velocidad |
| `moondream` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 4 GB | CPU lento o RAM limitada |
| `llava:13b` | ⭐⭐ | ⭐⭐⭐⭐⭐ | 16 GB | Máxima precisión |
| `bakllava` | ⭐⭐⭐ | ⭐⭐⭐⭐ | 8 GB | Texto pequeño y detección de objetos |
| `llava-phi3` | ⭐⭐⭐⭐ | ⭐⭐⭐ | 6 GB | CPU moderno con RAM moderada |

---

## 🗂️ Estructura del Proyecto

```text
VisionXComputadora/
│
├── docs/
│   └── arreglar.md             # Historial de versiones y cambios desde el código heredado
│
├── src/
│   └── heredado/
│       └── clasificacionImagenes.py  # Código original con OpenAI (solo referencia)
│
├── img/                        # Imágenes de entrada para clasificar
├── interface/                  # Interfaz gráfica del clasificador
├── resultados/                 # Generado en local — excluido por .gitignore
│
├── app_1.py                    # Primera versión funcional con Ollama
├── config.py                   # Configuración compartida terminal + interfaz
├── .gitignore
└── readme.md
```

> **Nota:** La carpeta `resultados/` y todos los archivos `.json` / `.txt` generados están excluidos del repositorio mediante `.gitignore`.

---

## 🚀 Instalación

### 1. Instalar Ollama

```bash
# Windows / macOS: descargar el instalador desde https://ollama.com/download

# Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# Verificar instalación:
ollama --version
```

### 2. Descargar un modelo de visión

```bash
# Recomendado (balance calidad/velocidad):
ollama pull llava

# Para PCs con poca RAM (4 GB):
ollama pull moondream

# Máxima precisión (requiere 16 GB+):
ollama pull llava:13b
```

### 3. Instalar dependencias Python

```bash
pip install requests
```

### 4. Arrancar el servidor de Ollama

```bash
# Dejar esta terminal abierta mientras usas el clasificador:
ollama serve
```

---

## ▶️ Uso

### Configuración (`config.py`)

El archivo `config.py` es compartido entre el clasificador de terminal y la interfaz gráfica, garantizando resultados **idénticos** en ambos entornos:

```python
# config.py — configuración compartida terminal + interfaz

MODELO_VISION = "llava"
OLLAMA_URL = "http://localhost:11434/api/generate"

CONFIG_CONSISTENTE = {
    "temperature": 0.0,
    "seed": 42,
    "num_predict": 150,
    "top_k": 1,
    "top_p": 0.9,
    "repeat_penalty": 1.0,
    "stream": False
}

TIMEOUT = 120
MAX_REINTENTOS = 3
CARPETA_IMAGENES = "img"
CARPETA_RESULTADOS = "resultados"

CATEGORIAS_POR_DEFECTO = [
    "gato", "perro", "pajaro", "auto",
    "comida", "persona", "flor", "arbol",
    "casa", "desconocido"
]
```

> ⚠️ **Nota:** El `config.py` actual tiene contenido duplicado. Conviene dejar solo un bloque limpio y único.

### Ejecutar el clasificador

```bash
python app_1.py
```

### Ejecutar la interfaz gráfica

```bash
# Desde la carpeta interface/
cd interface
python <nombre_del_script_de_interfaz>.py
```

---

## 🧪 Actividad guiada

### Parte 1 — Entender el código base

El archivo `clasificacionImagenes.py`:

- Usa un modelo de IA para clasificar imágenes.
- Recibe una imagen y una lista de categorías.
- Devuelve categoría, confianza y explicación.

**Tarea:**

- Ejecutar el código.
- Analizar cómo funciona.
- Identificar prompt, formato JSON y flujo de datos.

### Parte 2 — Migración a modelos locales

Debes modificar el sistema para que funcione sin API externa, usando modelos locales.

**Requisitos:**

- Implementar al menos 2 modelos distintos.
- Por ejemplo: `llava` y `moondream`.

**Objetivo:**

- Comparar precisión.
- Comparar velocidad.
- Comparar tipo de respuestas.
- Comparar consistencia.

### Parte 3 — Comparación de resultados

Debes ejecutar el clasificador sobre las 9 imágenes de la carpeta `img/`.

**Salida esperada:**

```text
resultados/
├── json/
│   ├── imagen1.json
│   ├── imagen2.json
│   └── ...
├── txt/
│   ├── imagen1.txt
│   ├── imagen2.txt
│   └── ...
```

**Formato esperado:**

```json
{
  "categoria": "gato",
  "confianza": 0.95,
  "razones": "Se observan orejas puntiagudas..."
}
```

```text
Imagen: gato1.jpg
Categoría: gato
Confianza: 0.95
Razón: Se observan orejas puntiagudas...
```

### Parte 4 — Interfaz gráfica

Se proporciona una interfaz similar a entorno profesional.

**Características:**

- Selección de imágenes.
- Gestión de categorías.
- Visualización de resultados.
- Exportación JSON / TXT.

**Tarea:**

- Ejecutar la interfaz demo.
- Analizar flujo de usuario, organización y funcionalidad.

### Parte 5 — Mejora de interfaz

Debes crear una versión mejorada de la interfaz.

Puedes mejorar:

- Diseño visual.
- Experiencia de usuario.
- Feedback de carga o progreso.
- Visualización de resultados.
- Comparación entre modelos.
- Filtros o estadísticas.

**Bonus ideas:**

- Mostrar imagen y resultado juntos.
- Gráficas de resultados.
- Selector dinámico de modelo.
- Historial de ejecuciones.

### Parte 6 — Experimentación

Prueba variaciones como:

- Cambiar categorías.
- Añadir imágenes propias.
- Ajustar prompts.
- Comparar resultados entre modelos.

---

## 📋 Entregables

El alumno debe entregar:

- ✅ Código funcional con mínimo 2 modelos.
- ✅ Carpeta `resultados/` con JSON y TXT.
- ✅ Interfaz mejorada.
- ✅ Documento breve explicando diferencias entre modelos, problemas encontrados y conclusiones.

---

## 🧠 Criterios de evaluación

- Funcionamiento del código.
- Correcta generación de resultados.
- Comparación entre modelos.
- Calidad de la interfaz.
- Capacidad de análisis.

---

## 🔄 Evolución del Proyecto

| Versión | Archivo | Descripción |
|---|---|---|
| v0 (heredado) | `src/heredado/clasificacionImagenes.py` | Código original con OpenAI — solo referencia |
| v1 | `app_1.py` | Primera versión funcional con Ollama. Verificación de conexión, clasificación JSON, salida en terminal |
| Config | `config.py` | Configuración centralizada compartida: temperatura, semilla, timeout, prompt unificado |
| Interfaz | `interface/` | Interfaz gráfica que replica la salida de terminal gracias a `config.py` |

Para el detalle técnico de todos los cambios, consulta [`docs/arreglar.md`](docs/arreglar.md).

---

## 🛠️ Tecnologías

- **Python 3.10+**
- **[Ollama](https://ollama.com)** — servidor local de modelos LLM/visión
- **`requests`** — cliente HTTP para comunicarse con Ollama
- **Modelos:** `llava`, `moondream`, `llava:13b`, `bakllava`, `llava-phi3`

---

## 📄 Licencia

Proyecto educativo de uso libre. Consulta el archivo `LICENSE` si existe, o contacta al autor del repositorio.