# 🐍 Pipeline de Prompts — Desarrollo de Apps Python con IA

> Estructura profesional de prompts para desarrollar aplicaciones Python desde la idea hasta producción.

---

## 📋 Flujo general

```
PROMPT 1  →  Definir el proyecto
PROMPT 2  →  Diseñar arquitectura
PROMPT 3  →  Crear roadmap
PROMPT 4  →  Estructura del proyecto
PROMPT 5  →  Generar código por módulos
PROMPT 6  →  Testing
PROMPT 7  →  Optimización
PROMPT 8  →  Seguridad
PROMPT 9  →  Docker
PROMPT 10 →  Despliegue
```

---

## 🧱 Plantilla base (usar siempre)

```
CONTEXTO
Estoy desarrollando una aplicación en Python.

OBJETIVO
Quiero crear [tipo de aplicación].

REQUISITOS
- lenguaje: Python
- framework: [Flask / FastAPI / Django / CLI / etc]
- base de datos: [si aplica]
- tipo de arquitectura: [MVC, modular, clean architecture]

TAREA
Necesito que generes [lo que pides].

FORMATO DE RESPUESTA
- Explicación breve
- Código completo
- Estructura clara
- Buenas prácticas
```

---

## 🚀 Prompt Maestro (ejecutar primero)

```
Quiero que actúes como:

- arquitecto de software
- desarrollador senior de Python
- experto en buenas prácticas

Estoy desarrollando una aplicación completa en Python.

Tu objetivo será ayudarme a diseñarla, desarrollarla, testearla
y prepararla para producción paso a paso.

No avances a la siguiente fase hasta que yo lo indique.
```

---

## PROMPT 1 — Definición del proyecto

```
Actúa como un arquitecto de software senior.

Quiero desarrollar una aplicación en Python desde cero.

La aplicación es:
[explica tu idea]

Necesito que me ayudes a definir:

1. Objetivo del proyecto
2. Funcionalidades principales
3. Usuarios del sistema
4. Tecnologías recomendadas
5. Riesgos técnicos

Devuelve la respuesta estructurada.
```

---

## PROMPT 2 — Arquitectura del sistema

```
Actúa como arquitecto de software.

Con base en este proyecto:
[descripcion del proyecto]

Define:

1. Arquitectura recomendada
2. Patrones de diseño
3. Estructura de carpetas
4. Flujo de datos
5. Componentes principales

La aplicación será desarrollada en Python.

Devuelve diagramas en texto y explicación clara.
```

---

## PROMPT 3 — Roadmap de desarrollo

```
Actúa como tech lead.

Crea un roadmap para desarrollar este proyecto en Python.

El roadmap debe incluir:

Fase 1 – Configuración del proyecto
Fase 2 – Desarrollo del core
Fase 3 – Integración de base de datos
Fase 4 – API / interfaz
Fase 5 – Testing
Fase 6 – Optimización
Fase 7 – Despliegue

Cada fase debe tener:
- tareas
- objetivos
- resultado esperado
```

---

## PROMPT 4 — Estructura del proyecto

```
Genera la estructura profesional de carpetas para este proyecto en Python.

Debe incluir:
- src
- tests
- config
- scripts
- docs

También incluye:
- requirements.txt
- README.md
- .env
- .gitignore

Devuelve la estructura tipo árbol.

Ejemplo:

project/
├── app
│   ├── routes
│   ├── services
│   ├── models
│   └── utils
├── tests
├── config
├── requirements.txt
├── README.md
└── main.py
```

---

## PROMPT 5 — Desarrollo de módulos

```
Actúa como desarrollador Python senior.

Estamos desarrollando este proyecto:
[descripcion]

Ahora quiero implementar el módulo:
[modulo]

Requisitos:
- código limpio
- tipado
- comentarios
- manejo de errores

Devuelve:
1. explicación
2. código completo
```

---

## PROMPT 6 — Testing

```
Genera tests para este módulo de Python usando pytest.

El test debe incluir:
- tests unitarios
- tests de errores
- casos límite

Explica cada test.
```

---

## PROMPT 7 — Optimización

```
Analiza este código Python.

Identifica:

1. problemas de rendimiento
2. problemas de escalabilidad
3. mejoras de arquitectura

Propón mejoras y muestra el código optimizado.
```

---

## PROMPT 8 — Seguridad

```
Actúa como experto en seguridad de aplicaciones.

Analiza este proyecto Python y detecta:
- vulnerabilidades
- problemas de autenticación
- manejo inseguro de datos

Propón soluciones.
```

---

## PROMPT 9 — Dockerización

```
Genera todo lo necesario para dockerizar esta aplicación Python.

Incluye:
- Dockerfile
- docker-compose
- variables de entorno
- instrucciones de ejecución
```

---

## PROMPT 10 — Despliegue

```
Explica cómo desplegar esta aplicación Python en producción.

Incluye:
- servidor recomendado
- configuración
- CI/CD
- monitorización
```
