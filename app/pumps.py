import pymysql
from datetime import datetime
from urllib.parse import urlparse
import json


#Administracion de Surtidores
def check_pump(pump):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM `PUMPS` WHERE Codigo_Surtidor=%s'
    cursor.execute(Query,(pump['Codigo_Surtidor']))
    lon=cursor.rowcount
    if lon>0:
        return True
    else:
        return False

def save_pump(pump):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='INSERT INTO PUMPS (Codigo_Surtidor,Codigo_Estacion,Status,Ultimo_Mantenimiento,Codigo_Proveedor,Codigo_Operador) VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(Query,(pump['Codigo_Surtidor'],pump['Codigo_Estacion'],pump['Status'],pump['Ultimo_Manteniminto'],pump['Codigo_Proveedor'],pump['Codigo_Operador']))
    connection.commit()
    cursor.close()
    connection.close()

def update_pump(pump):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='UPDATE PUMPS SET Codigo_Surtidor = %s, Codigo_Estacion = %s, Status = %s , Ultimo_Mantenimiento = %s, Codigo_Proveedor = %s, Codigo_Operador = %s, WHERE Codigo_Surtidor = %s'
    cursor.execute(Query,(pump['Codigo_Surtidor'],pump['Codigo_Estacion'],pump['Status'],pump['Ultimo_Mantenimiento'],pump['Codigo_Proveedor'],pump['Codigo_Operador']))
    connection.commit()
    cursor.close()
    connection.close()

def get_pump(pump):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM PUMPS WHERE Codigo_Surtidor = %s '
    cursor.execute(Query,(pump['Codigo_Surtidor']))
    data=cursor.fetchone()
    lon=cursor.rowcount
    cursor.close()
    connection.close()
    pump= { 'Codigo_Surtidor':'','Codigo_Estacion':'','Status':'','Ultimo_Mantenimiento:':'','Codigo_Proveedor':'','Codigo_Operador':''}
    if lon>0:
        pump['Codigo_Surtidor']=data[1]
        pump['Codigo_Estacion']=data[2]
        pump['Status']=data[3]
        pump['Ultimo_Mantenimiento']=data[4]
        pump['Codigo_Proveedor']=data[5]
        pump['Codigo_Operador']=data[6]
    return pump
