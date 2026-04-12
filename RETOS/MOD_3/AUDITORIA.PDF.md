# Auditoría de vulnerabilidades - StockGuard

**Fecha:** 06/04/2026  
**Auditor:** Angel Echenique

## Resumen
Se ha analizado el archivo `stockguard.py` (código heredado). 
Se identificaron **tres vulnerabilidades críticas** que afectan a la integridad de los datos, la robustez del sistema y la mantenibilidad del proyecto.

---

## Vulnerabilidad 1: Ausencia de validación de entrada (qty y price negativos)

### Descripción
Las funciones `add_item(name, qty, price)` y `update_price(name, new_price)` no realizan ninguna comprobación sobre los valores de cantidad y precio. 

Se permite almacenar:
- Cantidades negativas (ej. `-10` unidades)
- Precios negativos o cero (ej. `0€`, `-5€`)

### Riesgo real en producción
- **Inventario inconsistente**: Stock negativo no tiene sentido físico y rompe la lógica de negocio (ej. ventas, reposiciones).
- **Valoración económica erróta**: `get_total_value()` multiplica cantidad negativa por precio, dando resultados incorrectos (pérdidas ficticias o valores negativos).
- **Posible explotación maliciosa**: Un usuario podría introducir precios negativos para manipular informes financieros.

### Propuesta de corrección
- Crear un módulo `validator.py` con funciones `validate_qty(qty: int) -> bool` y `validate_price(price: float) -> bool`.
- Lanzar `ValueError` si los valores no son válidos (positivos y mayores que cero).
- Integrar las validaciones dentro de `add_item()` y `update_price()` **antes** de guardar en el inventario.

---

## Vulnerabilidad 2: Sin manejo de errores al leer JSON corrupto

### Descripción
La función `load_inventory()` abre el archivo `inventory.json` y llama directamente a `json.load(f)` sin capturar excepciones. Si el archivo está dañido (JSON mal formado) o vacío, se produce un `JSONDecodeError` que detiene el programa por completo.

### Riesgo real en producción
- **Indisponibilidad del sistema**: El script crashea cada vez que el archivo JSON está corrupto, impidiendo cargar el inventario.
- **Pérdida de datos**: No hay mecanismo de recuperación ni respaldo automático.
- **Mala experiencia de usuario**: El programa se cierra sin un mensaje claro.

### Propuesta de corrección
- Crear un nuevo módulo `storage.py` que maneje:
  - `FileNotFoundError` → devolver lista vacía (primer ejecución).
  - `JSONDecodeError` → registrar error y devolver lista vacía (o intentar recuperar desde backup).
- Añadir `indent=2` en `save_inventory()` para facilitar la depuración manual.
- Documentar el comportamiento con docstrings.

---

## Vulnerabilidad 3: Ausencia total de tests y documentación

### Descripción
El proyecto no contiene ningún test (unitario, de integración, etc.) ni documentación técnica. No hay docstrings en las funciones, ni README, ni archivo de requisitos.

### Riesgo real en producción
- **Mantenimiento imposible**: Cualquier cambio, incluso pequeño, puede introducir regresiones sin que nadie lo detecte.
- **Falta de calidad**: No se puede medir la cobertura ni verificar que el código sigue funcionando tras refactorizaciones.
- **Dependencia del autor original**: Solo quien escribió el código sabe cómo debería comportarse.

### Propuesta de corrección
- Escribir tests unitarios con `pytest` y `pytest-mock` para:
  - Validaciones (`test_validator.py`)
  - Modelo de datos (`test_models.py`)
  - Persistencia (`test_storage.py`) simulando el sistema de archivos.
- Añadir docstrings estilo Google a **todas** las funciones públicas.
- Crear un pipeline CI/CD en GitHub Actions que ejecute los tests y linters automáticamente en cada `push`.

---

## Conclusión
Las tres vulnerabilidades son críticas y deben corregirse en el orden propuesto. 
La corrección completa se realizará en las siguientes fases del ejercicio, respetando el plan de 12 commits que mando Rusgar.


