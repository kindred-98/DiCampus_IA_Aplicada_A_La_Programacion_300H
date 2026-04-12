# Reflexión Individual – StockGuard

**Autor:** Angel Echenique  
**Fecha:** 07/04/2026

## 8.1 — Inventario de uso de IA

Para cada archivo donde usé IA, describo el prompt principal que utilicé y los cambios que realicé sobre el código generado.

| Archivo | Prompt principal que usaste | Cambios que hiciste tú |
|---------|----------------------------|------------------------|
| **validator.py** | *"Genera dos funciones, validate_qty y validate_price, con docstring estilo Google, type hints, que lancen TypeError si el tipo no es correcto y devuelvan True si el valor es positivo, False en caso contrario."* | La IA generó las funciones con los mensajes de error en inglés. Yo los cambié a español para que fueran más claros en el contexto del proyecto. Además, añadí ejemplos específicos en los docstrings y ajusté el manejo de `float` para que aceptara tanto `int` como `float` sin conversiones forzadas. |
| **storage.py** | *"Escribe un módulo storage.py con funciones load_inventory y save_inventory. load_inventory debe manejar FileNotFoundError y JSONDecodeError devolviendo lista vacía. save_inventory debe guardar con indent=2. Incluye docstrings."* | La IA propuso un código que solo capturaba `JSONDecodeError`. Yo añadí un bloque `except Exception` genérico para cualquier otro error (permisos, disco lleno, etc.) y también agregué `encoding='utf-8'` a la apertura de archivos para evitar problemas con caracteres especiales. Además, completé los ejemplos de los docstrings. |
| **test_storage.py** | *"Crea tests con pytest-mock para simular json.load() lanzando JSONDecodeError y verificar que load_inventory devuelve lista vacía. También test de archivo inexistente y de guardado con indentación."* | La IA usó `pytest-mock` directamente (el decorador `mocker`). Yo decidí no usar `pytest-mock` porque preferí `unittest.mock.patch` para mantener la coherencia con otros tests. Modifiqué todos los tests para usar `patch` y `mock_open`. También eliminé la importación de `pytest` que la IA había incluido pero no se usaba, y añadí un test extra para excepciones genéricas. |
| **ci.yml** | *"Genera un pipeline de GitHub Actions para un proyecto Python 3.12 con pytest y flake8. Debe ejecutarse en push y pull_request sobre main."* | La IA generó un pipeline básico con `python-version: '3.x'`. Yo cambié a la versión exacta `3.12`, añadí `--max-line-length=100` al comando de flake8 y agregué `--statistics` para que diera más información. También incluí el paso de actualizar `pip` antes de instalar dependencias. |

# Reflexión Individual – StockGuard

## 8.2 — Análisis de la vulnerabilidad

**Explica con tus propias palabras: ¿qué riesgo real tendría permitir qty o price negativos en un sistema de inventario en producción? ¿Cómo lo mitigaste en este ejercicio?**

### Riesgo real de permitir qty o price negativos en producción

En un sistema de inventario real, permitir cantidades negativas rompe por completo la lógica de negocio. Imagina un almacén donde se registran ventas y reposiciones. Si un empleado introduce por error `-5` unidades, el sistema mostraría un stock negativo, lo que no tiene sentido físico. Eso podría ocultar problemas reales como roturas, robos o errores de conteo. Además, si el sistema se integra con un ERP financiero, el valor total del inventario (`qty * price`) podría volverse negativo, generando informes contables erróneos y potencialmente decisiones de compra o venta equivocadas.

Por otro lado, permitir precios negativos es aún más grave. Un atacante o un usuario malintencionado podría introducir productos con precio `-100€`, lo que haría que el valor total del inventario disminuyera artificialmente, pudiendo manipular balances o incluso generar órdenes de compra absurdas (el sistema podría "regalar" dinero si se integra con pagos). En el peor de los casos, si el sistema se usa para facturación, un precio negativo podría generar abonos automáticos no deseados.

