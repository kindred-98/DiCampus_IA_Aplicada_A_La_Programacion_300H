# Proyecto StockGuard - Informe completo de desarrollo

**Autor:** Angel Echenique  
**Fecha:** 07/04/2026  
**Repositorio:** https://github.com/kindred-98/StockGuard

## Índice

1. [Descripción del proyecto](#descripción-del-proyecto)
2. [Estructura final del repositorio](#estructura-final-del-repositorio)
3. [Fase 1: Estructura y código de partida](#fase-1-estructura-y-código-de-partida)
4. [Fase 2: Modelo de datos y validación](#fase-2-modelo-de-datos-y-validación)
5. [Fase 3: Tests con pytest y mocks](#fase-3-tests-con-pytest-y-mocks)
6. [Fase 4: Pipeline GitHub Actions](#fase-4-pipeline-github-actions)
7. [Fase 5: Documentación y cierre](#fase-5-documentación-y-cierre)
8. [Mejoras adicionales implementadas](#mejoras-adicionales-implementadas)
9. [SonarCloud - Análisis de Calidad](#sonarcloud---análisis-de-calidad)
10. [Problemas encontrados y soluciones](#problemas-encontrados-y-soluciones)
11. [Reflexión final](#reflexión-final)

---

## Descripción del proyecto

StockGuard es un sistema de gestión de existencias en Python 3.12+. El código inicial (`stockguard.py`) contenía tres vulnerabilidades críticas:

1. **Falta de validación de entrada**: permitía cantidades negativas y precios ≤ 0.
2. **Sin manejo de JSON corrupto**: si `inventory.json` estaba dañado, el programa crasheaba.
3. **Ausencia total de tests y documentación**.

El objetivo era auditar, documentar, testear y proteger el código con un pipeline CI/CD, siguiendo un plan de 12 commits.

---

## Estructura final del repositorio

```
StockGuard/
├── .gitignore
├── requirements.txt
├── README.md
├── LICENSE
├── .pre-commit-config.yaml
├── sonar-project.properties
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── security.yml
│
├── stockguard/
│   ├── __init__.py
│   ├── models.py
│   ├── stockguard.py
│   ├── storage.py
│   └── validator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_storage.py
│   ├── test_validator.py
│   └── test_stockguard.py
│
└── docs/
    ├── Auditoria.md
    ├── Resolucion_del_Bloque8.md
    ├── PIPELINES_EXPLICACION.md
    └── Inf_Completo-Desarrollo.md
```

---

## Fase 1: Estructura y código de partida

### Commit 01: `chore: init repo y .gitignore`

**Acciones:**
- Crear repositorio público en GitHub.
- Clonar localmente.
- Crear `.gitignore` con:
  ```
  __pycache__/
  .venv/
  *.pyc
  inventory.json
  ```
- Commit y push inicial.

### Commit 02: `chore: estructura de carpetas [ai]`

**Acciones:**
- Crear carpetas `stockguard/` y `tests/`.
- Añadir `__init__.py` vacío en cada una.
- Copiar `stockguard.py` original dentro de `stockguard/`.
- Crear `requirements.txt`:
  ```
  pytest>=8
  pytest-mock>=3
  flake8>=7
  ```

**Problema encontrado:** Inicialmente se creó una estructura anidada (`stockguard/stockguard/`). Se corrigió moviendo archivos.

### Commit 03: `docs: auditoría de vulnerabilidades [ai]`

**Archivo:** `docs/AUDIT.md`

**Contenido:**
- **Vulnerabilidad 1:** Entrada sin validación (riesgo de stock negativo).
- **Vulnerabilidad 2:** JSON corrupto (caída del sistema).
- **Vulnerabilidad 3:** Falta de tests y documentación (mantenimiento imposible).

Se redactó con ayuda de IA pero con conclusiones propias.

---

## Fase 2: Modelo de datos y validación

### Commit 04: `feat: dataclass Item en models.py [ai]`

**Archivo:** `stockguard/models.py`

```python
@dataclass
class Item:
    name: str
    qty: int
    price: float

    def __post_init__(self) -> None:
        if self.qty <= 0:
            raise ValueError(f"La cantidad debe ser positiva, recibido: {self.qty}")
        if self.price <= 0:
            raise ValueError(f"El precio debe ser positivo, recibido: {self.price}")

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "qty": self.qty, "price": self.price}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Item":
        return cls(name=data["name"], qty=data["qty"], price=data["price"])
```

**Nota:** Se añadieron métodos `to_dict`/`from_dict` para facilitar persistencia.

### Commit 05: `feat: validator.py con validate_qty y validate_price [ai]`

**Archivo:** `stockguard/validator.py`

Funciones con docstring Google, type hints y lanzamiento de TypeError si el tipo es incorrecto:

```python
def validate_qty(qty: int) -> bool:
    if not isinstance(qty, int):
        raise TypeError(f"qty debe ser int, recibido {type(qty)}")
    return qty > 0
```

**Integración en stockguard.py:** Se modificó el código original para importar y usar estas validaciones en `add_item` y `update_price`.

### Commit 06: `feat: storage.py con manejo de errores [ai]`

**Archivo:** `stockguard/storage.py`

- `load_inventory()` captura JSONDecodeError, FileNotFoundError y cualquier otra excepción, devolviendo lista vacía.
- `save_inventory()` escribe con `indent=2` y `ensure_ascii=False`.
- Docstrings completos en todas las funciones.

---

## Fase 3: Tests con pytest y mocks

### Commit 07: `test: test_models.py [ai]`

**Archivo:** `tests/test_models.py`

- Tests de creación válida.
- Tests de ValueError para qty=0, qty negativo, price=0, price negativo.
- Edge cases: cantidad muy grande (2^31-1), precio muy pequeño (0.0001).

### Commit 08: `test: test_validator.py [ai]`

**Archivo:** `tests/test_validator.py`

- Tests para valores válidos y no válidos (False).
- Tests de TypeError con tipos incorrectos.
- Edge cases: cantidad enorme, precio muy pequeño y muy grande.

### Commit 09: `test: test_storage.py [ai]`

**Archivo:** `tests/test_storage.py`

Uso de `unittest.mock.patch` para simular:
- Archivo inexistente.
- JSON corrupto.
- Excepción genérica.
- Guardado con indentación correcta.

---

## Fase 4: Pipeline GitHub Actions

### Commit 10: `feat: .github/workflows/ci.yml [ai]`

**Archivo:** `.github/workflows/ci.yml`

```yaml
name: StockGuard CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: flake8 stockguard/ tests/ --max-line-length=100
      - run: pytest tests/ -v --cov=stockguard --cov-report=xml
```

### Commit 11: `test: verificar pipeline en GitHub Actions`

Acción: Commit para forzar la ejecución del pipeline. Se verificó en la pestaña Actions que el workflow termina en verde.

---

## Fase 5: Documentación y cierre

### Commit 12: `docs: README final y reflexión IA [ai]`

**Archivo:** `README.md`

Contiene:
- Badge del pipeline CI.
- Badge de Security Audit.
- Badge de Coverage.
- Instalación y uso.
- Explicación de los tests.
- Tabla de uso de IA.

---

## Mejoras adicionales implementadas

| Mejora | Descripción | Archivo |
|--------|-------------|---------|
| Pipeline Security | Escaneo con Bandit | `.github/workflows/security.yml` |
| pytest-cov | Coverage ≥80% | `requirements.txt` |
| Pre-commit hooks | flake8 + black | `.pre-commit-config.yaml` |
| Tests stockguard.py | 8 tests adicionales | `tests/test_stockguard.py` |
| SonarCloud | Análisis de calidad | Pipeline CI + `sonar-project.properties` |

### Los 3 Pipelines de StockGuard

Este proyecto implementa **3 pipelines automatizados** que trabajan juntos:

```
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS                               │
├─────────────────┬─────────────────┬─────────────────────────────┤
│      CI         │    SECURITY     │     SONARCLOUD              │
│  (ci.yml)       │ (security.yml)  │    (integrado en CI)        │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ • flake8        │ • Bandit        │ • Análisis estático         │
│ • pytest        │ • Escaneo       │ • Métricas de calidad       │
│ • coverage      │   de seguridad  │ • Debt técnico              │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

#### Pipeline 1: CI (Continuous Integration)

**Propósito**: Verificar que el código funciona y cumple el estilo

**Herramientas**:
- **flake8**: Verifica estilo de código
- **pytest**: Ejecuta tests unitarios
- **coverage**: Mide cobertura de código
- **SonarCloud**: Análisis de calidad

**Cuándo se ejecuta**: Push o PR a `main`

#### Pipeline 2: Security

**Propósito**: Detectar vulnerabilidades de seguridad

**Herramientas**:
- **Bandit**: Escanea código Python en busca de problemas de seguridad

**Qué detecta**:
- Contraseñas hardcodeadas
- Uso de funciones peligrosas
- Inyecciones de código
- Cryptography issues

#### Pipeline 3: SonarCloud

**Propósito**: Análisis profundo de calidad del código

**Qué analiza**:
- Bugs y errores potenciales
- Code Smells (código mejorable)
- Security Hotspots
- Deuda técnica
- Cobertura de tests
- Código duplicado

### Cómo interactúan

1. **Push/PR** → Se activan todos los pipelines
2. **CI** → Verifica que el código funcione
3. **Security** → Busca vulnerabilidades
4. **SonarCloud** → Analiza calidad técnica

**Todos deben pasar en verde** para considerar el código listo.

### Ejecutar localmente

```bash
# Verificar tests
pytest tests/ -v

# Verificar coverage
pytest tests/ --cov=stockguard --cov-report=term-missing

# Verificar estilo
flake8 stockguard/ tests/ --max-line-length=100

# Verificar seguridad
bandit -r stockguard/
```

### Pipeline Security (`.github/workflows/security.yml`)

```yaml
name: Security Audit
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  bandit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install bandit
      - run: bandit -r stockguard/ -f txt -o bandit_report.txt
      - uses: actions/upload-artifact@v4
        with:
          name: bandit-report
          path: bandit_report.txt
```

### Pre-commit hooks (`.pre-commit-config.yaml`)

```yaml
repos:
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  - repo: https://github.com/psf/black
    rev: 24.4.0
    hooks:
      - id: black
        args: ['--line-length=100']
```

---

## SonarCloud - Análisis de Calidad

### ¿Qué es SonarCloud?

SonarCloud es una plataforma de análisis de código estático en la nube que evalúa la calidad del código fuente. Se integra con GitHub Actions para proporcionar métricas automáticamente.

### ¿Qué analiza?

| Métrica | Descripción |
|---------|-------------|
| **Bugs** | Errores potenciales que pueden causar problemas |
| **Code Smells** | Código difícil de mantener o confuso |
| **Security Hotspots** | Zonas sensibles que requieren revisión |
| **Technical Debt** | Tiempo estimado para corregir problemas |
| **Coverage** | Porcentaje de código cubierto por tests |
| **Duplications** | Código duplicado que debería refactorizarse |

### Configuración

#### 1. Token de SonarCloud

1. Ve a **sonarcloud.io** e inicia sesión
2. Click en tu avatar → **My Account** → **Security**
3. Genera un token y cópialo

#### 2. Configurar en GitHub

1. Ve a tu repositorio → **Settings** → **Secrets and variables** → **Actions**
2. Añade un nuevo secret:
   - Name: `SONAR_TOKEN`
   - Value: El token que generaste

#### 3. Configuración del proyecto

**Archivo:** `sonar-project.properties`

```properties
sonar.projectKey=kindred-98_StockGuard
sonar.organization=kindred-98
sonar.projectName=StockGuard
sonar.projectVersion=1.0.0
sonar.sources=stockguard
sonar.tests=tests
sonar.python.version=3.12
sonar.sourceEncoding=UTF-8
```

#### 4. Desactivar Automatic Analysis

⚠️ **Importante**: Desactiva el análisis automático para evitar conflictos:

1. Ve a tu proyecto en SonarCloud
2. **Administration** → **Analysis Method**
3. Desactiva **Automatic Analysis**
4. Guarda

### Integración en CI

El análisis de SonarCloud está integrado en el pipeline CI (`.github/workflows/ci.yml`):

```yaml
- name: SonarCloud Scan
  uses: SonarSource/sonarqube-scan-action@v5.0.0
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Beneficios de usar SonarCloud

1. **Detección temprana**: Encuentra bugs antes de que lleguen a producción
2. **Mantenibilidad**: Identifica código difícil de mantener
3. **Seguridad**: Detecta vulnerabilidades de seguridad
4. **Technical Debt**: Muestra cuánto esfuerzo se necesita para mejorar
5. **Seguimiento**: Historial de métricas a lo largo del tiempo

---

## Problemas encontrados y soluciones

| Problema | Solución |
|----------|----------|
| Estructura anidada `stockguard/stockguard/` | Mover archivos y eliminar subcarpeta sobrante. |
| ModuleNotFoundError al importar | Asegurar `__init__.py` en cada paquete. |
| flake8 muestra errores (líneas en blanco) | Corregir manualmente cada archivo. |
| Test importaba pytest sin usarlo | Eliminar import, usar solo unittest.mock. |
| Pipeline fallaba por errores de linting | Corregir localmente antes del push. |
| Coverage bajo (52%) | Añadir tests para `stockguard.py` (coverage → 89%). |

---

## Reflexión final

El ejercicio ha permitido practicar todos los conceptos de calidad de software:
- **Auditoría**: Identificar vulnerabilidades en código heredado.
- **Validación de datos**: Implementar comprobaciones robustas.
- **Tests unitarios**: Con mocks y coverage.
- **Integración continua**: Pipeline CI/CD + Security.
- **Documentación**: Docstrings y READMEs.

La IA se utilizó como asistente para generar esqueletos y detectar vulnerabilidades, pero todo el código fue comprendido y ajustado manualmente. El pipeline CI garantiza que cualquier cambio futuro no rompa la funcionalidad existente.
