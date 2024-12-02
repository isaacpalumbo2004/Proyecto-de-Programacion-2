from Modulos.Inventario.inventario import cargar_inventario_desde_binario,guardar_inventario_en_binario
from Modulos.Ventas.ventas import procesar_y_agrupar_ventas,generar_factura_venta

archivo_bin_ventas = 'Datos/ventas.bin' 
archivo_bin_inventario = 'Datos/inventario.bin'

carpeta_facturas = 'Facturas'


inventario = cargar_inventario_desde_binario(archivo_bin_inventario)

ventas_por_cliente = procesar_y_agrupar_ventas(archivo_bin_ventas, archivo_bin_inventario,inventario)

for cliente, datos_venta in ventas_por_cliente.items():
    fecha_limpia = datos_venta['fecha'].replace('/', '-').replace(':', '-')
    archivo_factura = f"{carpeta_facturas}/factura_{cliente}_{fecha_limpia}.txt"
    
    generar_factura_venta({'cliente': cliente, 'fecha': datos_venta['fecha'], 'telefono': datos_venta['telefono'], 'productos': datos_venta['productos']}, archivo_factura)
    
    print(f"Factura generada para el cliente {cliente} con fecha {datos_venta['fecha']}")
    
guardar_inventario_en_binario(archivo_bin_inventario, inventario)
