def leer_ventas_bin(archivo_bin):
    """Lee el archivo binario y lo organiza en un diccionario de ventas con más campos."""
    ventas = {}

    # Abrir y leer el archivo binario
    with open(archivo_bin, 'rb') as f:
        # Leer el archivo binario y decodificarlo a texto
        data = f.read().decode('utf-8')
    
    # Dividir los datos en líneas
    lineas = data.split('\n')
    
    # Procesar cada línea para extraer la información de las ventas
    for linea in lineas:
        if linea.strip():  # Ignorar líneas vacías
            partes = linea.split('#')
            
            proveedor = partes[0].strip()  # Nombre del proveedor
            fecha_venta = partes[1].strip()  # Fecha de la venta
            telefono = partes[2].strip()  # Teléfono del proveedor
            codigo_producto = partes[3].strip()  # Código de producto
            producto = partes[4].strip()  # Nombre del producto
            cantidad = int(partes[5].strip())  # Cantidad vendida
            precio_unitario = float(partes[6].strip())  # Precio unitario
            estado = partes[7].strip()  # Estado de la venta (por ejemplo, "Vendido")
            total = float(partes[8].strip())  # Total (cantidad * precio unitario)
            
            # Si el producto no está en las ventas, agregarlo
            if producto not in ventas:
                ventas[producto] = {
                    'proveedor': proveedor,
                    'telefono': telefono,
                    'fecha_venta': fecha_venta,
                    'codigo_producto': codigo_producto,
                    'cantidad': 0,  # Inicializamos la cantidad a 0
                    'precio_unitario': precio_unitario,
                    'estado': estado,
                    'total': 0.0
                }
            
            # Sumar la cantidad a las ventas del producto y actualizar el total
            ventas[producto]['cantidad'] += cantidad
            ventas[producto]['total'] += total
    
    return ventas

# Ruta al archivo binario de ventas (ejemplo)
archivo_bin_path = 'ventas_cemento.bin'  # Ruta del archivo binario de ventas

# Leer y procesar los datos del archivo
ventas = leer_ventas_bin(archivo_bin_path)

# Crear un archivo de texto para guardar la tabla de ventas
archivo_txt_path = 'ventas_cemento.txt'

# Escribir los datos de las ventas en formato tabla en el archivo de texto
with open(archivo_txt_path, 'w', encoding='utf-8') as f:
    # Escribir encabezado
    f.write(f"{'Proveedor':<25} {'Fecha':<15} {'Teléfono':<20} {'Código':<10} {'Producto':<25} {'Cantidad':<10} {'Precio Unitario':<15} {'Estado':<10} {'Total':<10}\n")
    f.write('-' * 115 + '\n')  # Línea de separación
    
    # Escribir los datos de las ventas
    for producto, datos in ventas.items():
        f.write(f"{datos['proveedor']:<25} {datos['fecha_venta']:<15} {datos['telefono']:<20} {datos['codigo_producto']:<10} {producto:<25} {datos['cantidad']:<10} {datos['precio_unitario']:<15.2f} {datos['estado']:<10} {datos['total']:<10.2f}\n")

print(f"Archivo 'ventas_cemento.txt' creado con éxito.")
