import pymysql
from datetime import datetime
from urllib.parse import urlparse
import bcrypt
import json

#Login de usuarios
def val_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor= connection.cursor()
    Query="SELECT Password FROM `USERS` WHERE Email = %s"
    cursor.execute(Query,(user['Email']))
    e=cursor.fetchone()
    cursor.close()
    connection.close()    
    try:
        hashed=e[0].encode('UTF-8')
        return bcrypt.checkpw(user['Password'].encode('UTF-8'), hashed)
    except:
        return False
#Administracion de usuarios
def check_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM `USERS` WHERE Email=%s'
    cursor.execute(Query,(user['Email']))
    lon=cursor.rowcount
    if lon>0:
        return True
    else:
        return False

def save_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    password = user['Password'].encode('UTF-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    user['Hashed'] = hashed.decode('UTF-8')
    Query='INSERT INTO USERS (Nombre,Usuario, Password,Email,Telefono,Direccion,Empresa,Cargo, Rol) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(Query,(user['Nombre'],user['Usuario'],user['hashed'],user['Email'],user['Telefono'],user['Direccion'],user['Empresa'],user['Cargo'],user['Rol']))
    connection.commit()
    cursor.close()
    connection.close()
    message = {
            'status': 200,
            'message': 'OK',
            'data': 'Se insertó registro'
        }
    resp =  json.dumps(message, indent=4)
    return resp

def update_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    password = user['Npassword'].encode('UTF-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    user['hashed'] = hashed.decode('UTF-8')
    Query='UPDATE USERS SET Nombre = %s, Usuario = %s , Password = %s, Telefono = %s, Direccion = %s, Empresa = %s, Cargo = %s,  Rol = %s WHERE Email = %s'
    cursor.execute(Query,(user['Nombre'],user['Usuario'],user['hashed'],user['Telefono'],user['Direccion'],user['Empresa'],user['Cargo'],user['Rol'],user['Email']))
    connection.commit()
    cursor.close()
    connection.close()
    message = {
            'status': 200,
            'message': 'OK',
            'data': 'Se actualizó Registro'
        }
    resp =  json.dumps(message, indent=4)
    return resp

def get_user(user):
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query='SELECT * FROM USERS WHERE Email = %s '
    cursor.execute(Query,(user['Email']))
    data=cursor.fetchone()
    lon=cursor.rowcount
    cursor.close()
    connection.close()
    user = { 'Nombre':'','Usuario':'','Password':'','Email':'','Telefono':'','Direccion':'','Empresa':'','Cargo':'','Rol':''}
    if lon>0:
        user['Nombre']=data[1]
        user['Usuario']=data[2]
        user['Password']=data[3]
        user['Email']=data[4]
        user['Telefono']=data[5]
        user['Direccion']=data[6]
        user['Empresa']=data[7]
        user['Cargo']=data[8]
        user['Rol']=data[9]        
    message = {
        'status': 200,
        'message': 'OK',
        'data': user
    }
    resp =  json.dumps(message, indent=4)
    return resp
