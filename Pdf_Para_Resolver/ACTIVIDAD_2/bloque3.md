 Código equivalente en ambos lenguajes

 Python

 from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': 'Eres un asistente experto.'},
        {'role': 'user', 'content': '¿Qué es un token?'}
    ],
    temperature=0.3,
    max_tokens=500
)

print(response.choices[0].message.content)


JavaScript (Node.js)

import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const response = await client.chat.completions.create({
  model: 'gpt-4o-mini',
  messages: [
    { role: 'system', content: 'Eres un asistente experto.' },
    { role: 'user', content: '¿Qué es un token?' }
  ],
  temperature: 0.3,
  max_tokens: 500
});

console.log(response.choices[0].message.content);ç


🔑 Diferencias clave resumidas
Diferencia	Python	JavaScript
Sintaxis de importación	from module import Class	import { Class } from "module"
Inicialización de cliente	OpenAI(api_key=...)	new OpenAI({ apiKey: ... })
Variables de entorno	os.getenv("KEY")	process.env.KEY
Ejecución	Síncrono por defecto	Siempre async/await
Uso principal	Backend, scripts, data	Frontend, Node.js, APIs web