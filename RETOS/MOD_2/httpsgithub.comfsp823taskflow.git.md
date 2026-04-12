# 📋 TaskFlow CLI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-yellow?style=for-the-badge)

**Gestor de tareas ligero y extensible para la terminal**

</div>

---

## 📖 Descripción

**TaskFlow CLI** es un gestor de tareas en consola escrito en **Python 3.12+**.
 Su objetivo es ofrecer una herramienta ligera, extensible y fácil de usar para crear, listar y gestionar tareas desde la terminal.

El proyecto crece de forma incremental: comienza con una estructura mínima y evoluciona hacia una aplicación completa con modelos de datos, persistencia en JSON, lógica de negocio, colores en la CLI y una batería de tests automatizados.

---

## 📁 Estructura del proyecto
```
taskflow/
├── taskflow/
│   ├── __init__.py
│   ├── cli.py          # Interfaz de línea de comandos
│   ├── logic.py        # Lógica de negocio
│   ├── models.py       # Modelos de datos
│   └── storage.py      # Persistencia en JSON
├── tests/
│   ├── test_logic.py
│   ├── test_models.py
│   └── test_storage.py
├── tasks.json
├── requirements.txt
└── README.md
```

---

## 🚀 Instalación

> Asegúrate de tener **Python 3.12 o superior** instalado.

**1. Clona el repositorio:**
```bash
git clone https://github.com/fsp823/taskflow.git
cd taskflow
```

**2. Instala las dependencias:**
```bash
pip install -r requirements.txt
```

### 📦 Dependencias incluidas

| Paquete | Descripción |
|---------|-------------|
| [Typer](https://typer.tiangolo.com/) | Interfaz de línea de comandos |
| [Rich](https://rich.readthedocs.io/) | Salida con colores y tablas |
| [pytest](https://pytest.org/) | Ejecución de tests automatizados |

---

> 💡 También puedes instalarlas manualmente:
```bash
pip install typer>=0.9 rich>=13 pytest>=8
```

## ▶️ Uso

Ejecuta la CLI directamente con Python:
```bash
python -m taskflow.cli hello
```

**Ejemplo:**
```bash
python -m taskflow.cli hello TaskFlow
```

**Salida esperada:**
```
Hola TaskFlow 👋
```

---

## 🧪 Tests

Para ejecutar la batería de tests:
```bash
pytest
```

O con más detalle:
```bash
pytest -v
```

---

## 👥 Equipo

| Nombre | GitHub |
|--------|--------|
| Ernesto | [@ernesto](https://github.com/ernestoSotero) |
| Angel | [@Angel](https://github.com/Kindred-98) |
| Fernando | [@Fernando](https://github.com/FSP823) |
| Alberto | [@Alberto](https://github.com/RFireforge) |
| Raul  | [@Raul](https://github.com/Ralfy) |

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.