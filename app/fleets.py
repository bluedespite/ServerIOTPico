import pymysql
from datetime import datetime
from urllib.parse import urlparse
import json


#Administracion de Flotas de Vehiculos
def check_fleet(fleet):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM `FLEETS` WHERE Codigo_Flota=%s'
    cursor.execute(Query,(fleet['Codigo_Flota']))
    lon=cursor.rowcount
    if lon>0:
        return True
    else:
        return False

def save_fleet(fleet):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='INSERT INTO FLEETS (Codigo_Flota,Nombre_Flota,Codigo_Empresa,Centro_Costo) VALUES (%s,%s,%s,%s)'
    cursor.execute(Query,(fleet['Codigo_Flota'],fleet['Nombre_Flota'],fleet['Codigo_Empresa'],fleet['Centro_Costo']))
    connection.commit()
    cursor.close()
    connection.close()

def update_fleet(fleet):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='UPDATE FLEETS SET Codigo_Flota = %s, Nombre_Flota = %s, Codigo_Empresa = %s , Centro_Costo = %s WHERE Codigo_Flota = %s'
    cursor.execute(Query,(fleet['Codigo_Flota'],fleet['Nombre_Flota'],fleet['Codigo_Empresa'],fleet['Centro_Costo'],fleet['Codigo_Flota']))
    connection.commit()
    cursor.close()
    connection.close()

def get_fleet(fleet):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM FLEETS WHERE Codigo_Flota = %s '
    cursor.execute(Query,(fleet['Codigo_Flota']))
    data=cursor.fetchone()
    lon=cursor.rowcount
    cursor.close()
    connection.close()
    fleet = { 'Codigo_Flota':'','Nombre_Flota':'', 'Codigo_Empresa':'','Centro_Costo':''}
    if lon>0:
        fleet['Codigo_Flota']=data[1]
        fleet['Nombre_Flota']=data[2]
        fleet['Codigo_Empresa']=data[3]
        fleet['Centro_Costo']=data[4]
    return fleet
