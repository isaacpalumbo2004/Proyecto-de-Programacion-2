
def validar_archivo_existe(archivo,data):
    try:
        with open(archivo, data):
            return True 
    except FileNotFoundError:
        return False
      

def abrir_archivo(archivo_bin, modo):
    try:
        archivo = open(archivo_bin, modo)
        return archivo
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_bin} no se encontró.")
        return None