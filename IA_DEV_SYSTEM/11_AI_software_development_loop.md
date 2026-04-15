# 🔁 AI Software Development Loop

> Flujo de trabajo profesional para desarrollar software con IA.
> Usa la IA como arquitecto, desarrollador, tester y reviewer al mismo tiempo.

---

## El ciclo completo

```
IDEA
 ↓
ARQUITECTURA
 ↓
PLAN
 ↓
CÓDIGO
 ↓
REVIEW
 ↓
OPTIMIZACIÓN
 ↓
SIGUIENTE FEATURE  →  vuelve al inicio
```

---

## ⚡ Paso 0 — Anti-errores (añadir siempre)

Antes de cualquier prompt de código, incluye esto.
Mejora drásticamente la calidad del resultado.

```
Antes de escribir código:

1. analiza el problema
2. propone arquitectura
3. explica decisiones técnicas
4. luego genera el código
```

---

## 1️⃣ Definir el problema

```
Actúa como arquitecto de software.

Estoy desarrollando una aplicación en Python.

Funcionalidad que quiero crear:
[explica la funcionalidad]

Define:

1. objetivo
2. posibles enfoques
3. complejidad técnica
4. solución recomendada
```

---

## 2️⃣ Diseñar la arquitectura

```
Diseña la arquitectura para implementar esta funcionalidad.

Incluye:
- módulos necesarios
- flujo de datos
- responsabilidades de cada módulo
```

---

## 3️⃣ Planificar el desarrollo

```
Divide esta funcionalidad en tareas pequeñas.

Cada tarea debe ser un módulo o función implementable.
```

Ejemplo de resultado esperado:
```
1. crear función de lectura de texto
2. crear función de conteo de palabras
3. crear función de frecuencia
4. crear exportador de resultados
```

---

## 4️⃣ Implementar

```
Implementa esta tarea en Python:
[tarea]

Requisitos:
- código limpio
- tipado
- manejo de errores
- docstrings
```

---

## 5️⃣ Revisar y testear

**Code review:**
```
Actúa como code reviewer senior.

Revisa este código Python.

Detecta:
- bugs
- malas prácticas
- problemas de rendimiento
```

**Testing:**
```
Genera tests usando pytest para este módulo.
```

---

## 6️⃣ Optimizar

```
Optimiza este código Python.

Busca:
- mejoras de rendimiento
- simplificación de lógica
- mejor arquitectura
```

---

## 📦 Ejemplo real — Contador de palabras

| Paso | Acción |
|------|--------|
| 1 | "Quiero crear una función que analice un texto y devuelva estadísticas" |
| 2 | IA propone: `text_loader.py`, `text_analyzer.py`, `exporter.py` |
| 3 | IA divide: leer archivo → limpiar texto → contar palabras → calcular frecuencia |
| 4 | Generas código módulo a módulo |
| 5 | IA revisa y crea tests con pytest |
| 6 | IA optimiza funciones |

---

## 🗂️ AI_DEV_WORKFLOW — Checklist rápido

Guárdalo y úsalo en cada feature nueva.

```
[ ] 1. Definir funcionalidad
[ ] 2. Diseñar arquitectura
[ ] 3. Dividir en tareas
[ ] 4. Implementar módulo a módulo
[ ] 5. Revisar código
[ ] 6. Crear tests
[ ] 7. Optimizar
```
