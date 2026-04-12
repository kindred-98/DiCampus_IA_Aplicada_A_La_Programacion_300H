# Requisitos del Sistema — PomodoroSecureTime

---

## 👔 SUPERVISOR

### Gestión de Equipos

| Funcionalidad | Descripción |
|--------------|-------------|
| **Agregar equipos vacíos** | El supervisor puede crear equipos sin miembros y luego asignar usuarios |
| **Buscar empleados** | Buscador para encontrar empleados por nombre |
| **Descansos fijos** | El supervisor define 2 puestos de descanso (no visible para empleados) |

### Estado de Empleados

| Funcionalidad | Descripción |
|--------------|-------------|
| **Ver conexión** | Mostrar si un empleado está conectado o no |
| **Dashboard de equipos** | Ver equipos organizados con nombre y rango de cada miembro |

---

## 🔐 CONTRASEÑA

### Cambio de Contraseña

| Funcionalidad | Descripción |
|--------------|-------------|
| **Campo repetir contraseña** | Agregar campo "Repetir contraseña" como en apps de mercado |
| **Ver contraseña actual** | Mostrar contraseña actual con el pin de 6 dígitos |
| **Generador de código pin** | Botón para generar código numérico de 6 dígitos |

---

## 👤 EMPLEADO

### Sesiones y Estado

| Problema | Requerimiento |
|----------|---------------|
| **Sesión activa tras 4 días** | La sesión no debe mantenerse activa si la app no se cerró correctamente |
| **Fin de jornada laboral** | Botón para finalizar jornada: reinicia pausas usadas, ciclos, horas trabajadas a 0 |
| **Reporte al supervisor/encargado** | Enviar reporte de fin de jornada |

### Comportamiento Esperado

- Al cerrar sesión manualmente: el contador puede seguir corriendo
- Al abrir la app de nuevo: debe continuar desde donde quedó
- Al presionar "Fin de jornada": tutto vuelve al inicio

---

## 👥 ENCARGADO

### Dashboard

| Funcionalidad | Descripción |
|--------------|-------------|
| **Ver minutos de trabajo** | Mostrar minutos restantes para descanso de 5 minutos (como en cybers) |
| **Ver equipo** | Ver miembros del equipo asignado |
| ** own dashboard** | Igual que empleado + apartado de equipos |

### Gestión de Equipos

- Los equipos **solo los organiza el supervisor**
- Al encargado le aparecen los equipos ya organizados
- Estructura: `Equipo: [Nombre] → [Empleado] - [Rango]`

---

## Ejemplo de Estructura de Equipos

```
📁 DEBUG
   ├─ Wally - Empleado
   └─ David - Encargado

📁 REVISION_CODIGO
   └─ Angel - Empleado

📁 FRONTEND
   └─ [Sin asignar]
```

---

## Cálculo de Tiempos (Supervisor)

| Acción | Descripción |
|--------|-------------|
| **Login** | Inicia contador de trabajo |
| **Logout** | Inicia contador de descanso |
| **Reporte final** | Muestra total trabajados y total descansados por turno |

### Ejemplo de Reporte

```
Turno del día:
├── 🟢 Trabajados: 2h 30min
└── 🔵 Descansados: 30min
```