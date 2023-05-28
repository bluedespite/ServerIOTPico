import pymysql
from datetime import datetime
from urllib.parse import urlparse
import json


#Administracion de Vehiculos
def check_vehicle(vehicle):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM `VEHICLES` WHERE Numero_Placa=%s'
    cursor.execute(Query,(vehicle['Numero_Placa']))
    lon=cursor.rowcount
    if lon>0:
        return True
    else:
        return False

def save_vehicle(vehicle):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='INSERT INTO VEHICLES (Numero_Placa,Marca,Modelo,Tipo_Combustible,Capacidad_Tanque,Poliza,Vencimiento_Poliza,Codigo_Flota) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(Query,(vehicle['Numero_Placa'],vehicle['Marca'],vehicle['Modelo'],vehicle['Tipo_Combustible'],vehicle['Capacidad_Tanque'],vehicle['Poliza'],vehicle['Vencimiento_Poliza'],vehicle['Codigo_Flota']))
    connection.commit()
    cursor.close()
    connection.close()

def update_vehicle(vehicle):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='UPDATE VEHICLES SET Numero_Placa = %s, Marca = %s, Modelo = %s, Tipo_Combustible = %s, Capacidad_Tanque = %s, Poliza = %s, Vencimiento_Poliza = %s, Codigo_Flota = %s WHERE Codigo_Flota = %s'
    cursor.execute(Query,(vehicle['Numero_Placa'],vehicle['Marca'],vehicle['Modelo'],vehicle['Tipo_Combustible'],vehicle['Capacidad_Tanque'],vehicle['Poliza'],vehicle['Vencimiento_Poliza'],vehicle['Codigo_Flota']))
    connection.commit()
    cursor.close()
    connection.close()

def get_vehicle(vehicle):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM VEHICLES WHERE Numero_Placa = %s '
    cursor.execute(Query,(vehicle['Numero_Placa']))
    data=cursor.fetchone()
    lon=cursor.rowcount
    cursor.close()
    connection.close()
    vehicle= { 'Numero_Placa':'', 'Marca':'','Modelo':'', 'Tipo_Combustible':'','Capacidad_Tanque':'','Poliza':'','Vencimiento_Poliza':'','Codigo_Flota':''}
    if lon>0:
        vehicle['Numero_Placa']=data[1]
        vehicle['Marca']=data[2]
        vehicle['Modelo']=data[3]
        vehicle['Tipo_Combustible']=data[4]
        vehicle['Capacidad_Tanque']=data[5]
        vehicle['Poliza']=data[6]
        vehicle['Vencimiento_Poliza']=data[7]
        vehicle['Codigo_Flota']=data[8]
    return vehicle
