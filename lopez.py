import mysql.connector
from mysql.connector.errors import Error
import funciones
from datetime import datetime

a = 0 #variable gobal inicializada en 0
def consulta_usuario(conex):# funcion que establece si los datos del usuario se encuentra guardado en la BD
    nombre = input('Ingrese el nombre del usuario: ')
    apellido = input('Ingrese el apellido del usuario: ')
    global a
    tabla = conex.cursor() #conexion con la BD para comprobar si el usuario existe
    sql = 'select id_usuario from lopezfinal.usuarios ' \
        'where nombre = "' + nombre + '" and Apellido = "' + apellido + '"'
    tabla.execute(sql) #consulta en BD y selecciono el id del usuario si existe, en caso contrario el id toma el valor -1 
    lista = tabla.fetchall()
    if tabla.rowcount != 0:#si el numero de filas es distinto a 0 ingresa en el if, para la idea de guardar el dato en la variable global
        for registro in lista:
            a = registro[0] #sobreescribo la variable global a con el valor del id del usuario en la posicion 0 de la tabla
    else:
        a = -1 #cuando no existe el usuario en la base, la variable toma el valor de -1

    tabla.close()


def agregar_usuario(conex):
    nombre = input('Ingrese el nombre del usuario: ')
    apellido = input('Ingrese el apellido del usuario: ')
    ban = True
    while ban:
        documento = input('Ingrese el numero del documento: ')
        if documento.isnumeric() and len(documento)==8:# comprueba si el dato ingresado es numero y tenga una longitud de 8 digitos
            print("El documento es correcto\n")
            ban = False

    bandera = True
    while bandera:#debe ingresar el caracter @ para resultar valido
        email = input("Ingrese el correo electronico del usuario: ")
        for i in range(0, len(email)): 
            if email[i] == '@': #saldra del bucle hasta que un letra del caracter ingresado contenga a @
                print("El email es correcto\n") 
                bandera = False #salida del bucle

    tabla =conex.cursor()
    nombre_usuario = apellido+documento[-6:]# concateno la variable apellido con los 6 digitos del documento
    sql = 'insert into lopezfinal.usuarios(nomb_usuario, Nombre, Apellido, documento, email) '\
        'values ("'+ nombre_usuario + '", "'+ nombre + '","'+ apellido + '","'+ documento +'","' + email + '")'
    tabla.execute(sql)#ejecuta la consulta en la BD
    conex.commit()# guardo los cambios realizados
    print("Los datos han sido guardados\n")
    tabla.close()


def borrar_usuario(conex):
    consulta_usuario(conex)#consulta en la BD si el usuario existe para proceder al borrado del mismo
    
    if a >= 0:# con la variable global determino en este caso que los datos del usuario estan guardado
        tabla2 = conex.cursor()
        #realizo el borrado por medio del id del usuario determinado por la funcion de consulta 
        tabla2.execute('delete from lopezfinal.usuarios ' \
            'where id_usuario = "' + str(a) +'"')
        conex.commit()
        print("El usuario fue borrado correctamente\n")
        tabla2.close()
    else:# en caso contrario el usuario no existe y sus datos no estan guardados
        print("Los datos ingresados no coinciden con un usuario de la Base de Datos")

def cambiar_email(conex):
    consulta_usuario(conex)
    
    if a >= 0: #en el caso que exista el usuario ingresa en el if y se pregunta sobre el email nuevo
        email_act = input("Ingrese la nueva direccion de email: ")
        tabla2 = conex.cursor()
        #ejecuto la actualizacion del email del usuario determinado por su id
        tabla2.execute('update lopezfinal.usuarios Set email = "' + email_act + '" Where id_usuario = "' + str(a) + '"')
        conex.commit()#para guardar los cambios de forma permanente
        print("El email ingresado fue actualizado correctamente\n")
        tabla2.close()
    else:# si no existe el usuario en la BD, ingresa en el else y no se realiza la actualizacion
        print("Los datos ingresados no coinciden con un usuario de la Base de Datos\n")

def carga_comentarios(conex):
    consulta_usuario(conex)
    
    if a>=0:
        coment = input("Ingrese el comentario que desea realizar: ")
        tabla = conex.cursor()
        fechaHora = datetime.now() #en la variable guardo la fecha y la hora en el momento que se guarda el comentario
        
        sql = 'insert into lopezfinal.comentarios (usuario, Texto, fecha, hora)'\
            ' values ("'+ str(a) +'","'+ coment + '", DATE("'+str(fechaHora)+'"), TIME("'+ str(fechaHora)+'"))'
        # separo la fecha con Date de la variable fechaHora y luego separa la hora con Time, ambos se guardan como caracter str para que coincida con varChar de la BD
        tabla.execute(sql)
        conex.commit()
        print("El comentario fue guardado correctamente\n")
        tabla.close()
    else:# no se permite el guardado del comentario si el usuario no existe, por la clave foranea 'usuario' que es necesario de la tabla usuarios
        print("Los datos ingresados son incorrectos\n")

def listar_comentarios(conex):
    nombre = input("Ingrese el nombre del usuario: ")
    apellido = input("Ingrese el apellido del usuario: ")
    tabla = conex.cursor()
    sql = 'select * from lopezfinal.comentarios ' \
        'where usuario in (select id_usuario from lopezfinal.usuarios where Nombre = "' +nombre+ '" and Apellido = "' +apellido+'") '\
        'order by fecha Desc'
    #primero realizo una consulta del usuario en la tabla 'usuarios' y selecciono su id. Segundo obtengo los comentarios del dicho usuario por medio de su id (id_usuario)
    tabla.execute(sql)
    lista = tabla.fetchall()
    print("----------------------------------------------------------------")
    print('Usuario     Texto        fecha           Hora        Noticia')
    print("----------------------------------------------------------------")
    if tabla.rowcount != 0: # ingreso en el if si el numero de filas es distinto de 0, para proceder a su impresion por cada posicion 
        for registro in lista:
            print(registro[1], " - ", registro[2], " - ", registro[3], " - ", registro[4], " - ", registro[5])
    else:# si el numero de filas es igual a cero imprimo el mensaje
        print("El Usuario no realizo ningun comentario")
    print("\n")
    tabla.close()

def menu():
    print("Examen Final Programacion I\n")
    print('1- Agregar usuarios')
    print('2- Borrar usuario')
    print('3- Cambiar email del usuario')
    print('4- Cargar comentarios')
    print('5- Lista de comentarios de un usuario')
    print('6- Salir\n')
    while True:
        opc = input('Ingrese la opción: ')
        if opc in ['1','2','3','4','5', '6']:
            break
        else:
            print('Opción mal ingresada, debe ser 1, 2, 3, 4, 5 o 6')
    return opc

try:# en el caso del error con la conexion con la Base de datos
    conexion1 = funciones.conectarse()
except mysql.connector.Error as e: #con la excepcion capto el error en el incorrecto ingreso de los datos de Locahost, root y contraseña
    print("Error de conexion MySQL -> ", e.msg)
else:# en el caso que la conexion sea correcta, se accede al Menu
    while True:
        opcion =menu()
        if opcion == '1':
            agregar_usuario(conexion1)
        elif opcion == '2':
            borrar_usuario(conexion1)
        elif opcion == '3':
            cambiar_email(conexion1)
        elif opcion == '4':
            carga_comentarios(conexion1)
        elif opcion == '5':
            listar_comentarios(conexion1)
        elif opcion == '6':
            print('Fin del menu')
            break
    
    conexion1.close()#cierro la conexion con la BD
