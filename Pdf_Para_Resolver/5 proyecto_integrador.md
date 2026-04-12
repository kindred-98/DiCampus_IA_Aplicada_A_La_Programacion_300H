# 5 — Proyecto Integrador Final: Asistente de IA para Gestión de Contratos Legales

## Resumen del Proyecto

| Aspecto | Descripción |
|--------|-------------|
| **Nombre** | LegalDocs AI |
| **Funcionalidad** | Analizar contratos PDF, detectar cláusulas de riesgo, responder preguntas, generar resumen ejecutivo |
| **Presupuesto** | Limitado (startup en fase temprana) |
| **Volumen** | ~50 contratos/semana inicialmente |

---

## Decisiones Técnicas 

### 1. Proveedor y Modelo untuk Análisis de Contratos Largos

| Decisión | Justificación |
|---------|--------------|
| **Proveedor: Anthropic (Claude 3.5 Sonnet)** | Tiene 200K tokens de context window vs 128K de GPT-4o. Permite procesar contratos completos de una sola vez. |
| **Alternativa: Google Gemini 1.5 Pro** | Hasta 2M tokens context, pero el precio es variable. Lo uso como backup. |
| **Modelo principal: Claude 3.5 Sonnet** | Ideal para análisis profundo de documentos legales. Excelente en razonamiento y precisión. |
| **Modelo secundario: Claude 3 Haiku** | Para tareas simples (clasificar, resumir breve). 5x más barato. |

**Por qué NO GPT-4o:**
- Context window de 128K tokens puede no ser suficiente para contratos largos (un contrato = ~30K-50K tokens)
- Claude tiene enfoque en "IA constitucional" = mejor siguiendo instrucciones de seguridad
- Mejor relación calidad/precio para documentos largos

---

### 2. Parámetros Clave

| Parámetro | Valor | Justificación |
|-----------|-------|-------------|
| **temperature** | 0.1 | Los contratos son documentos legales. Necesitamos precisión, no creatividad. Un valor bajo evita que el modelo "invent clauses". |
| **max_tokens** | 1500 | Un resumen ejecutivo de contrato no necesita más de 1-2 páginas. Limitamos para controlar costes. |
| **system prompt** | "Eres un asistente legal experto. Analizas contratos y extraes cláusulas de riesgo. Respondes de forma precisa, citing las cláusulas específicas. Nunca inventas información." | Define el rol profesional, las reglas de resposta, y la prohibición de inventar. |
| **max_tokens para preguntas** | 500 | Respuestas cortas a preguntas específicas. Suficiente para concretos facts. |
| **few-shot** | Incluir 3 exemplos de contratos con cláusulas problemáticas conhecidas | Enseña al modelo qué buscar sin hacer fine-tuning. |

---

### 3. Estructura de Módulos

```
legal_docs_ai/
├── .env                              # NO subir
├── .gitignore
├── requirements.txt
├── config.py                         # Configuración centralizada
├── parser.py                         # Extracción de texto de PDF
├── analizador.py                    # Análisis de cláusulas
├── resumidor.py                      # Generación de resúmenes
├── chat.py                          # Q&A sobre el contrato
├── orquestador.py                    # Coordinación
├── base_clausulas/                  # Base de cláusulas de riesgo
│   └── clausulas.json
└── main.py                         # Punto de entrada
```

| Módulo | Responsabilidad | API/Llamada |
|--------|---------------|-------------|
| **parser.py** | Extrae texto de PDF usando PyPDF2 | No usa IA |
| **analizador.py** | Detecta cláusulas de riesgo | Claude 3.5 Sonnet + few-shot |
| **resumidor.py** | Genera resumen ejecutivo | Claude 3.5 Haiku (más barato) |
| **chat.py** | Responde preguntas sobre contrato | Claude 3.5 Sonnet |
| **orquestador.py** | Coordina todos los módulos | Orchestration |

---

### 4. Gestión Segura de API Keys

