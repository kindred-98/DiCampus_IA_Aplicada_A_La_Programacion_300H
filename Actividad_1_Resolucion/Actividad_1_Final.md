# 🧪 Módulo 4 · Introducción a APIs de IA
## APIs de IA — Fundamentos y Proveedores
**Ejercicio de Clase · Ejercicio 1 de 3 · Bloques 4.1 — 4.2 — 4.3**

---

| Campo | Valor |
|---|---|
| **Nombre del alumno/a** | Angel Echenique |
| **Fecha** | 08/04/2026 |
| **🔗 Enlace GitHub del repositorio** |-----|

---

> 📌 **Instrucciones:** Responde con lo que hemos visto en clase. Puedes consultar tus apuntes. No hay que escribir código, ¡solo demostrar que entendiste!

---

## BLOQUE 1 — ¿Qué es una API de IA? (4.1)

### 1.1 — Características clave

En clase vimos las características clave de una API de IA. Escríbelas y explica brevemente para qué sirve cada una:

| Nº | Característica | ¿Para qué sirve concretamente? |
|---|---|---|
| **1** | **Modelos preentrenados** | Ofrecen capacidades avanzadas listas para usar (texto, visión, audio, predicción). No necesitas entrenar nada. |
| **2** | **Respuestas en tiempo real** | Procesan datos y devuelven resultados en milisegundos, ideales para apps interactivas. |
| **3** | **Multicapacidad** | Una misma API puede analizar texto, clasificar imágenes, transcribir audio o generar contenido. |
| **4** | **Escalabilidad y seguridad** | El proveedor gestiona infraestructura, actualizaciones y protección de datos. |
| **5** | **Coste por uso** | Pagas solo por las llamadas realizadas, sin inversión inicial ni mantenimiento. |
| **6** | **Ventaja clave** | Permiten integrar IA profesional en cualquier aplicación con pocas líneas de código. |

---

### 1.2 — Idea clave del módulo

Completa esta frase que vimos al inicio de la sesión:

> *"Las APIs de IA permiten incorporar capacidades avanzadas sin necesidad de **entrenar**, mantener ni desplegar modelos propios. Son la forma más rápida de añadir inteligencia a cualquier aplicación porque **abstraen** toda la complejidad del machine learning."*

¿Qué NO tienes que hacer cuando usas una API de IA en lugar de entrenar tu propio modelo? Explícalo con la analogía vista en clase:

> *Con la analogía vista en clase: es como **contratar especialistas ya formados** en lugar de entrenar un equipo desde cero. No necesitas:**
> - Contratar expertos en lingüística, visión por computador, análisis de datos
> - Comprar GPU caras para entrenamiento
> - Mantener servidores con modelos
> - Recopilar miles de datos para entrenar
>
> Solo envías una petición ("analiza este texto", "resume este documento") y te devuelven la respuesta lista.*

---

## BLOQUE 2 — Proveedores principales (4.2)

### 2.1 — Une proveedor, especialidad y caso de uso

Une cada proveedor con su especialidad y escribe para qué caso de uso es ideal:

| Proveedor | Especialidad | ¿Para qué es ideal? |
|---|---|---|
| **OpenAI** | NLP, chat, embeddings | Chatbots, asistentes, generación de texto. Es el estándar de la industria. |
| **Hugging Face** | Modelos open-source | Personalización, NLP específico. Ideal para quienes necesitan privacidad total (descargar modelos y ejecutarlos en su propio servidor). |
| **Google AI (Gemini)** | Multimodal, visión | Apps con imágenes + texto. Su context window de 2M de tokens es su mayor ventaja. |
| **Anthropic (Claude)** | Contexto largo | Análisis de documentos extensos, contratos, código complejo. Enfoque en seguridad y "IA constitucional". |
| **AWS Bedrock** | Modelos múltiples | Empresas con AWS. Integración nativa con servicios cloud de Amazon. |
| **Azure OpenAI** | OpenAI + compliance | Entornos Microsoft. Seguridad, cumplimiento (GDPR, HIPAA, ISO) y despliegue empresarial. |
| **Mistral AI** | Modelos ligeros y eficientes | Integraciones rápidas, despliegues híbridos. Modelos económicos y personalizables. |
| **Meta (Llama Models)** | Modelos open-source potentes | Soluciones on-premise. Libertad total para adaptar y desplegar sin dependencias de nube. |

