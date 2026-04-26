# Sistema de Análisis de Tickets de Soporte con NLP (Ollama)

## 📋 Descripción

Sistema que utiliza NLP para analizar automáticamente tickets de soporte usando **modelos locales de Ollama** (gratuito, sin API keys). Clasifica por categoría, urgencia, extrae entidades y sugiere acciones.

## 🔄 Comparativa: OpenAI vs Ollama

| Característica | OpenAI | Ollama |
|----------------|--------|--------|
| 💰 Costo | Por uso | **Gratis** |
| 🔒 Privacidad | Envía tickets | **Local** |
| 🌐 Internet | Requerido | **No necesario** |
| 🇪🇸 Español | Bueno | **Excelente (Qwen2.5)** |
| ⚡ Velocidad | Rápida | Variable según PC |
| 🔧 Configuración | API key | **Una variable** |

## 📦 Instalación

```bash
# 1. Instalar Ollama
# Windows/Mac: Descargar de https://ollama.ai
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# 2. Descargar modelo recomendado (para español)
ollama pull qwen2.5:7b

# 3. Iniciar servidor
ollama serve

# 4. Instalar dependencias Python
pip install requests python-dotenv

# 5. Ejecutar
python app.py

🚀 Modelos Disponibles
Modelo	Tamaño	RAM	Mejor para	Instalación
qwen2.5:7b	7B	8GB	⭐ Español	ollama pull qwen2.5:7b
llama3.1:8b	8B	8GB	Balanceado	ollama pull llama3.1:8b
mistral:7b	7B	8GB	Clasificación	ollama pull mistral:7b
llama3.2:3b	3B	4GB	Rápido, ligero	ollama pull llama3.2:3b
phi3:mini	3.8B	4GB	Muy rápido	ollama pull phi3:mini

📁 Estructura del Proyecto (a crear por los alumnos)
text
tickets-soporte-nlp/
├── app.py              # Código base (con Ollama)
├── requirements.txt    # Dependencias
├── README.md           # Documentación
├── src/                # (Crear) Código refactorizado
│   ├── __init__.py
│   ├── models.py       # Modelos de datos
│   ├── preprocess.py   # Preprocesamiento
│   ├── nlp_analyzer.py # Análisis con Ollama
│   ├── actions.py      # Acciones
│   └── pipeline.py     # Pipeline principal
├── tests/              # (Crear) Tests unitarios
│   ├── __init__.py
│   ├── test_preprocess.py
│   ├── test_nlp_analyzer.py
│   └── test_actions.py
└── data/               # (Crear) Datos de ejemplo
    └── tickets_ejemplo.json