| Paso | Acción | Justificación |
|------|--------|---------------|
| **1. Crear API key** | En consola de Anthropic, crear una nueva API key | Una key por proyecto |
| **2. GitHub Secrets** | Settings → Secrets → ANTHROPIC_API_KEY | Nunca en código |
| **3. .gitignore** | Añadir `.env`, `__pycache__/`, `*.pyc` | Previene subi files sensibles |
| **4. Código** | Usar `os.getenv("ANTHROPIC_API_KEY")` | Carga segura |
| **5. Rotar key** | Cambiar cada 90 días | Best practice de seguridad |
| **6. Limitar en consola** |设置 monthly spend limit (ej: $50/mes) | Control de costes |

---

### 5. Control de Costes

| Estrategia | Implementación |
|------------|---------------|
| **Modelo correcto** | Haiku para resúmenes simples, Sonnet para análisis profundo |
| **Cachear contratos** | Si el mismo contrato se analiza, usar versión cacheada (hash) |
| **Max tokens** | Limitar a 1500 para resúmenes, 500 para preguntas |
| **Rate limiting** | Máximo 10 llamadas/minuto en el pipeline |
| **Presupuesto alerta** | Configurar alert en consola de Anthropic a $20/mes |
| **Pipeline manual** | No ejecutar en cada commit, solo en workflow_dispatch o nightly |

**Coste estimado:**

| Tarea | Tokens (input+output) | Coste | Volumen | Coste semanal |
|-------|------------------------|-------|---------|---------------|
| Análisis de contrato | 50K + 1K | $0.15 | 50/semana | $7.50 |
| Resumen ejecutivo | 50K + 500 | $0.02 | 50/semana | $1.00 |
| Q&A (5 preg/contrato) | 55K × 5 = 275K | $0.08 | 50/semana | $4.00 |
| **TOTAL** | | | | | **$12.50/semana ≈ $50/mes** |

---

### 6. Errores Anticipados y Manejo

| Error | Causa | Manejo |
|--------|-------|--------|
| **PDF no readable** | Escaneo o formato extraño | Usar OCR (pytesseract) o marcar como "no procesable" |
| **Contratto demasiado largo** | >200K tokens | Dividir en secciones y procesar por partes |
| **API key inválida** | Key expirada | Verificar al inicio, notificar si falla |
| **Rate limit excedido** | Muchas peticiones | Backoff exponencial, cola de procesamiento |
| **Respuesta vacía** | El modelo no detecta cláusulas | Devolver "no se detectaron cláusulas de riesgo" |
| **Costo超标** | Uso excesivo | Alerts, detener pipeline si supera umbral |
| **Timeout** | Contratto muy largo | Chunking, procesamiento asíncrono |

---

## Código Destacado

### analizador.py (Análisis de cláusulas)

```python
from anthropic import Anthropic
import os
import json
from typing import List, Dict

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """Eres un asistente legal experto en análisis de contratos.
Tu tarea es identificar cláusulas de riesgo en contratos legales.
Detecta y clasifica las cláusulas en estas categorías:
- CLAUSULAS DE RIESGO ALTO: Penalizaciones excesivas, renovación automática, jurisdicción extranjera
- CLAUSULAS DE RIESGO MEDIO: Límites de responsabilidad, modificación unilateral
- CLAUSULAS DE BAJO RIESGO: Términos estándar

Para cada cláusula detectada, indica:
- Tipo de riesgo
- Texto exacto de la cláusula
- Recomendación/action sugerida

Responde en JSON con este formato:
{
  "resumen": "resumen breve del contrato",
  "clausulas": [
    {
      "tipo": "RIESGO ALTO/MEDIO/BAJO",
      "sección": "número o referencia",
      "texto": "texto exacto",
      "recomendación": "qué hacer"
    }
  ],
  "recomendacion_general": "consejo general"
}"""

# Few-shot examples
FEW_SHOT = """
Ejemplo 1 (cláusula alta):
{"tipo": "RIESGO ALTO", "sección": "12.3", "texto": "El proveedor podrá modificar unilaterally los términos...", "recomendación": "Negociar cláusula de aviso previo"}

Ejemplo 2 (sin riesgo):
{"tipo": "BAJO", "sección": "1.1", "texto": "Las partes agree a cumplir con la legislación vigente", "recomendación": "Aucune acción requerida"}
"""

def analizar_contrato(texto_contrato: str) -> dict:
    # Reducir si es muy largo (truncar a 180K tokens paraLeave room)
    if len(texto_contrato) > 180000 * 4:  # ~180K caracteres
        texto_contrato = texto_contrato[:180000 * 4]
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.1,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": f"{FEW_SHOT}\n\nCONTRATO:\n{texto_contrato}"}
            ]
        )
        
        respuesta = response.content[0].text
        
        # Intentar parsear JSON
        try:
            return json.loads(respuesta)
        except json.JSONDecodeError:
            # Si no es JSON válido, crear estructura manual
            return {
                "resumen": respuesta[:500],
                "clausulas": [],
                "recomendacion_general": "Revisar manualmente"
            }
            
    except Exception as e:
        return {
            "error": str(e),
            "resumen": None,
            "clausulas": [],
            "recomendacion_general": "Error al analizar"
        }
```