---

### 2.2 — Verdadero o Falso: Proveedores

Marca V (Verdadero) o F (Falso) y justifica brevemente las que sean Falsas:

| V / F | Afirmación | Justificación si es Falsa |
|---|---|---|
| **V** | OpenAI es el proveedor que marca el estándar en la industria en 2025. | Es el más conocido y sus modelos GPT son referencia. |
| **F** | Hugging Face es un único modelo de lenguaje disponible en la nube. | Hugging Face es una **plataforma** que alberga miles de modelos open-source (Mistral, Llama, BLOOM, etc.). No es un único modelo. |
| **V** | Google Gemini 1.5 Pro tiene una ventana de contexto de hasta 2 millones de tokens. | Puede procesar documentos enormesen una sola petición. |
| **V** | Anthropic Claude es la opción preferida para procesar información sensible empresarial. | Su enfoque en "IA constitucional" permite seguir instrucciones de seguridad con precisión. |
| **F** | Azure OpenAI y OpenAI ofrecen exactamente los mismos modelos sin diferencias. | Azure ofrece los modelos de OpenAI pero con **infraestructura de Microsoft**, certificaciones de cumplimiento (GDPR, HIPAA, ISO) y opciones de seguridad empresarial que la versión directa no tiene. |
| **V** | Hugging Face permite descargar modelos open-source para ejecutarlos en tu propia infraestructura. | Sí, puedes descargar Mistral, Llama, etc., y ejecutarlos on-premise para privacidad total. |
| **V** | GPT-4o-mini cuesta hasta 20 veces menos que el modelo GPT-4o completo. | Es la opción económica ideal para prototipos y apps educativas. |

---

### 2.3 — ¿Qué proveedor elegirías?

Para cada caso de uso, indica qué proveedor elegirías de los vistos en clase y justifica brevemente:

| Caso de uso | Proveedor elegido | ¿Por qué? |
|---|---|---|
| Quieres hacer un chatbot educativo de bajo coste para un prototipo. | **OpenAI (GPT-4o-mini)** | Es el mejor equilibrio precio/rendimiento. Muy económico (20x más barato que GPT-4o) y suficientemente potente para un chatbot educativo. |
| Necesitas procesar datos médicos confidenciales en tu propio servidor. | **Hugging Face** o **Meta (Llama)** | Permite descargar modelos y ejecutarlos **on-premise**, así los datos nunca salen de la organización (privacidad total). |
| Tu empresa ya trabaja con Microsoft y necesita cumplimiento GDPR e HIPAA. | **Azure OpenAI** | Ofrece los modelos de OpenAI dentro del ecosistema Microsoft con certificaciones de cumplimiento normativo (GDPR, HIPAA, ISO). |
| Quieres analizar imágenes y texto en la misma petición con contexto muy largo. | **Google AI (Gemini 1.5 Pro)** | Es multimodal (texto + imagen) y tiene la ventana de contexto más grande (2M tokens). |
| Necesitas embeddings para un buscador semántico corporativo. | **Cohere** o **OpenAI** | Cohere destaca en embeddings y NLP empresarial; OpenAI también ofrece embeddings de calidad (text-embedding-3-small). |

---

## BLOQUE 3 — Conceptos clave de APIs de IA (4.3)

### 3.1 — Define los conceptos

Define con tus propias palabras cada concepto clave visto en clase. Incluye un ejemplo concreto para cada uno:

