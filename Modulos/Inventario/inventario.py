# modulos/inventario/inventario.py

from Modulos.Utils.utils import validar_archivo_existe  # Importamos la función para validar el archivo

def leer_datos_bin(archivo_bin):
    """Lee un archivo binario con los datos y los organiza en un diccionario de inventario."""
    
    # Validamos que el archivo de inventario exista antes de continuar
    if not validar_archivo_existe(archivo_bin, 'rb'):
        print(f"Error: El archivo {archivo_bin} no existe.")
        return {}
    
    inventario = {}

    try:
        with open(archivo_bin, 'rb') as f:
            data = f.read().decode('utf-8')
    except Exception as e:
        print(f"Error al leer el archivo {archivo_bin}: {e}")
        return {}

    lineas = data.split('\n')
    
    for linea in lineas:
        if linea.strip():  # Ignorar líneas vacías
            partes = linea.split('#')
            proveedor = partes[0].strip()
            fecha = partes[1].strip()
            telefono = partes[2].strip()
            codigo_producto = partes[3].strip()
            producto = partes[4].strip()
            cantidad = int(partes[5].strip())
            precio_unitario = float(partes[6].strip())
            
            if producto not in inventario:
                inventario[producto] = {
                    'proveedor': proveedor,
                    'telefono': telefono,
                    'fecha_ingreso': fecha,
                    'codigo_producto': codigo_producto,
                    'cantidad': 0,
                    'precio_unitario': precio_unitario,
                    'ventas': []  # Lista de ventas (vacía al inicio)
                }
            
            inventario[producto]['cantidad'] += cantidad
    
    return inventario

def guardar_inventario(archivo_bin, inventario):
    print(inventario)
    """Reescribe el archivo binario de inventario con las cantidades actualizadas."""
    # Validamos que el archivo de inventario exista antes de continuar
    if not validar_archivo_existe(archivo_bin, 'wb'):
        print(f"Error: El archivo {archivo_bin} no existe.")
        return
    
    try:
        with open(archivo_bin, 'wb') as f:
            for producto, datos in inventario.items():
                linea = f"{datos['proveedor']}#{datos['fecha_ingreso']}#{datos['telefono']}#{datos['codigo_producto']}#{producto}#{datos['cantidad']}#{datos['precio_unitario']}\n"
                f.write(linea.encode('utf-8'))
    except Exception as e:
        print(f"Error al guardar el archivo {archivo_bin}: {e}")
