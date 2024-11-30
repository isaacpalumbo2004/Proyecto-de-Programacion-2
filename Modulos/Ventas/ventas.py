from Modulos.Inventario.inventario import leer_datos_bin, guardar_inventario  # Importamos las funciones de inventario
from Modulos.Utils.utils import validar_archivo_existe

def generar_factura(venta, archivo_factura):
    if not validar_archivo_existe(archivo_factura,'w'):
        print(f"Error: El archivo {archivo_factura,'w'} no existe.")
        return
    with open(archivo_factura, 'w', encoding='utf-8') as f:
        f.write(f"Factura de Venta\n")
        f.write(f"Cliente: {venta['cliente']}\n")
        f.write(f"Fecha: {venta['fecha']}\n")
        f.write(f"Teléfono: {venta['telefono']}\n")
        f.write(f"\n")
        f.write(f"{'Producto':<30} {'Cantidad':<10} {'Precio Unitario (¥)':<20} {'Total (¥)':<20}\n")
        f.write("-" * 80 + "\n")
        
        total_venta = 0.0
        for producto, datos in venta['productos'].items():
            total_producto = datos['cantidad'] * datos['precio_unitario']
            total_venta += total_producto
            f.write(f"{producto:<30} {datos['cantidad']:<10} {datos['precio_unitario']:<20.2f} {total_producto:<20.2f}\n")
        
        f.write("-" * 80 + "\n")
        f.write(f"{'Total de la Venta (¥)':<60} {total_venta:<20.2f}\n")
        f.write(f"\nGracias por su compra!\n")


def procesar_ventas_y_agrupar_por_cliente(archivo_ventas_bin, archivo_inventario_bin,inventario):
    ventas_por_cliente = {}
    
    # Leer el archivo de inventario
    
    print("Hola",inventario)
    # Verificar si el archivo de ventas existe
    try:
        with open(archivo_ventas_bin, 'rb') as f:
            data = f.read().decode('utf-8')
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_ventas_bin} no existe")
        return {}

    lineas = data.split('\n')
    
    for linea in lineas:
        if linea.strip():  # Ignorar líneas vacías
            partes = linea.split('#')
            cliente = partes[0].strip()  # Nombre del cliente
            fecha = partes[1].strip()    # Fecha de la venta
            telefono = partes[2].strip() # Teléfono
            producto = partes[4].strip()  # Nombre del producto
            cantidad_venta = int(partes[5].strip())  # Cantidad a vender
            precio_venta = float(partes[6].strip())  # Precio de venta
            
            # Verificamos si el producto está en el inventario
            if producto in inventario:
                producto_inventario = inventario[producto]
                
                # Verificar si hay suficiente cantidad en el inventario
                if producto_inventario['cantidad'] >= cantidad_venta:
                    # Reducir la cantidad disponible en el inventario
                    producto_inventario['cantidad'] -= cantidad_venta
                    
                    # Registrar la venta en ventas por cliente
                    if cliente not in ventas_por_cliente:
                        ventas_por_cliente[cliente] = {
                            'fecha': fecha,
                            'telefono': telefono,
                            'productos': {}
                        }
                    
                    if producto in ventas_por_cliente[cliente]['productos']:
                        ventas_por_cliente[cliente]['productos'][producto]['cantidad'] += cantidad_venta
                    else:
                        ventas_por_cliente[cliente]['productos'][producto] = {
                            'cantidad': cantidad_venta,
                            'precio_unitario': precio_venta
                        }
                else:
                    print(f"No hay suficiente stock de {producto} para la venta.")
            else:
                print(f"El producto {producto} no está en el inventario.")
    guardar_inventario(archivo_inventario_bin, inventario)

    # Una vez procesadas todas las ventas, guardar el inventario actualizado
    
    
    
    return ventas_por_cliente