| Concepto | Definición con tus palabras | Ejemplo concreto |
|---|---|---|
| **Tokens** | Son las unidades mínimas que el modelo procesa. Es como la "moneda" que se consume en cada llamada. Un token puede ser una palabra completa o parte de ella. | "Hola" = 1 token, "extraordinariamente" = 4 tokens, "inteligencia artificial" = 3 tokens. |
| **Context window** | Es la "memoria" del modelo: la cantidad máxima de tokens que puede recordar en una sola conversación. Si lo superas, olvida el principio. | GPT-4o-mini tiene 128.000 tokens (equivalente a un libro de ~300 páginas). Si hablas más que eso, olvida lo que dijiste al inicio. |
| **Temperature** | Controla la creatividad del modelo. Valores bajos = respuestas predecibles. Valores altos = respuestas creativas/impredecibles. | Temperature 0.0 = respuesta siempre igual para la misma pregunta. Temperature 1.0 = respuestas muy variadas y originales. |
| **Max tokens** | Es el límite de tokens que el modelo puede **generar como salida**. No afecta al input, solo restringe la longitud de la respuesta. | Si pones max_tokens=50, la respuesta será muy corta. Si pones max_tokens=1000, puede generar textos largos. |
| **System prompt** | Es un mensaje especial (invisible para el usuario) que define cómo debe comportarse el modelo: su rol, tono, reglas y límites. | "Eres un asistente técnico experto en Python. Responde de forma clara y didáctica, usando ejemplos de código." |
| **Few-shot learning** | Técnica para enseñar al modelo cómo debe responder incluyéndole ejemplos dentro del prompt. Es "entrenar en caliente" sin fine-tuning. | Le das 2-3 ejemplos de clasificación: "Spam: ..., No spam: ..., Ahora clasifica este: [texto]" |
| **Embeddings** | Son representaciones numéricas (vectores) que capturan el significado de un texto. Textos con significado similar tienen vectores "cercanos". | "perro" y "can" tienen vectores similares, mientras que "perro" y "coche" están lejos. Permite búsquedas por significado. |

---

### 3.2 — Temperature: elige el valor correcto

Para cada tarea, indica qué rango de temperature usarías (0.0–0.3 / 0.4–0.7 / 0.8–1.0) y por qué:

| Tarea | Temperature | ¿Por qué? |
|---|---|---|
| Extraer datos estructurados de un contrato legal. | **0.0 – 0.3** | Necesitas respuestas precisas, consistentes y objetivas. No quieres que el modelo "inventé" información. |
| Generar nombres creativos para un producto nuevo. | **0.8 – 1.0** | Necesitas máxima creatividad, respuestas originales y variadas. |
| Construir un asistente conversacional para atención al cliente. | **0.4 – 0.7** | Un punto intermedio: respuestas naturales pero manteniendo coherencia y precisión. |
| Clasificar tickets de soporte como urgente / normal / spam. | **0.0 – 0.3** | Necesitas consistencia: el mismo tipo de ticket debe clasificarse igual siempre. |
| Escribir un poema sobre el mar. | **0.8 – 1.0** | Máxima creatividad poeticista, metáforas originales, variaciones interesantes. |
| Generar código Python que sume dos números. | **0.0 – 0.3** | Necesitas código preciso y correcto. No quieres que el modelo "cree" soluciones incorrectas. |

---

### 3.3 — Tokens: la moneda de las APIs

Responde las siguientes preguntas sobre tokens:

| Pregunta | Tu respuesta |
|---|---|
| **¿Qué es un token exactamente?** | Es la unidad mínima de texto que el modelo procesa. Puede ser una palabra completa, una sílaba, o parte de una palabra. Es la "moneda" que se consume en cada llamada a la API. |
| **¿Por qué los textos en español consume más tokens que en inglés?** | Porque el español es un idioma más "compactado": tiene palabras más largas y más caracteres por palabra. El inglés promedio tiene ~4 caracteres por token, mientras que español tiene ~1.5 caracteres por token. |
| **¿Cuántos tokens equivale aproximadamente un párrafo de 100 palabras?** | Aproximadamente **130–150 tokens**. |
| **¿Qué pasa si tu conversación supera la context window del modelo?** | El modelo comienza a **olvidar las partes más antiguas** de la conversación. Es como hablar con alguien de mala memoria: si le cuentas algo largo, al final habrá olvidado el principio. |
| **¿En qué se diferencia `max_tokens` del context window?** | **Context window** = cuántos tokens puede **recibir** (input) y "recordar" en total. **Max tokens** = cuántos tokens puede **generar** como salida. Son independientes: puedes tener context window de 128K pero limitar la respuesta a 100 tokens. |

