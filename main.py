def convertir_bin_a_txt(archivo_bin, archivo_txt):
    # Leer los datos del archivo binario
    with open(archivo_bin, 'rb') as f:
        data = f.read().decode('utf-8')
    lineas = data.split("\n")
    with open(archivo_txt, 'w', encoding='utf-8') as f:
        # Escribir encabezados
        f.write("|----|------------------|-------------------|---|------|--------|\n")
        f.write("|  N |Nombre de Cliente |Nombre de producto  |und|Precio|Total   |\n")
        f.write("|----|------------------|-------------------|---|------|--------|\n")
       
        for i in range(len(lineas)):
            partes = lineas[i].split('#')
            nombre_cliente = partes[0]
            nombre_producto = partes[4]
            cantidad = int(partes[5])
            precio_unitario = float(partes[6].replace('¥', ''))

            # Calcular el total
            total = cantidad * precio_unitario

            # Escribir la línea en el archivo de texto
            f.write(f"| {i + 1:<2} |{nombre_cliente:<16} |{nombre_producto:<17}|{cantidad:<3}|{precio_unitario:.2f}¥ |{total:.2f}¥|\n")
        
        f.write("|----|------------------|-------------------|---|------|--------|\n")

# Ejecutar la conversión
convertir_bin_a_txt('datos.bin', 'inventario.txt')

print("Archivo 'inventario.txt' generado con éxito.")
