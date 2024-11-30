def leer_datos_bin(archivo_bin):
    """Lee un archivo binario con los datos y los organiza en un diccionario de inventario."""
    inventario = {}

    # Abrir y leer el archivo binario
    with open(archivo_bin, 'rb') as f:
        # Leer el archivo binario y decodificarlo a texto
        data = f.read().decode('utf-8')
    
    # Dividir los datos en líneas
    lineas = data.split('\n')
    
    # Procesar cada línea para extraer la información
    for linea in lineas:
        if linea.strip():  # Ignorar líneas vacías
            partes = linea.split('#')
            
            proveedor = partes[0].strip()  # Nombre del proveedor
            fecha = partes[1].strip()      # Fecha de ingreso
            telefono = partes[2].strip()   # Teléfono del proveedor
            codigo_producto = partes[3].strip()  # Código de producto
            producto = partes[4].strip()   # Nombre del producto
            cantidad = int(partes[5].strip())    # Cantidad en inventario
            precio_unitario = float(partes[6].strip())  # Precio unitario
            
            # Si el producto no está en el inventario, agregarlo
            if producto not in inventario:
                inventario[producto] = {
                    'proveedor': proveedor,
                    'telefono': telefono,
                    'fecha_ingreso': fecha,
                    'codigo_producto': codigo_producto,
                    'cantidad': 0,  # Inicializamos la cantidad a 0
                    'precio_unitario': precio_unitario,
                    'ventas': []  # Lista de ventas (debería ser vacía al inicio)
                }
            
            # Sumar la cantidad al inventario del producto
            inventario[producto]['cantidad'] += cantidad
    
    return inventario

def guardar_inventario(archivo_bin, inventario):
    """Reescribe el archivo binario de inventario con las cantidades actualizadas."""
    with open(archivo_bin, 'wb') as f:
        # Reescribir el archivo binario con los datos actualizados
        for producto, datos in inventario.items():
            linea = f"{datos['proveedor']}#{datos['fecha_ingreso']}#{datos['telefono']}#{datos['codigo_producto']}#{producto}#{datos['cantidad']}#{datos['precio_unitario']}\n"
            f.write(linea.encode('utf-8'))

def generar_factura(venta, archivo_factura):
    """Genera una factura de la venta en un archivo de texto, mostrando los montos en yenes."""
    with open(archivo_factura, 'w', encoding='utf-8') as f:
        # Escribir encabezado de la factura
        f.write(f"Factura de Venta\n")
        f.write(f"Cliente: {venta['cliente']}\n")
        f.write(f"Fecha: {venta['fecha']}\n")
        f.write(f"Teléfono: {venta['telefono']}\n")
        f.write(f"\n")
        f.write(f"{'Producto':<30} {'Cantidad':<10} {'Precio Unitario (¥)':<20} {'Total (¥)':<20}\n")
        f.write("-" * 80 + "\n")
        
        total_venta = 0.0
        # Escribir los productos vendidos en la factura
        for producto, datos in venta['productos'].items():
            total_producto = datos['cantidad'] * datos['precio_unitario']
            total_venta += total_producto
            f.write(f"{producto:<30} {datos['cantidad']:<10} {datos['precio_unitario']:<20.2f} {total_producto:<20.2f}\n")
        
        f.write("-" * 80 + "\n")
        f.write(f"{'Total de la Venta (¥)':<60} {total_venta:<20.2f}\n")
        f.write(f"\nGracias por su compra!\n")

def procesar_ventas_y_agrupar_por_cliente(archivo_ventas_bin, carpeta_facturas):
    """Procesa el archivo de ventas y agrupa los productos por cliente en una sola venta, generando una factura."""
    ventas_por_cliente = {}

    # Abrir y leer el archivo binario de ventas
    with open(archivo_ventas_bin, 'rb') as f:
        # Leer el archivo binario y decodificarlo a texto
        data = f.read().decode('utf-8')
    
    # Dividir los datos en líneas
    lineas = data.split('\n')
    
    # Procesar cada línea para extraer la información de las ventas
    for linea in lineas:
        if linea.strip():  # Ignorar líneas vacías
            partes = linea.split('#')
            
            cliente = partes[0].strip()  # Nombre del cliente
            fecha = partes[1].strip()    # Fecha de la venta
            telefono = partes[2].strip() # Teléfono
            codigo_producto = partes[3].strip()  # Código de producto
            producto = partes[4].strip()  # Nombre del producto
            cantidad_venta = int(partes[5].strip())  # Cantidad a vender
            precio_venta = float(partes[6].strip())  # Precio de venta
            
            # Si el cliente no tiene ventas registradas, inicializamos
            if cliente not in ventas_por_cliente:
                ventas_por_cliente[cliente] = {
                    'fecha': fecha,
                    'telefono': telefono,
                    'productos': {}
                }
            
            # Si el producto ya existe en los productos del cliente, sumamos la cantidad
            if producto in ventas_por_cliente[cliente]['productos']:
                ventas_por_cliente[cliente]['productos'][producto]['cantidad'] += cantidad_venta
            else:
                ventas_por_cliente[cliente]['productos'][producto] = {
                    'cantidad': cantidad_venta,
                    'precio_unitario': precio_venta
                }

    # Generar la factura para cada cliente
    for cliente, datos_venta in ventas_por_cliente.items():
        fecha_limpia = datos_venta['fecha'].replace('/', '-').replace(':', '-')
        archivo_factura = f"{carpeta_facturas}/factura_{cliente}_{fecha_limpia}.txt"
        
        # Generar la factura con los productos comprados por el cliente
        generar_factura({'cliente': cliente, 'fecha': datos_venta['fecha'], 'telefono': datos_venta['telefono'], 'productos': datos_venta['productos']}, archivo_factura)

    return ventas_por_cliente

# Ruta al archivo binario de ventas (ejemplo)
archivo_bin_ventas = 'ventas.bin'  # Ruta del archivo binario de ventas

# Ruta de la carpeta donde se guardarán las facturas
carpeta_facturas = 'facturas'  # Carpeta para las facturas

# Procesar las ventas y agrupar los productos por cliente
ventas_por_cliente = procesar_ventas_y_agrupar_por_cliente(archivo_bin_ventas, carpeta_facturas)

# Mostrar las ventas agrupadas
for cliente, datos_venta in ventas_por_cliente.items():
    print(f"Factura generada para el cliente {cliente} con fecha {datos_venta['fecha']}")
