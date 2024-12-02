#utilitarias
def Diccionario():
    return {
        "abrirArchivo":openF,
        "ValidarNombreRetornaBool":Valname,
        "UtilitariaParaValName":manejo,
        "ValidarEnteros":Valint,
        "ValidarFloat":ValFloat
    }

def openF():#objet
    archivo = object
    try:
        archivo = open("InventarioVentas.bin","rb")
        return archivo
    except FileNotFoundError:
        print("- objet-File: Archivo no encontrado. ")
        return None

def Valname(nombre):#bool
    
    tupla = ("0","1","2","3","4","5","6","7","8","9","@","*","/","-","+",".","#","$")\

    for i in range(len(nombre)):
        for j in range(len(tupla)):
            if (nombre[i]==tupla[j]):
                return False
    return True

def manejo(dato):#str
    while(True):
        try:
            nombre = Valname(nombre)
            return nombre
        except TypeError:
            print("-Tiene que tener caracteres del abecedario no numero")
            dato = input("- Nombre: ") 

def Valint(numero):#int
    valor = 0 # int 
    while True:
        try:
            valor = int(numero)
            if (valor < 0):
                numero = input("El dato solicitado no es valido, debe ingresar un numero mayor a 0: ")
            else: 
                return valor
        except ValueError:
            print("ValuError, el programa no admite str ni float ")
            numero  = input ("Por favor ingrese un valor entero positivo: ")
        
def ValFloat(numero):#float
    valor = 0.0 # float
    while True:
        try:
            valor = float(numero)
            if (valor < 0.0):
                numero = input("El dato solicitado no es valido, debe ingresar un numero mayor a 0.0: ")
            else: 
                return valor
        except ValueError:
            print("ValuError, el programa no admite str ")
            numero  = input ("Por favor ingrese un valor decimal positivo: ")

validaciones = Diccionario()