print("Parcial Practico 10/2021")

def generarID(apellido, nombre, docum):
    mayus = apellido.upper()
    long = str(len(mayus)) #guardo la longitud de la variable mayus como string en una nueva variable 

    minusc = nombre.lower()
    sep = minusc.split() #separo y guardo cada palabra en una lista llamada sep
    nombre = "" 
    for i in range(0, len(sep)): 
        sep[i] = sep[i].capitalize() #la primera letra de cada palabra se pasa a mayuscula
        nombre += (sep[i] + " ") #guardo nuevamente en la misma variable nombre


    for i in range(0, len(docum)): #uso un for para que ingrese el dato del dni entre 7 u 8 digitos
        if (len(docum) == 7 or len(docum) == 8):
            if len(docum) == 7: #guardo los ultimos 4 digitos de un documento de 7 en total
                dig4 = docum[3:]
            else:
                dig4 = docum[4:]
            break
        else:
            print("Incorrecto. Ingrese el numero de documento de 7 u 8 digitos")
            docum = input("Ingrese su numero de documento: ")
            continue

    bandera = True
    while bandera:
        try:
            edad = int(input("Ingrese la edad: "))
            bandera = False
        except ValueError: #en caso de ingresar string o float, ingresa en la exception valueError
            print("Debe ingresar un numero entero")


    sexo = input("Ingrese el sexo, entre H(Hombre) o M(Mujer): ")
    bander = True
    while bander:
        if (sexo == "H" or sexo == "M"):
            bander = False
        else:
            print("Incorrecto. Ingrese la opcion entre los valores asignados") #queda en el bucle si no ingresa H o M(mayuscula)
            sexo = input("Ingrese el sexo, entre H(Hombre) o M(Mujer): ")
        
    """Mostrar todo los datos"""
    print("ID: "+ mayus + sep[0][0].capitalize() + long + dig4)
    print("Apellido y Nombre: " + apellido.upper() + ", " + nombre)
    print("Edad: ", edad)
    print("DNI: " + docum)
        
    if sexo == "H":
        print("Sexo: Hombre")
    else:
        print("Sexo: Mujer")        


"""formar un bucle que tiene como salida cuando el apellido sea ingresado un vacio("")"""
bandera = True
while bandera:
    apellido = input("Ingrese el apellido: ")
    if apellido != "":
        nombre = input("Ingrese el nombre: ")
        docum = input("Ingrese el numero de documento: ")
        generarID(apellido, nombre, docum)
    
    else:
        bandera = False    

    