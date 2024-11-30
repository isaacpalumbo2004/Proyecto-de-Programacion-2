
def validar_archivo_existe(archivo,data):
    try:
        with open(archivo, data):
            return True 
    except FileNotFoundError:
        return False
      

