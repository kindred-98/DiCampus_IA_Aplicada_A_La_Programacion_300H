# Bloque 3: Conceptos clave de APIs de IA

## Conceptos fundamentales

| Concepto | Descripción |
|---------|-------------|
| **Tokens** | Unidades mínimas que consume un modelo (trozos de palabras). Determinan el coste y la longitud del procesamiento. |
| **Context Window** | Cantidad máxima de tokens que el modelo puede "recordar" en una sola interacción. |
| **Temperature** | Controla el grado de creatividad. Valores bajos → respuestas precisas. Valores altos → respuestas más variadas. |
| **Max Tokens** | Límite de tokens que el modelo puede generar como salida. |
| **System Prompt** | Bloque inicial que define el comportamiento del modelo: rol, estilo, reglas y límites. |
| **Few-shot** | Técnica para enseñar al modelo cómo debe responder mostrando ejemplos directamente en el prompt. |
| **Embeddings** | Representaciones numéricas que capturan el significado de textos o imágenes. |

---

## Ejemplo 1: Contar tokens con tiktoken (OpenAI)

**Python**

```python
import tiktoken

def contar_tokens(texto: str, modelo: str = "gpt-4o"):
    encoding = tiktoken.encoding_for_model(modelo)
    tokens = encoding.encode(texto)
    print(f"Texto: '{texto[:50]}...'")
    print(f"Caracteres: {len(texto)}")
    print(f"Tokens: {len(tokens)}")
    return tokens

contar_tokens("Hola, ¿cómo estás?")
contar_tokens("La inteligencia artificial está transformando el mundo.")
```

**JavaScript**

```javascript
import tiktoken from "tiktoken";

async function contarTokens(texto, modelo = "gpt-4o") {
  const encoding = await tiktoken.encode(modelo);
  const tokens = encoding.encode(texto);
  console.log(`Texto: '${texto.slice(0, 50)}...'`);
  console.log(`Caracteres: ${texto.length}`);
  console.log(`Tokens: ${tokens.length}`);
  return tokens;
}

contarTokens("Hola, ¿cómo estás?");
contarTokens("La inteligencia artificial está transformando el mundo.");
```

---

## Ejemplo 2: Efecto de la temperature

**Python**

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def probar_temperature(pregunta: str, temperatura: float):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": pregunta}],
        temperature=temperatura
    )
    return response.choices[0].message.content

pregunta = "Escribe una frase sobre la luna"

print("TEMPERATURE 0.0 (predecible):")
print(probar_temperature(pregunta, 0.0))
print("\nTEMPERATURE 1.0 (creativa):")
print(probar_temperature(pregunta, 1.0))
```

**JavaScript**

```javascript
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function probarTemperature(pregunta, temperatura) {
  const response = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: pregunta }],
    temperature: temperatura
  });
  return response.choices[0].message.content;
}

const pregunta = "Escribe una frase sobre la luna";

console.log("TEMPERATURE 0.0 (predecible):");
console.log(await probarTemperature(pregunta, 0.0));
console.log("\nTEMPERATURE 1.0 (creativa):");
console.log(await probarTemperature(pregunta, 1.0));
```

---

## Ejemplo 3: System prompt para definir comportamiento

**Python**

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def asistente_con_personalidad(pregunta: str, personalidad: str):
    system_prompts = {
        "tecnico": "Eres un experto técnico. Responde con precisión, usando terminología profesional.",
        "divulgativo": "Eres un divulgador amigable. Explica conceptos complejos de forma sencilla.",
        "poeta": "Eres un poeta. Responde con lenguaje poético y evocador."
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompts.get(personalidad, system_prompts["divulgativo"])},
            {"role": "user", "content": pregunta}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

print("TÉCNICO:")
print(asistente_con_personalidad("¿Qué es una API?", "tecnico"))
print("\nDIVULGATIVO:")
print(asistente_con_personalidad("¿Qué es una API?", "divulgativo"))
```

**JavaScript**

```javascript
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function asistenteConPersonalidad(pregunta, personalidad) {
  const systemPrompts = {
    tecnico: "Eres un experto técnico. Responde con precisión, usando terminología profesional.",
    divulgativo: "Eres un divulgador amigable. Explica conceptos complejos de forma sencilla.",
    poeta: "Eres un poeta. Responde con lenguaje poético y evocador."
  };

  const response = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: systemPrompts[personalidad] || systemPrompts.divulgativo },
      { role: "user", content: pregunta }
    ],
    temperature: 0.7
  });
  return response.choices[0].message.content;
}

console.log("TÉCNICO:");
console.log(await asistenteConPersonalidad("¿Qué es una API?", "tecnico"));
console.log("\nDIVULGATIVO:");
console.log(await asistenteConPersonalidad("¿Qué es una API?", "divulgativo"));
```

---

## Ejemplo 4: Few-shot learning para clasificación

