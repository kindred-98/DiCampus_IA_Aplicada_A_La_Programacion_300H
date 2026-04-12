                                            # ESTO ES LO QUE ME DARIA MI PROMPT

import datetime

# Base de datos simulada con integridad de datos
productos = {
    'cafe':  {'precio': 2.5,  'stock': 10},
    'te':    {'precio': 2.0,  'stock': 5},
    'zumo':  {'precio': 3.0,  'stock': 8},  # Corregido: Clave 'stock' añadida
}

historial = []

def calcular_total(pedido):
    """Calcula la suma total de los productos existentes en el pedido."""
    total = 0.0
    if not pedido:
        return 0.0
        
    for item in pedido:
        # Validación de seguridad: ¿Existe el producto en nuestra base de datos?
        if item in productos:
            total += productos[item]['precio']
        else:
            print(f"⚠️ Advertencia: El producto '{item}' no existe en el catálogo.")
            
    return total  # Corregido: Ahora devuelve la suma, no el promedio

def registrar_pedido(cliente, pedido):
    """Valida, calcula y registra un pedido en el historial."""
    if len(pedido) > 0:
        total = calcular_total(pedido)
        fecha = datetime.date.today()  # Corregido: Llamada a la función con ()
        
        # Registro en el historial
        historial.append({
            'cliente': cliente,
            'pedido':  pedido,
            'total':   total,
            'fecha':   fecha
        })
        
        # Corregido: Uso de f-string para evitar TypeError al concatenar str + float
        print(f"✅ Pedido de {cliente} registrado con éxito. Total: ${total:.2f}")
    else:
        print("❌ Error: No se puede registrar un pedido vacío.")

def obtener_resumen():
    """Devuelve un resumen estadístico de los pedidos registrados."""
    if not historial:
        return 'No hay pedidos registrados actualmente.'
    
    totales = [registro['total'] for registro in historial]
    media = sum(totales) / len(totales)
    
    return f'Total pedidos: {len(historial)} | Media por pedido: ${media:.2f}'

# --- Zona de Pruebas (Test) ---
if __name__ == "__main__":
    registrar_pedido('Ana', ['cafe', 'te'])
    registrar_pedido('Luis', ['zumo', 'cafe'])
    # Prueba de producto inexistente para validar la robustez
    registrar_pedido('Marta', ['cafe', 'agua_mineral']) 
    
    print("-" * 30)
    print(obtener_resumen())



                                            # Y LUEGO MODULARIZARLO 


                                    # datos.py - Módulo de persistencia de datos


# Diccionario de productos con stock corregido
productos = {
    'cafe':  {'precio': 2.5,  'stock': 10},
    'te':    {'precio': 2.0,  'stock': 5},
    'zumo':  {'precio': 3.0,  'stock': 8}, 
}
# Lista global para almacenar los pedidos realizados
historial = []



                                    # pedidos.py - Módulo de lógica de negocio


import datetime
from datos import productos, historial

def calcular_total(pedido):
    """Calcula la suma total validando que los productos existan."""
    total = 0.0
    if not pedido:
        return 0.0
        
    for item in pedido:
        if item in productos:
            total += productos[item]['precio']
        else:
            # Log de advertencia (buena práctica de diseño)
            print(f"⚠️ Advertencia: El producto '{item}' no existe en el catálogo.")
            
    return total

def registrar_pedido(cliente, pedido):
    """Procesa el pedido y lo guarda en el historial de datos."""
    if len(pedido) > 0:
        total = calcular_total(pedido)
        fecha = datetime.date.today() # Corregido con ()
        
        historial.append({
            'cliente': cliente,
            'pedido':  pedido,
            'total':   total,
            'fecha':   fecha
        })
        
        # Usamos f-string para evitar errores de tipo al imprimir
        print(f"✅ Pedido de {cliente} registrado: ${total:.2f}")
    else:
        print("❌ Error: No se puede registrar un pedido vacío.")



                                    # reportes.py - Módulo de salida y ejecución principal


from datos import historial
from pedidos import registrar_pedido

def obtener_resumen():
    """Genera un reporte estadístico basado en el historial."""
    if not historial:
        return '📊 No hay pedidos registrados actualmente.'
    
    totales = [registro['total'] for registro in historial]
    media = sum(totales) / len(totales)
    
    return (f"\n--- RESUMEN DEL DÍA ---\n"
            f"Total pedidos: {len(historial)}\n"
            f"Media por pedido: ${media:.2f}\n"
            f"-----------------------")

# Simulación de ejecución del sistema
if __name__ == "__main__":
    print("🚀 Iniciando Sistema de Gestión de Pedidos...\n")
    
    # Registramos algunos pedidos
    registrar_pedido('Ana', ['cafe', 'te'])
    registrar_pedido('Luis', ['zumo', 'cafe'])
    registrar_pedido('Marta', ['cafe', 'item_inexistente']) # Caso de prueba
    
    # Mostramos el reporte final
    print(obtener_resumen())


    