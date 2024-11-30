# main.py

from Modulos.Inventario.inventario import leer_datos_bin, guardar_inventario
from Modulos.Ventas.ventas import procesar_ventas_y_agrupar_por_cliente, generar_factura

# Ruta de los archivos binarios
archivo_bin_ventas = 'Datos/ventas.bin'  # Ruta del archivo binario de ventas
archivo_bin_inventario = 'Datos/inventario.bin'  # Ruta del archivo binario de inventario

# Carpeta donde se guardarán las facturas
carpeta_facturas = 'Facturas'

# Crear la carpeta de facturas si no existe

# Leer el inventario
inventario = leer_datos_bin(archivo_bin_inventario)

# Procesar las ventas y agrupar los productos por cliente
ventas_por_cliente = procesar_ventas_y_agrupar_por_cliente(archivo_bin_ventas, archivo_bin_inventario,inventario)

# Generar las facturas para cada cliente
for cliente, datos_venta in ventas_por_cliente.items():
    fecha_limpia = datos_venta['fecha'].replace('/', '-').replace(':', '-')
    archivo_factura = f"{carpeta_facturas}/factura_{cliente}_{fecha_limpia}.txt"
    
    # Generar la factura con los productos comprados por el cliente
    generar_factura({'cliente': cliente, 'fecha': datos_venta['fecha'], 'telefono': datos_venta['telefono'], 'productos': datos_venta['productos']}, archivo_factura)
    
    print(f"Factura generada para el cliente {cliente} con fecha {datos_venta['fecha']}")

# Después de procesar todas las ventas, guardar el inventario actualizado
guardar_inventario(archivo_bin_inventario, inventario)