---

## BLOQUE 4 — ¿Qué puedes construir con estas APIs? (4.4)

Relaciona cada tipo de aplicación con el proveedor más adecuado y escribe un caso de uso real:

| Tipo de aplicación | Proveedor más adecuado | Caso de uso real |
|---|---|---|
| **Chatbot inteligente** | OpenAI / Azure OpenAI | Un asistente virtual que explica código, resuelve errores y ayuda a navegar una plataforma de programación. |
| **Resumen de documentos** | Anthropic (Claude) | Resumir un PDF de 40 páginas en 5 puntos clave, extraer acuerdos de actas de reuniones, sintetizar informes médicos. |
| **Clasificación y análisis de texto** | OpenAI (GPT-4o-mini) | Clasificar tickets de soporte por urgencia, analizar sentiment de encuestas, categorizar emails como spam/no spam. |
| **Búsqueda semántica** | Cohere / OpenAI (embeddings) | Buscar "documentos sobre seguridad" y encontrar textos que hablen de ciberseguridad aunque no usen esas palabras exactas. |
| **Análisis de imágenes** | Google AI (Gemini) / OpenAI (GPT-4o) | Validar si una imagen contiene un DNI válido, analizar radiografías, describir imágenes para personas con discapacidad visual. |
| **Traducción contextual** | OpenAI / Google AI (Gemini) | Traducir documentación técnica manteniendo el tono formal y la precisión terminológica. |
| **Predicción de datos** | AWS Bedrock / Google AI | Predecir qué usuarios podrían abandonar un servicio, anticipar demanda de productos, detectar anomalías. |
| **Aplicación multimodal (texto + imagen)** | Google AI (Gemini) / OpenAI (GPT-4o) | Sistema que recibe una foto de producto, extrae texto, lo traduce, genera descripción y publica en redes sociales automáticamente. |

---

## BLOQUE 5 — Pregunta de síntesis

> *Un compañero/a dice: "Las APIs de IA son demasiado caras para usarlas en proyectos reales, mejor entreno mi propio modelo." ¿Estás de acuerdo? Razona tu respuesta con al menos dos argumentos concretos apoyándote en lo visto en los 4 bloques de este ejercicio:*

> **NO estoy de acuerdo.** Los argumentos son:
>
> 1. **Las APIs de IA son extremadamente económicas**: Como vimos en el Bloque 4 (precios), un chatbot con 100 consultas al día cuesta menos de $1 al mes. El coste por token es tan bajo (GPT-4o-mini: $0.002/1K tokens) que para la mayoría de aplicaciones el gasto es mínimo. Entrenar un modelo propio requiere GPUs caras, datos masivos y meses de trabajo.
>
> 2. **Las APIs abstraen toda la complejidad**: No necesitas entrenar, mantener ni desplegar modelos propios (BLOQUE 1). Es como contratar especialistas ya formados en lugar de entrenar un equipo desde cero. El desarrollo es mucho más rápido y el mantenimiento es casi nulo.
>
> 3. **Modelos económicos para tareas simples**: Para proyectos reales, no necesitas el modelo más potente. GPT-4o-mini es 20 veces más barato que GPT-4o y suficiente para tareas como clasificación, resúmenes simples, chatbots educativos.
>
> 4. **Flexibilidad de proveedor**: Si un proveedor resulta caro, puedes cambiar a otro (Hugging Face, Mistral, Gemini) sin cambiar tu código. Los modelos open-source están disponibles.
>
> **Conclusión**: Las APIs son la opción más práctica y económica para la mayoría de proyectos. Entrenar tu propio modelo solo tiene sentido si necesitas algo muy específico que no exista, o si tienes requisitos estrictos de privacidad (ejecutar on-premise).

---

*Módulo 4 · APIs de IA — Fundamentos y Proveedores · Dicampus*
