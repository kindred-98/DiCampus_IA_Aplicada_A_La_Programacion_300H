# ============================================
# FUNCIÓN A — convertir_celsius
# ============================================

def convertir_celsius(grados: float) -> float:
    """
    Convierte grados Celsius a Fahrenheit.

    Args:
        grados (float): Temperatura en Celsius.

    Returns:
        float: Temperatura equivalente en Fahrenheit.

    Manejo de errores:
        - Si el parámetro no es numérico, devuelve un mensaje de error.
    """
    if not isinstance(grados, (int, float)):
        return "Error: debes ingresar un número."

    return (grados * 9/5) + 32


# ============================================
# FUNCIÓN B — filtrar_pares
# ============================================

def filtrar_pares(numeros: list) -> list:
    """
    Devuelve solo los números pares de una lista.

    Args:
        numeros (list): Lista de números enteros.

    Returns:
        list: Lista con solo los números pares.

    Manejo de errores:
        - Si el parámetro no es una lista, devuelve un mensaje de error.
    """
    if not isinstance(numeros, list):
        return "Error: debes ingresar una lista."

    return [n for n in numeros if isinstance(n, int) and n % 2 == 0]


# ============================================
# FUNCIÓN C — contar_vocales
# ============================================

def contar_vocales(texto: str) -> int:
    """
    Cuenta cuántas vocales (a, e, i, o, u) tiene una cadena de texto,
    sin distinguir mayúsculas de minúsculas.

    Args:
        texto (str): Cadena de texto a analizar.

    Returns:
        int: Número de vocales encontradas.

    Manejo de errores:
        - Si el parámetro no es una cadena, devuelve un mensaje de error.
    """
    if not isinstance(texto, str):
        return "Error: debes ingresar un texto."

    texto = texto.lower()
    vocales = "aeiou"
    contador = 0

    for caracter in texto:
        if caracter in vocales:
            contador += 1

    return contador


# ============================================
# PRUEBAS DE TODAS LAS FUNCIONES
# ============================================

print("=== PRUEBAS convertir_celsius ===")
print(convertir_celsius(0))      # 32.0
print(convertir_celsius(100))    # 212.0
print(convertir_celsius(37))     # 98.6 aprox
print(convertir_celsius(-40))    # -40.0
print(convertir_celsius("hola")) # Error

print("\n=== PRUEBAS filtrar_pares ===")
print(filtrar_pares([1, 2, 3, 4, 5, 6]))      # [2, 4, 6]
print(filtrar_pares([10, 15, 20, 25]))        # [10, 20]
print(filtrar_pares([]))                      # []
print(filtrar_pares([7, 11, 13]))             # []
print(filtrar_pares("no es lista"))           # Error

print("\n=== PRUEBAS contar_vocales ===")
print(contar_vocales("Hola"))                 # 2
print(contar_vocales("AEIOU"))                # 5
print(contar_vocales(""))                     # 0
print(contar_vocales("rhythm"))               # 0 (sin vocales)
print(contar_vocales("Kindred y Yasuo"))      # 5
print(contar_vocales(123))                    # Error