### orquestador.py (Coordinación completa)

```python
import hashlib
from pathlib import Path
import json

class OrquestadorContratos:
    def __init__(self):
        self.cache = {}  # Cache en memoria
        self.procesados = []
    
    def hash_contrato(self, texto: str) -> str:
        """Genera hash del contrato para cache"""
        return hashlib.md5(texto.encode()).hexdigest()
    
    def esta_cacheado(self, hash_contrato: str) -> bool:
        return hash_contrato in self.cache
    
    def procesar(self, pdf_path: str) -> dict:
        """Procesa un contrato completo"""
        from parser import extraer_texto
        from analizador import analizar_contrato
        from resumidor import resumir_contrato
        
        # 1. Extraer texto
        texto = extraer_texto(pdf_path)
        if "error" in texto:
            return texto
        
        # 2. Check cache
        hash_contrato = self.hash_contrato(texto)
        if self.esta_cacheado(hash_contrato):
            return self.cache[hash_contrato]
        
        # 3. Análisis completo
        analisis = analizar_contrato(texto)
        resumen = resumir_contrato(texto)
        
        resultado = {
            "hash": hash_contrato,
            "resumen_ejecutivo": resumen,
            "analisis": analisis,
            "errores": []
        }
        
        # 4. Guardar en cache
        self.cache[hash_contrato] = resultado
        self.procesados.append(hash_contrato)
        
        return resultado
    
    def procesar_lote(self, pdf_paths: List[str]) -> List[dict]:
        """Procesa múltiples contratos"""
        resultados = []
        for pdf_path in pdf_paths:
            print(f"Procesando: {pdf_path}")
            resultado = self.procesar(pdf_path)
            resultados.append(resultado)
            
            # Rate limiting entre contratos
            import time
            time.sleep(1)
        
        return resultados
```

---

## Pipeline de CI/CD

```yaml
name: LegalDocs AI - CI/CD

on:
  workflow_dispatch:  # Solo manualmente
  schedule:
    - cron: '0 2 * * *'  # nightly a las 2am

jobs:
  analisis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Instalar dependencias
        run: pip install -r requirements.txt
      
      - name: Análisis de contratos nuevos
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python main.py --lote contratos_nuevos/
      
      - name: Generar informe
        if: always()
        run: python generar_informe.py
      
      - name: Notificar
        if: failure()
        uses: 8398a1/action-slack@v2
        with:
          status: ${{ job.status }}
```

---

## Comparativa Final: anthropic vs OpenAI

| Aspecto | Claude 3.5 Sonnet | GPT-4o |
|--------|------------------|--------|
| **Context window** | 200K tokens | 128K tokens |
| **Coste** | $3/1M input, $15/1M output | $5/1K input, $15/1K output |
| **Análisis legal** | Excelente (enfoque constitucional) | Bueno |
| **Seguridad** | Mejor siguiendo instrucciones | Standard |
| **Veredicto** | ✅ Mejor para contratos largos | Para documentos cortos |

---

## Resumen de la Decisión

| Decisión | Justificación |
|---------|--------------|
| **Problema** | Analizar contratos PDF, detectar jurídic risks, responder questions |
| **Proveedor** | Anthropic (Claude) - context window 200K |
| **Modelo** | 3.5 Sonnet análisis, 3 Haiku resúmenes |
| **Temperature** | 0.1 - precisión sin creatividad |
| **Max tokens** | 1500 resúmenes, 500 preguntas |
| **API key** | GitHub Secrets + .gitignore |
| **Coste** | ~$50/mes para 50 contratos |
| **Errores** | Backoff, cache, validación, logging |