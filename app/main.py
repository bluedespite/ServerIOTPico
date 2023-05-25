from flask import Flask,request,redirect,url_for
from flask import render_template,session

import secrets
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(20)

from datetime import datetime
from init import *
from auth import *
from clients import *
from stations import *

from nodo import *
from config import *
from graf import *

import llaves
API_KEY=llaves.token.encode('UTF-8')

#Funciones Basicas de configuracion
user = { 'Nombre':'','Usuario':'','Password':'','Email':'','Telefono':'','Direccion':'','Empresa':'','Cargo':'','Rol':''}
client = { 'Nombre_Empresa':'','Direccion':'','RUC':'','Telefono':'','Persona_Contacto':'','Email':'','Num_cuenta':''}
station = { 'Nombre_Estacion':'', 'Tipo_Estacion':'','Direccion':'','Coordenadas':''}
CONF = {'ID':'', 'ID_ESTACION': '','ESTACION': '', 'ID_TANQUE':'','TANQUE':'', 'PRODUCTO':'', 'DENSIDAD':'', 'TAG_SENSOR':'','DESCRIPCION':'','UM':'', 'RANGO_MIN':'', 'RANGO_MAX':'','TIPO':'','DIRECCION':'','MASCARA':'','PUERTO':'','ID_COMM':'','SERIAL':'','LINEAR':'','ENABLE':'' }
DATA = {'ID':'', 'FECHA_HORA': '','TAG_SENSOR': '', 'MEDIDA':'', 'UM':'','VELOCIDAD':'','LATITUD':'', 'LONGITUD':'', 'SALE':'', 'DELIVERY':'' }
CONX = { 'NOMBRE':'','DIRECCION':'','ENABLE':''}
     

#Tablas de Rutas
@app.route('/')
@app.route('/index')
def index():
    init_db()
    return render_template('index.html')

@app.route('/dashboard', methods=["GET","POST"])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        if request.method=="POST":
            user={}
            user['Email']=request.form.get("Email")
            user['Password']=request.form.get("Password")
            if val_user(user):
                session['username']=user['Email']
                user = {}
                return render_template('dashboard.html')
            else:
                return redirect(url_for('index'))
        else:
                return redirect(url_for('index'))