### Cómo lo mitigué en este ejercicio

- Creé un modelo de datos (`Item` dataclass) con `__post_init__` que lanza `ValueError` si `qty <= 0` o `price <= 0`. Esto asegura que nunca se pueda instanciar un producto inválido.
- Implementé las funciones `validate_qty` y `validate_price` en `validator.py`, que son llamadas desde `add_item` y `update_price` antes de guardar cualquier cambio.
- En `stockguard.py` (modificado), si la validación falla, se lanza una excepción y no se persiste el dato.
- Los tests unitarios verifican que estas validaciones funcionan correctamente, incluyendo casos borde.

De esta forma, cualquier intento de introducir valores no positivos es rechazado inmediatamente.

## 8.3 — Reflexión sobre el pipeline CI

**¿Por qué es útil ejecutar los tests automáticamente en cada push y no solo en local? Razona con una situación concreta de este ejercicio.**

Ejecutar los tests en local es necesario durante el desarrollo, pero no es suficiente porque diferentes entornos pueden dar resultados distintos (versiones de Python, dependencias, sistema operativo, etc.). Además, los desarrolladores pueden olvidar ejecutar los tests antes de hacer push.

Un caso concreto ocurrió en este ejercicio: cuando corregí los errores de `flake8` localmente, todo pasaba en mi máquina con Windows. Sin embargo, al hacer push, el pipeline en GitHub Actions (Ubuntu Linux) detectó un error que yo no había visto: un `import pytest` no usado en `test_storage.py` que `flake8` en Windows no había señalado (aunque debería, pero a veces hay diferencias de versión). El pipeline falló, y eso me obligó a revisar y corregir el código. Sin el pipeline, ese import muerto habría llegado al repositorio y podría causar confusión a otro desarrollador o incluso un warning innecesario.

Otro ejemplo: si un compañero de equipo modificara `storage.py` y rompiera el manejo de `JSONDecodeError`, el pipeline lo detectaría inmediatamente al hacer push, sin necesidad de que yo me enterara días después. Así el pipeline actúa como una red de seguridad que garantiza que el código siempre esté en un estado mínimo de calidad (tests pasando y estilo correcto) antes de integrarse.

Además, el pipeline proporciona un **informe público y automático** (el badge verde/rojo) que cualquier miembro del equipo puede consultar, fomentando la transparencia y la disciplina de calidad.

---

## 8.4 — ¿Cuándo NO usar IA?

**Describe un momento durante el ejercicio en el que decidiste NO usar la IA y lo resolviste tú. ¿Por qué lo hiciste así?**

Durante el ejercicio, decidí **no usar la IA para diseñar los casos borde (edge cases) de los tests**. Por ejemplo, en `test_models.py` la IA podía haberme dado casos como `qty=0.001` o `price=10**6`, pero preferí pensar yo mismo en situaciones límite. Razoné que un producto podría tener un precio muy pequeño (0.0001€) en sistemas de microtransacciones, o una cantidad enorme (2^31-1) para inventarios masivos. También se me ocurrió probar `price=1e-10` para ver si la validación con `float` funcionaba correctamente.

**¿Por qué lo hice sin IA?** Porque quería entrenar mi propio criterio como QA. Los casos extremos son donde suelen fallar los sistemas, y confiar ciegamente en la IA para generarlos me habría privado de aprender a pensar en condiciones límite. 

Otro momento fue al corregir la estructura anidada de carpetas. La IA me habría dado el comando `Move-Item` probablemente, pero preferí entender por qué ocurría el error y resolverlo manualmente mirando el `tree /F`. Eso me ayudó a comprender cómo Python interpreta los paquetes y la importancia de `__init__.py`. Usar IA habría sido más rápido, pero menos formativo.

En resumen, **no uso IA cuando quiero consolidar un concepto fundamental** o cuando el ejercicio valora específicamente mi capacidad de análisis y creatividad. La IA es una herramienta, no un sustituto del pensamiento crítico..

---

