from Modulos.Inventario.inventario import guardar_inventario_en_binario
from Modulos.Utils.utils import abrir_archivo

def generar_factura_venta(venta, archivo_factura):
    total_venta = 0.0 
    archivo = None  # Inicializar la variable archivo
    
    archivo = abrir_archivo(archivo_factura, 'w')
    
    archivo.write(f"Factura de Venta\n")
    archivo.write(f"Cliente: {venta['cliente']}\n")
    archivo.write(f"Fecha: {venta['fecha']}\n")
    archivo.write(f"Teléfono: {venta['telefono']}\n")
    archivo.write(f"\n")
    archivo.write(f"{'Producto':<30} {'Cantidad':<10} {'Precio Unitario (¥)':<20} {'Total (¥)':<20}\n")
    archivo.write("-" * 80 + "\n")
    
    for producto, datos in venta['productos'].items():
        total_producto = datos['cantidad'] * datos['precio_unitario']
        total_venta += total_producto
        archivo.write(f"{producto:<30} {datos['cantidad']:<10} {datos['precio_unitario']:<20.2f} {total_producto:<20.2f}\n")
    
    archivo.write("-" * 80 + "\n")
    archivo.write(f"{'Total de la Venta (¥)':<62.5} {total_venta:<20.2f}\n")
    archivo.write(f"\nGracias por su compra!\n")
    
    archivo.close()  

def procesar_ventas(archivo_ventas_bin):
    """Lee y procesa las ventas desde un archivo binario."""
    ventas = []  # Inicializar la lista de ventas
    archivo_ventas = None  # Inicializar la variable del archivo
    data = ""  # Inicializar la variable de datos

    archivo_ventas = abrir_archivo(archivo_ventas_bin, 'rb')
    data = archivo_ventas.read().decode('utf-8') 
    archivo_ventas.close() 

    lineas = data.split('\n') 

    for linea in lineas:
        if linea.strip(): 
            partes = linea.split('#')
            cliente = partes[0].strip() 
            fecha = partes[1].strip()   
            telefono = partes[2].strip()
            producto = partes[4].strip() 
            cantidad_venta = int(partes[5].strip())
            precio_venta = float(partes[6].strip())
            
            # Agregar cada venta como un diccionario a la lista
            ventas.append({
                'cliente': cliente,
                'fecha': fecha,
                'telefono': telefono,
                'producto': producto,
                'cantidad': cantidad_venta,
                'precio_unitario': precio_venta
            })
    
    return ventas

def agrupar_ventas_por_cliente(ventas, inventario):
    """Agrupa las ventas por cliente y actualiza el inventario."""
    ventas_por_cliente = {}  # Inicializar el diccionario para agrupar ventas
    
    for venta in ventas:
        producto = venta['producto']
        cantidad_venta = venta['cantidad']
        
        if producto in inventario:
            producto_inventario = inventario[producto]
            
            if producto_inventario['cantidad'] >= cantidad_venta:
                producto_inventario['cantidad'] -= cantidad_venta
                
                cliente = venta['cliente']
                
                if cliente not in ventas_por_cliente:
                    ventas_por_cliente[cliente] = {
                        'fecha': venta['fecha'],
                        'telefono': venta['telefono'],
                        'productos': {}
                    }
                
                if producto in ventas_por_cliente[cliente]['productos']:
                    ventas_por_cliente[cliente]['productos'][producto]['cantidad'] += cantidad_venta
                else:
                    ventas_por_cliente[cliente]['productos'][producto] = {
                        'cantidad': cantidad_venta,
                        'precio_unitario': venta['precio_unitario']
                    }
            else:
                print(f"No hay suficiente stock de {producto} para la venta.")
        else:
            print(f"El producto {producto} no esta en el inventario.")
    
    return ventas_por_cliente

def procesar_y_agrupar_ventas(archivo_ventas_bin, archivo_inventario_bin, inventario):
    
    ventas = []  
    ventas_por_cliente = {} 

    ventas = procesar_ventas(archivo_ventas_bin)
        
    ventas_por_cliente = agrupar_ventas_por_cliente(ventas, inventario)
    
    return ventas_por_cliente