@app.route('/saveconf', methods=["GET","POST"])
def saveconf():
    if request.method=="POST":
        CONF['ID_ESTACION']=request.form.get("ID_ESTACION")
        CONF['ESTACION']=request.form.get("ESTACION")
        CONF['ID_TANQUE']=request.form.get("ID_TANQUE")
        CONF['TANQUE']=request.form.get("TANQUE")
        CONF['PRODUCTO']=request.form.get("PRODUCTO")
        CONF['DENSIDAD']=request.form.get("DENSIDAD")
        CONF['TAG_SENSOR']=request.form.get("TAG_SENSOR")
        CONF['DESCRIPCION']=request.form.get("DESCRIPCION")
        CONF['UM']=request.form.get("UM")
        CONF['TIPO']=request.form.get("TIPO")
        CONF['RANGO_MIN']=request.form.get("RANGO_MIN")
        CONF['RANGO_MAX']=request.form.get("RANGO_MAX")
        CONF['DIRECCION']=request.form.get("DIRECCION")
        CONF['MASCARA']=request.form.get("MASCARA")
        CONF['PUERTO']=request.form.get("PUERTO")
        CONF['ID_COMM']=request.form.get("ID_COMM")
        CONF['SERIAL']=request.form.get("SERIAL")
        CONF['LINEAR']=request.form.get("LINEAR")       
        CONF['ENABLE']=request.form.get("ENABLE")
        if check_conf(CONF):
            return update_conf(CONF)
        else:
            return save_conf(CONF)
    else:
        message = {
            'status': 404,
            'message': 'FAIL',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/getconf', methods=["GET","POST"])
def getconf():
    if request.method=="POST":
        CONF['TAG_SENSOR']=request.form.get("TAG_SENSOR")
        return get_conf(CONF)
    else:
        message = {
            'status': 404,
            'message': 'FAIL',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/main_clientes')
def main_clientes():
    if 'username' in session:
        return render_template('main_clientes.html')
    else:
        return redirect(url_for('index'))  

@app.route('/view_client', methods=["GET","POST"])
def view_client():
    if 'username' in session:
        if request.method=="POST":
            client = { 'Nombre_Empresa':'','Direccion':'','RUC':'','Telefono':'','Persona_Contacto':'','Email':'','Num_cuenta':''}
            client['RUC']=request.form.get("RUC")
            if check_client(client):
                client=get_client(client)
            return render_template('view_client.html', client=client)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
 
@app.route('/new_client', methods=["GET","POST"])
def new_client():
    if 'username' in session:
        client = { 'Nombre_Empresa':'','Direccion':'','RUC':'','Telefono':'','Persona_Contacto':'','Email':'','Num_cuenta':''}
        return render_template('view_user.html', client=client)
    else:
        return redirect(url_for('index'))
    
@app.route('/saveclient', methods=["GET","POST"])
def saveclient():
    if 'username' in session:
        if request.method=="POST":
            client['Nombre_Empresa']=request.form.get("Nombre_Empresa")
            client['Direccion']=request.form.get("Direccion")
            client['RUC']=request.form.get("RUC")
            client['Telefono_Contacto']=request.form.get("Telefono_Contacto")
            client['Persona_Contacto']=request.form.get("Persona_Contacto")
            client['Email']=request.form.get("Email")
            client['Num_cuenta']=request.form.get("Num_cuenta")
            if check_client(client):
                update_client(client)
            else:
                save_client(client)
            return redirect(url_for('main_clientes'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/main_usuarios')
def main_usuarios():
    if 'username' in session:
        return render_template('main_usuarios.html')
    else:
        return redirect(url_for('index'))

@app.route('/view_user', methods=["GET","POST"])
def view_user():
    if 'username' in session:
        if request.method=="POST":
            user = { 'Nombre':'','Usuario':'','Password':'','Email':'','Telefono':'','Direccion':'','Empresa':'','Cargo':'','Rol':'Usuario'}
            user['Email']=request.form.get("Email")
            if check_user(user):
                user=get_user(user)
            else:
                user = { 'Nombre':'','Usuario':'','Password':'','Email':'','Telefono':'','Direccion':'','Empresa':'','Cargo':'','Rol':'Usuario'}
            return render_template('view_user.html', user=user)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/new_user', methods=["GET","POST"])
def new_user():
    if 'username' in session:
        user = { 'Nombre':'','Usuario':'','Password':'','Email':'','Telefono':'','Direccion':'','Empresa':'','Cargo':'','Rol':'Usuario'}
        return render_template('view_user.html', user=user)
    else:
        return redirect(url_for('index'))

@app.route('/saveuser', methods=["GET","POST"])
def saveuser():
    if 'username' in session:
        if request.method=="POST":
            user['Nombre']=request.form.get("Nombre")
            user['Usuario']=request.form.get("Usuario")
            user['Password']=request.form.get("Password")
            user['Npassword']=request.form.get("Npassword")
            user['Email']=request.form.get("Email")
            user['Telefono']=request.form.get("Telefono")
            user['Direccion']=request.form.get("Direccion")
            user['Empresa']=request.form.get("Empresa")
            user['Cargo']=request.form.get("Cargo")
            user['Rol']=request.form.get("Rol")
            if user['Password']==user['Npassword']:
                if check_user(user):
                    update_user(user)
                else:
                    save_user(user)
            return redirect(url_for('main_usuarios'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/main_estaciones')
def main_estaciones():
    if 'username' in session:
        return render_template('main_estaciones.html')
    else:
        return redirect(url_for('index'))  

@app.route('/view_estacion', methods=["GET","POST"])
def view_estacion():
    if 'username' in session:
        if request.method=="POST":
            station = { 'Codigo_Estacion':'','Nombre_Estacion':'', 'Tipo_Estacion':'','Direccion':'','Coordenadas':'','Responsable_Estacion':'','Telefono_Responsable':'','Email':''}
            station['Codigo_Estacion']=request.form.get("Codigo_Estacion")
            if check_client(station):
                client=get_client(station)
            return render_template('view_station.html', station=station)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/new_estacion', methods=["GET","POST"])
def new_estacion():
    if 'username' in session:
        station = { 'Codigo_Estacion':'','Nombre_Estacion':'', 'Tipo_Estacion':'','Direccion':'','Coordenadas':'','Responsable_Estacion':'','Telefono_Responsable':'','Email':''}
        return render_template('view_station.html', station=station)
    else:
        return redirect(url_for('index'))
    
@app.route('/savestation', methods=["GET","POST"])
def savestation():
    if 'username' in session:
        if request.method=="POST":
            station['Codigo_Estacion']=request.form.get("Codigo_Estacion")
            station['Nombre_Estacion']=request.form.get("Nombre_Estacion")
            station['Tipo_Estacion']=request.form.get("Tipo_Estacion")
            station['Direccion']=request.form.get("Direccion")
            station['Coordenadas']=request.form.get("Coordenadas")
            station['Responsable_Estacion']=request.form.get("Responsable_Estacion")
            station['Telefono_Responsable']=request.form.get("Telefono_Responsable")
            station['Email']=request.form.get("Email")
            if check_station(station):
                update_station(station)
            else:
                save_station(station)
            return redirect(url_for('main_estaciones'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/configuracion')
def configuracion():
    if 'username' in session:
        return render_template('configuracion.html')
    else:
        return redirect(url_for('index'))

@app.route('/nodos')
def nodos():
    if 'username' in session:
        return render_template('nodos.html')
    else:
        return redirect(url_for('index'))



@app.route('/getnodo', methods=["GET","POST"])
def getnodo():
    if 'username' in session:
        if request.method=="POST":
            CONX['NOMBRE']=request.form.get("NOMBRE")
            return get_nodo(CONX)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/savenodo', methods=["GET","POST"])
def savenodo():
    if 'username' in session:
        if request.method=="POST":
            CONX['NOMBRE']=request.form.get("NOMBRE")
            CONX['DIRECCION']=request.form.get("DIRECCION")
            CONX['ENABLE']=request.form.get("ENABLE")
            if check_nodo(CONX):
                return update_nodo(CONX)
            else:
                return save_nodo(CONX)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 'Actualizacion Fallida'
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)



@app.route('/getchardata', methods=["GET","POST"])
def getchardata():
    if 'username' in session:
        if request.method=="POST":
            fecha_inicio=request.form.get('fecha_inicio')
            fecha_fin=request.form.get('fecha_fin')
            return get_chartdata(fecha_inicio,fecha_fin)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)


@app.route('/getbardata', methods=["GET","POST"])
def getbardata():
    if 'username' in session:
        if request.method=="POST":
            fecha_inicio=request.form.get('fecha_inicio')
            fecha_fin=request.form.get('fecha_fin')
            return get_bardata(fecha_inicio,fecha_fin)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/getgeomapdata', methods=["GET","POST"])
def getgeomapdata():
    if 'username' in session:
        if request.method=="POST":
            fecha_inicio=request.form.get('fecha_inicio')
            fecha_fin=request.form.get('fecha_fin')
            return get_geomap(fecha_inicio,fecha_fin)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)
    
@app.route('/api', methods=["GET","POST"])
def api():
	if request.method=="POST":
		datos=request.json
		print(datos)
		hashed=datos['token']
		if (bcrypt.checkpw(API_KEY,hashed.encode('UTF-8'))):
			datos['token']=bcrypt.hashpw(API_KEY, bcrypt.gensalt()).decode('UTF-8')
			save_db(datos['date_time'],'TI60001','°C',datos['temperature'])
			message = {
			'status': 200,
			'message': 'SUCCESS',
			'data': datos
			}
		else:
			message = {
			'status': 404,
			'message': 'FAIL',
			'data': 0
			}
	else:
		message = {
		'status': 404,
		'message': 'FAIL',
		'data': 0
		}
	return json.dumps(message, indent=4)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
