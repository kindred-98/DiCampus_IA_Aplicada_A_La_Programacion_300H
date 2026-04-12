def analizar_notas(alumnos):
    """
    Analiza una lista de alumnos y sus notas.

    Args:
        alumnos (list): Lista de tuplas con formato (nombre: str, nota: float)

    Returns:
        dict: Diccionario con:
            - "nota_maxima": float o None
            - "nota_minima": float o None
            - "nota_media": float
            - "mejor_alumno": str o None

    Ejemplo:
        >>> analizar_notas([("el que entra a clase solo para las evaluaciones", 8.5), ("el flojo", 6.0), ("el inteligente", 9.2)])
        {
            "nota_maxima": 9.2,
            "nota_minima": 6.0,
            "nota_media": 7.9,
            "mejor_alumno": "Marta"
        }
    """

    # Caso límite: lista vacía
    if not alumnos:
        return {
            "nota_maxima": None,
            "nota_minima": None,
            "nota_media": 0,
            "mejor_alumno": None
        }

    # Extraer solo las notas
    notas = [nota for nombre, nota in alumnos]

    nota_max = max(notas)
    nota_min = min(notas)
    nota_media = sum(notas) / len(notas)

    # Encontrar el alumno con mejor nota
    mejor_alumno = max(alumnos, key=lambda x: x[1])[0]

    return {
        "nota_maxima": nota_max,
        "nota_minima": nota_min,
        "nota_media": round(nota_media, 2),
        "mejor_alumno": mejor_alumno
    }

# PRUEBAS
print(analizar_notas([("aphelios", 8.5), ("yone", 6.0), ("akali", 9.2)]))
print(analizar_notas([]))
print(analizar_notas([("Kindred", 10), ("Yasuo", 4.5)]))
