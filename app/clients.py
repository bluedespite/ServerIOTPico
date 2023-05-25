import pymysql
from datetime import datetime
from urllib.parse import urlparse
import json


#Administracion de clientes
def check_client(client):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM `CLIENTS` WHERE RUC=%s'
    cursor.execute(Query,(client['RUC']))
    lon=cursor.rowcount
    if lon>0:
        return True
    else:
        return False

def save_client(client):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='INSERT INTO CLIENTS (Nombre_Empresa,Direccion,RUC,Telefono_Contacto,Persona_Contacto,Email,Num_cuenta) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(Query,(client['Nombre_Empresa'],client['Direccion'],client['RUC'],client['Telefono_Contacto'],client['Persona_Contacto'],client['Email'],client['Num_cuenta']))
    connection.commit()
    cursor.close()
    connection.close()

def update_client(client):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='UPDATE CLIENTS SET Nombre_Empresa = %s, Direccion = %s , RUC = %s, Telefono_Contacto = %s, Persona_Contacto = %s, Email = %s, Num_cuenta = %s WHERE RUC = %s'
    cursor.execute(Query,(client['Nombre_Empresa'],client['Direccion'],client['RUC'],client['Telefono_Contacto'],client['Persona_Contacto'],client['Email'],client['Num_cuenta']))
    connection.commit()
    cursor.close()
    connection.close()

def get_client(client):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM CLIENTS WHERE RUC = %s '
    cursor.execute(Query,(client['RUC']))
    data=cursor.fetchone()
    lon=cursor.rowcount
    cursor.close()
    connection.close()
    client = { 'Nombre_Empresa':'','Direccion':'','RUC':'','Telefono_Contacto':'','Persona_Contacto':'','Email':'','Num_cuenta':''}
    if lon>0:
        client['Nombre_Empresa']=data[1]
        client['Direccion']=data[2]
        client['RUC']=data[3]
        client['Telefono_Contacto']=data[4]
        client['Persona_Contacto']=data[5]
        client['Email']=data[6]
        client['Num_cuenta']=data[7]
    return client
