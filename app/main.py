from flask import Flask,request,redirect,url_for
from flask import render_template,session
import pymysql
from urllib.parse import urlparse
import json
import llaves
import bcrypt
import secrets

API_KEY=llaves.token.encode('UTF-8')
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(20)
f=open("database.env")
dbc = urlparse(f.read())
f.close()

def init_db():
    connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
	cursor=connection.cursor()
	Query="SHOW TABLES FROM MAIN_SENSOR"
	cursor.execute(Query)
	lon=cursor.rowcount
	if lon<=0:
		password = "12345"
		hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		Query="CREATE TABLE USER (NOMBRE TEXT NOT NULL, APELLIDO TEXT NOT NULL,EMAIL TEXT NOT NULL UNIQUE, PASSWORD TEXT NOT NULL, CARGO TEXT, AREA TEXT, EMPRESA TEXT, ROL TEXT NOT NULL);"
		cursor.execute(Query)	
		Query= "CREATE TABLE DATA ( `ID` INT PRIMARY KEY AUTO_INCREMENT , `FECHA_HORA` DATETIME NOT NULL,`TAG_SENSOR` TEXT NOT NULL,`UM` TEXT NOT NULL,`MEDIDA` FLOAT NOT NULL)"
		cursor.execute(Query)
		Query="INSERT INTO USER (NOMBRE,APELLIDO,EMAIL,PASSWORD,ROL) VALUES ('MIGUEL','AGUIRRE','miguelaguirreleon@gmail.com','%s','Administrador');" % hashed.decode('UTF-8')
		cursor.execute(Query)
		connection.commit()
	cursor.close()
	connection.close()
	return

def val_user(user):
	connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
	cursor= connection.cursor()
	Query="SELECT PASSWORD FROM `USER` WHERE email = %s"
	cursor.execute(Query,(user['email']))
	e=cursor.fetchone()
	cursor.close()
	connection.close()
	try:
		hashed=e[0].encode('UTF-8')
		return bcrypt.checkpw(user['password'].encode('UTF-8'), hashed)
	except:
		return False

def save_db(FECHA_HORA,TAG,UM,VALUE):
	connection=pymysql.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
	cursor=connection.cursor()
	Query='INSERT INTO DATA (`FECHA_HORA`,`TAG_SENSOR`,`UM`,`MEDIDA`) VALUES ( %s,%s,%s,%s)'
	cursor.execute(Query,(FECHA_HORA,TAG,UM,VALUE))
	connection.commit()
	cursor.close()
	connection.close()
	return

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/dashboard', methods=["GET","POST"])
def dashboard():
	if 'username' in session:
		return render_template('dashboard.html')
	else:
		if request.method=="POST":
			user={}
			user['email']=request.form.get("email")
			user['password']=request.form.get("password")
			if val_user(user):
				session['username']=user['email']
				user = {}
				return render_template('dashboard.html')
			else:
					return redirect(url_for('index'))
		else:
				return redirect(url_for('index'))


@app.route('/api', methods=["GET","POST"])
def api():
	init_db()
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
