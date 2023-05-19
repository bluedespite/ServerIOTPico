import pymysql
from urllib.parse import urlparse
import bcrypt

#Inicializa las tablas necesarias dentro del dispositivo
def init_db():    
    f=open("database.env")
    dbc = urlparse(f.read())
    f.close()
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query="SHOW TABLES FROM RORAIMA"
    cursor.execute(Query)
    lon=cursor.rowcount
    if lon<=0:
        password = "12345"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        Query= "CREATE TABLE CONF ( `ID` INT PRIMARY KEY AUTO_INCREMENT, `ID_ESTACION` TEXT NOT NULL ,`ESTACION` TEXT NOT NULL,`ID_TANQUE` TEXT NOT NULL,`TANQUE` TEXT NOT NULL,`PRODUCTO` TEXT NOT NULL,`DENSIDAD` TEXT NOT NULL,`TAG_SENSOR` TEXT NOT NULL UNIQUE,`DESCRIPCION` TEXT NOT NULL,`UM` TEXT NOT NULL, `RANGO_MIN` FLOAT NOT NULL, `RANGO_MAX` FLOAT NOT NULL, `TIPO` TEXT NOT NULL,`DIRECCION` TEXT NOT NULL, `MASCARA` TEXT NOT NULL, `PUERTO` TEXT NOT NULL,`ID_COMM` TEXT NOT NULL,`SERIAL` TEXT NOT NULL,`LINEAR` TEXT NOT NULL,`ENABLE` TEXT NOT NULL)"
        cursor.execute(Query)
        Query= "CREATE TABLE DATA ( `ID` INT PRIMARY KEY AUTO_INCREMENT , `FECHA_HORA` DATETIME NOT NULL,`TAG_SENSOR` TEXT NOT NULL,`UM` TEXT NOT NULL,`MEDIDA` FLOAT NOT NULL, `VELOCIDAD` FLOAT NOT NULL, `LATITUD` FLOAT NOT NULL,`LONGITUD` FLOAT NOT NULL,`SALE` FLOAT NOT NULL,`DELIVERY` FLOAT NOT NULL)"
        cursor.execute(Query)
        Query="CREATE TABLE USERS (ID_USUARIO INT PRIMARY KEY AUTO_INCREMENT,Nombre VARCHAR(255) NOT NULL,Usuario VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL, Telefono VARCHAR(255) DEFAULT 'N/A', Direccion VARCHAR(255) DEFAULT 'N/A', Empresa VARCHAR(255) NOT NULL, Cargo VARCHAR(255) NOT NULL, Rol VARCHAR(255) NOT NULL, Fecha_Registro DATE DEFAULT CURRENT_DATE, Ultimo_Inicio_Sesion DATETIME DEFAULT CURRENT_TIMESTAMP);"
        cursor.execute(Query)
        Query="CREATE TABLE CONX (NOMBRE TEXT NOT NULL UNIQUE, DIRECCION TEXT NOT NULL, ENABLE TEXT NOT NULL);"
        cursor.execute(Query)
        Query="INSERT INTO USERs (Nombre,Usuario,Password,Email,Telefono,Direccion,Empresa,Cargo,Rol) VALUES ('Miguel Angel Aguirre','mikeatthebass','%s','miguelaguirreleon@gmail.com','N/A','N/A','Dev','Developer','Administrador');" % hashed.decode('UTF-8')
        cursor.execute(Query)
        connection.commit()
        import test
    cursor.close()
    connection.close()  

