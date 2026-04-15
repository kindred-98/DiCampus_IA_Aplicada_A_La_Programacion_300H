# PARTE 1 — Función es_positivo
def es_positivo(numero):
    """Devuelve True si el número es mayor que 0, False en caso contrario."""
    if not isinstance(numero, (int, float)):
        return "Error: debes ingresar un número"
    return numero > 0


# PARTE 2 — Función capitalizar
def capitalizar(texto):
    """Capitaliza la primera letra de cada palabra. Si está vacío, devuelve 'Texto vacío'."""
    if not isinstance(texto, str):
        return "Error: debes ingresar un texto"
    if texto == "":
        return "Texto vacío"
    return texto.title()


# PARTE 3 — Función validar_email
def validar_email(email):
    """Valida un email de forma muy básica: comprueba que contenga '@' y '.'."""
    if not isinstance(email, str):
        return "Error: debes ingresar un texto"
    return "@" in email and "." in email


# PARTE 4 — Función resumen_usuario
def resumen_usuario(nombre, email):
    """Capitaliza el nombre y valida el email, devolviendo un mensaje final."""
    if not isinstance(nombre, str) or not isinstance(email, str):
        return "Error: datos inválidos"

    nombre_cap = nombre.title()
    email_valido = validar_email(email)

    # Si validar_email devolvió un mensaje de error
    if isinstance(email_valido, str):
        return email_valido

    if email_valido:
        return f"Usuario: {nombre_cap} — Email correcto"
    else:
        return f"Usuario: {nombre_cap} — Email inválido"


# ============================
# PRUEBAS DE TODAS LAS FUNCIONES
# ============================

print("=== PRUEBAS PARTE 1 ===")
print(es_positivo(5))     # True
print(es_positivo(-3))    # False
print(es_positivo(0))     # False
print(es_positivo("hola"))  # Error

print("\n=== PRUEBAS PARTE 2 ===")
print(capitalizar("SOY KINDRED"))   # Hola Mundo
print(capitalizar(""))             # Texto vacío
print(capitalizar(123))            # Error

print("\n=== PRUEBAS PARTE 3 ===")
print(validar_email("usuario@ejemplo.com"))  # True
print(validar_email("usuario.com"))          # False
print(validar_email(123))                    # Error

print("\n=== PRUEBAS PARTE 4 ===")
print(resumen_usuario("kindred", "kindred@spirit.com"))
print(resumen_usuario("yasuo", "yasouleague.com"))
print(resumen_usuario(123, "correo@lol.com"))  # Error
