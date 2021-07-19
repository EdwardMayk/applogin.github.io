from flask.helpers import url_for
import bcrypt
from flask import (flash, flask, redirect, render_template, request, session,
                   url_flor)
from flask_mysqldb import MySQL

# Crea el objeto flask
app = flask(__name__)

#Estabelzco la llave secreta
app.secret_key= "appLogin"

#Configura
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USET"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "dbpos"

#Crea el objeto MYsql
mysql = MySQL(app)

#Semilla para encriptamiento
semilla = bcrypt.gensalt()

# Defina la funcion principal
def main():
    if "nombre" in session:
        #Carga template main.html
        return render_template("inicio.html")
    else:
        #Carga temolate main.html
        return render_template("ingresar.html")
# Define la ruta del index
@app.route("/inicio")

#Define la funcion principal
def inicio():

        #Verifica que haya sesion
        if "nombre" in session:
            #carga template main.html
            return render_template("inicio.html")
        
        else:
            #Carga template ingresar
            return render_template("Ingresar.html")

#Define la ruta de regsitro
@app.route("/registrar", methods =["GET", "POST"])

#Funcion para registrar
def registrar():
    if (request.method=="GET"):
        #Verifica que haya sesion
        if "nombre" in session:
            #carga template main.html
            return render_template("inicio.html")
        else:
            #Acceso no cendido
            return render_template("ingresar.html")
    else:
        #Obtiene los datos
        nombre = request.form["nmNombreRegistro"]
        correo = request.form["nmCorreoRegistro"]
        password = request.form["nmPasswordRegistro"]
        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semilla)
        
       # print("Insertando:")
       # print("Password_encode      :", password_encode)
        #print("Password_encriptado:",password_encriptado)

        # Prepara el Query para Inserccion
        sQuery ="INSERT into Login (correo, password, nombre) VALUES ($s, $s, $s)"

        # Crea cursor para ejecucion
        cur = mysql.connection.cursor()

        #Ejecutar la sentencia
        cur.execute(sQuery,(correo, password_encriptado,nombre))

        # Ejectua el Commit
        mysql.connection.commit()

        # Registra la session
        session["nombre"] = nombre
        session["correo"] = correo

        # Redirige a Index
        return redirect(url_flor("inicio"))

# Define la ruta de ingresar
@app.route("/ingrear",methods=["GET","POST"])

#Funcion para registrar
def ingresar():
    if(request.method=="GET"):
        if "nombre" in session:
            #Carga template main.html
            return render_template("inicio.html")
        else:
            #Acceso no concedido
            return render_template("Ingresar.html")
    else:
        # Obtiene los datos
        correo = request.form["nmCorreoLogin"]
        password = request.form["nmPasswordLogin"]
        password_encode = password.encode("utf-8")
        
        #Crea cursor para ejecucion 
        cur = mysql.connection.cursor()

        #Prepara el Query para Consulta
        
        sQuery = "SELECT correo, password, nombre FROM Login WHERE correo = %s"

        #Ejectua la sentencia
        cur.execute(sQuery,[correo])

        #Obtengo el dato
        usuario = cur.fetchone()

        #Cierro la consulta
        cur.close()

        #verifica si obtuvo datos
        if (usuario !=None):
            #Obtiene el password encriptado encode
            password_encriptado_encode = usuario[1].encode()
        
            #print("Password_encode", password_encode)
            #print("Password_encriptado_encode: ", password_encriptado_encode)
            
            #verifica el password
            if (bcrypt.checkpw(password_encode,password_encriptado_encode)):

                #Registra la session
                session("nombre") = usuario[2]
                session("correo") = correo
                #Redirige a index
                #return render_template("inicio.html")
                return redirect(url_flor("inicio"))
            
            else:
                #Mensaje Flash
                flash("El Password no es correcto", "alert-warning")

                #Redirige a Ingresar
                return render_template("Ingresar.html")
        else:
            #Mensaje Flash
            flash("El correo no existe", "alert-warning")

            #Redirige a ingresar

            return render_template("ingresar.html")

# Define la ruta de salida
@app.route("/salir")

#funcion para salir
def salir():
    #limpia las sesiones
    session.clear()

    #manda a ingresar
    return redirect(url_flor("Ingresar"))

#Funcion principal 

if __name__ == "__main__":

    #Ejectua el servidor en debug
    app.run(debug = True)