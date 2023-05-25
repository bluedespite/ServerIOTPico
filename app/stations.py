import pymysql
from datetime import datetime
from urllib.parse import urlparse
import json


#Administracion de clientes
def check_station(station):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM `STATIONS` WHERE Codigo_Estacion=%s'
    cursor.execute(Query,(station['Codigo_Estacion']))
    lon=cursor.rowcount
    if lon>0:
        return True
    else:
        return False

def save_station(station):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='INSERT INTO STATIONS (Codigo_Estacion,Nombre_Estacion,Tipo_Estacion,Direccion,Coordenadas,Responsable_Estacion,Telefono_Responsable,Email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(Query,(station['Codigo_Estacion'],station['Nombre_Estacion'],station['Tipo_Estacion'],station['Direccion'],station['Coordenadas'],station['Responsable_Estacion'],station['Telefono_Responsable'],station['Email']))
    connection.commit()
    cursor.close()
    connection.close()

def update_station(station):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='UPDATE CLIENTS SET Codigo_Estacion = %s,Nombre_Estacion = %s, Tipo_Estacion = %s , Direccion = %s, Coordenadas = %s, Responsable_Estacion = %s, Telefono_Responsable = %s, Email = %s WHERE Codigo_Estacion = %s'
    cursor.execute(Query,(station['Codigo_Estacion'],station['Nombre_Estacion'],station['Tipo_Estacion'],station['Direccion'],station['Coordenadas'],station['Responsable_Estacion'],station['Telefono_Responsable'],station['Email'],station['Codigo_Estacion']))
    connection.commit()
    cursor.close()
    connection.close()

def get_station(station):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM STATIONS WHERE Codigo_Estacion = %s '
    cursor.execute(Query,(client['Codigo_Estacion']))
    data=cursor.fetchone()
    lon=cursor.rowcount
    cursor.close()
    connection.close()
    station= { 'Codigo_Estacion':'','Nombre_Estacion':'','Tipo_Estacion':'','Direccion:':'','Coordenadas':'','Responsable':'','Telefono_Responsable':'','Email':''}
    if lon>0:
        station['Codigo_Estacion']=data[1]
        station['Nombre_Estacion']=data[2]
        station['Tipo_Estacion']=data[3]
        station['Direccion']=data[4]
        station['Coordenadas']=data[5]
        station['Responsable_Estacion']=data[6]
        station['Telefono_Responsable']=data[7]
        station['Email']=data[8]     
    return station
