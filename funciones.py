import mysql.connector
import getpass

def conectarse():
    host1= input("Ingrese el host: ")
    user1= input("Ingrese el usuario: ")
    passwd1= getpass.getpass("Ingrese el password: ")
    
    return mysql.connector.connect(host=host1,
                                   user=user1,
                                   passwd=passwd1)