**Python**

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clasificar_con_ejemplos(texto: str):
    prompt = """
Clasifica el sentimiento del texto como "POSITIVO", "NEUTRO" o "NEGATIVO".

EJEMPLOS:
Texto: "Me encanta este producto, es increíble"
Sentimiento: POSITIVO

Texto: "El servicio fue aceptable, sin más"
Sentimiento: NEUTRO

Texto: "Pésima experiencia, no lo recomiendo"
Sentimiento: NEGATIVO

AHORA CLASIFICA ESTE TEXTO:
Texto: """ + texto + """
Sentimiento:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

textos = [
    "La aplicación funciona perfectamente, muy contento",
    "Regular, cumple pero no esperaba más",
    "Horrible, perdí mi dinero"
]

for texto in textos:
    resultado = clasificar_con_ejemplos(texto)
    print(f"'{texto}' → {resultado}")
```

**JavaScript**

```javascript
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function clasificarConEjemplos(texto) {
  const prompt = `
Clasifica el sentimiento del texto como "POSITIVO", "NEUTRO" o "NEGATIVO".

EJEMPLOS:
Texto: "Me encanta este producto, es incredible"
Sentimiento: POSITIVO

Texto: "El servicio fue aceptable, sin mas"
Sentimiento: NEUTRO

Texto: "Pesima experiencia, no lo recomiendo"
Sentimiento: NEGATIVO

AHORA CLASIFICA ESTE TEXTO:
Texto: ${texto}
Sentimiento:
`;

  const response = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: prompt }],
    temperature: 0.0
  });
  return response.choices[0].message.content.trim();
}

const textos = [
  "La aplicación funciona perfectamente, muy contento",
  "Regular, cumple pero no esperaba más",
  "Horrible, perdí mi dinero"
];

for (const texto of textos) {
  const resultado = await clasificarConEjemplos(texto);
  console.log(`'${texto}' → ${resultado}`);
}
```

---

## Ejemplo 5: Embeddings para búsqueda semántica

**Python**

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def obtener_embedding(texto: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texto
    )
    return response.data[0].embedding

documentos = [
    "La inteligencia artificial permite a las máquinas aprender de la experiencia",
    "Las APIs son interfaces que permiten a programas comunicarse entre sí",
    "El aprendizaje automático es una rama de la inteligencia artificial",
    "Python es un lenguaje de programación muy popular",
    "Los embeddings convierten texto en vectores numéricos"
]

embeddings = [obtener_embedding(doc) for doc in documentos]

def buscar_semanticamente(consulta: str, documentos: list, embeddings: list, top_k: int = 2):
    consulta_emb = obtener_embedding(consulta)
    similitudes = []
    for i, doc_emb in enumerate(embeddings):
        sim = cosine_similarity([consulta_emb], [doc_emb])[0][0]
        similitudes.append((i, sim))
    similitudes.sort(key=lambda x: x[1], reverse=True)
    return [{"documento": documentos[i], "similitud": sim} for i, sim in similitudes[:top_k]]

consulta = "¿Cómo aprenden las máquinas?"
resultados = buscar_semanticamente(consulta, documentos, embeddings)
for r in resultados:
    print(f"{r['documento']} (similitud: {r['similitud']:.4f})")
```

**JavaScript**

```javascript
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function obtenerEmbedding(texto) {
  const response = await client.embeddings.create({
    model: "text-embedding-3-small",
    input: texto
  });
  return response.data[0].embedding;
}

const documentos = [
  "La inteligencia artificial permite a las máquinas aprender de la experiencia",
  "Las APIs son interfaces que permiten a programas comunicarse entre sí",
  "El aprendizaje automático es una rama de la inteligencia artificial",
  "Python es un lenguaje de programación muy popular",
  "Los embeddings convierten texto en vectores numéricos"
];

const embeddings = await Promise.all(documentos.map(doc => obtenerEmbedding(doc)));

function cosineSimilarity(a, b) {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

async function buscarSemanticamente(consulta, documentos, embeddings, topK = 2) {
  const consultaEmb = await obtenerEmbedding(consulta);
  const similitudes = embeddings.map((docEmb, i) => ({
    index: i,
    similitud: cosineSimilarity(consultaEmb, docEmb)
  }));
  similitudes.sort((a, b) => b.similitud - a.similitud);
  return similitudes.slice(0, topK).map(s => ({
    documento: documentos[s.index],
    similitud: s.similitud
  }));
}

const consulta = "¿Cómo aprenden las máquinas?";
const resultados = await buscarSemanticamente(consulta, documentos, embeddings);
resultados.forEach(r => {
  console.log(`${r.documento} (similitud: ${r.similitud.toFixed(4)})`);
});
```

---

## Diferencias clave resumidas

| Diferencia | Python | JavaScript |
|-----------|--------|------------|
| Sintaxis de importación | `from module import Class` | `import { Class } from "module"` |
| Inicialización de cliente | `OpenAI(api_key=...)` | `new OpenAI({ apiKey: ... })` |
| Variables de entorno | `os.getenv("KEY")` | `process.env.KEY` |
| Ejecución | Síncrono por defecto | Siempre async/await |
| Uso principal | Backend, scripts, data | Frontend, Node.js, APIs web |