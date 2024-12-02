from Modulos.Utils.utils import validar_archivo_existe, abrir_archivo

def cargar_inventario_desde_binario(archivo_bin):
    inventario = {}
    if not validar_archivo_existe(archivo_bin, 'rb'):
        print(f"Error: El archivo {archivo_bin} no existe.")
        return inventario

    archivo = abrir_archivo(archivo_bin, 'rb')
    if archivo is None:
        return inventario

    contenido = leer_contenido_archivo(archivo)
    if not contenido:
        archivo.close()
        return inventario

    lineas = contenido.split('\n')
    inventario = procesar_lineas_inventario(lineas)

    archivo.close()
    return inventario

def leer_contenido_archivo(archivo):
    try:
        data = archivo.read().decode('utf-8')
        return data
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def procesar_lineas_inventario(lineas):
    inventario = {}
    for linea in lineas:
        if linea.strip():
            producto = parsear_linea_producto(linea)
            if producto:
                actualizar_inventario(inventario, producto)
    return inventario

def parsear_linea_producto(linea):
    partes = linea.split('#')
    if len(partes) < 7:
        print(f"Error: Línea de datos mal formada: {linea}")
        return None

    try:
        return {
            'proveedor': partes[0].strip(),
            'fecha_ingreso': partes[1].strip(),
            'telefono': partes[2].strip(),
            'codigo_producto': partes[3].strip(),
            'producto': partes[4].strip(),
            'cantidad': int(partes[5].strip()),
            'precio_unitario': float(partes[6].strip()),
            'ventas': []
        }
    except ValueError as e:
        print(f"Error al parsear producto: {e}")
        return None

def actualizar_inventario(inventario, producto):
    if producto['producto'] not in inventario:
        inventario[producto['producto']] = producto
    else:
        inventario[producto['producto']]['cantidad'] += producto['cantidad']

def guardar_inventario_en_binario(archivo_bin, inventario):
    if not validar_archivo_existe(archivo_bin, 'wb'):
        print(f"Error: El archivo {archivo_bin} no existe.")
        return
    
    archivo = abrir_archivo(archivo_bin, 'wb')
    if archivo is None:
        return

    try:
        escribir_inventario_a_archivo(archivo, inventario)
    except Exception as e:
        print(f"Error al guardar el archivo {archivo_bin}: {e}")

    archivo.close()

def escribir_inventario_a_archivo(archivo, inventario):
    for producto, datos in inventario.items():
        linea = formatear_producto(datos)
        archivo.write(linea.encode('utf-8'))

def formatear_producto(datos):
    return f"{datos['proveedor']}#{datos['fecha_ingreso']}#{datos['telefono']}#{datos['codigo_producto']}#{datos['producto']}#{datos['cantidad']}#{datos['precio_unitario']}\n"