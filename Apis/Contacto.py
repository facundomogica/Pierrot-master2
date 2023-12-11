#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
#from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------



app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Catalogo:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS contactos (
            codigo INT,
            DNI INT,                
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            mail VARCHAR(255) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            consulta VARCHAR(10) NOT NULL,
            suscripcion BOOLEAN NOT NULL NOT NULL)
            ''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def agregar_amigo(self, codigo,DNI, nombre, apellido, mail, telefono, consulta,suscripcion):
        # Verificamos si ya existe un producto con el mismo código
        self.cursor.execute(f"SELECT * FROM contactos WHERE codigo = {codigo}")
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        sql = "INSERT INTO contactos (codigo,DNI, nombre, apellido, mail, telefono, consulta,suscripcion) VALUES (%s,%s, %s, %s, %s, %s, %s,%s)"
        valores = (codigo,DNI, nombre, apellido, mail, telefono, consulta,suscripcion)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True

    #----------------------------------------------------------------
    def consultar_amigo(self, codigo):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM contactos WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_amigo(self, codigo,nuevo_DNI, nuevo_nombre, nuevo_apellido, nuevo_mail, nuevo_telefono, nuevo_consulta,nuevo_suscripcion):
        sql = "UPDATE contactos SET  DNI = %s,nombre = %s, apellido = %s, mail = %s, telefono = %s, consulta = %s, suscripcion= %s WHERE codigo = %s"
        valores = (nuevo_DNI,nuevo_nombre, nuevo_apellido, nuevo_mail, nuevo_telefono, nuevo_consulta,nuevo_suscripcion, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_amigos(self):
        self.cursor.execute("SELECT * FROM contactos")
        amigos = self.cursor.fetchall()
        return amigos

    #----------------------------------------------------------------
    def eliminar_amigo(self, codigo):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM contactos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def mostrar_amigo(self, codigo):
        # Mostramos los datos de un producto a partir de su código
        amigo = self.consultar_amigo(codigo)
        if amigo:
            print("-" * 40)
            print(f"DNI........: {amigo['DNI']}")
            print(f"Nombre........: {amigo['nombre']}")
            print(f"Apellido:.....: {amigo['apellido']}")
            print(f"Mail..........: {amigo['mail']}")
            print(f"Telefono......: {amigo['telefono']}")
            print(f"Consulta....: {amigo['consulta']}")
            print(f"Suscripto....: {amigo['suscripcion']}")
            print(f"Numero Amigo..: {amigo['codigo']}")

            print("-" * 40)
        else:
            print("Amigo no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
catalogo = Catalogo(host='localhost', user='root', password='', database='miapp') 
""" catalogo = Catalogo(host='BasedeDatosPython.mysql.pythonanywhere-services.com', user='BasedeDatosPytho', password='1234sd4321', database='BasedeDatosPytho$default')  """
# Carpeta para guardar las imagenes.
#RUTA_DESTINO = './static/imagenes/'

#--------------------------------------------------------------------
@app.route("/contactos", methods=["GET"])
def listar_amigos():
    amigos = catalogo.listar_amigos()
    return jsonify(amigos)


#--------------------------------------------------------------------
@app.route("/contactos/<int:codigo>", methods=["GET"])
def mostrar_amigo(codigo):
    amigo = catalogo.consultar_amigo(codigo)
    if amigo:
        return jsonify(amigo), 201
    else:
        return "Amigo no encontrado", 404



#--------------------------------------------------------------------
@app.route("/contactos", methods=["POST"])
def agregar_amigo():
    #Recojo los datos del form
    codigo = time.time()
    DNI = request.form['DNI']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    mail = request.form['mail']
    telefono = request.form['telefono']  
    consulta = request.form['consulta']
    suscripcion = request.form['suscripcion']
    # Me aseguro que el producto exista
    amigo = catalogo.consultar_amigo(codigo)
    if not amigo: # Si no existe el producto...
    #     # Genero el nombre de la imagen
    #     nombre_imagen = secure_filename(imagen.filename)
    #     nombre_base, extension = os.path.splitext(nombre_imagen)
    #     nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

        if catalogo.agregar_amigo(codigo,DNI, nombre, apellido, mail, telefono, consulta,suscripcion):
            # imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
            return jsonify({"mensaje": "Amigo agregado"}), 201
        else:
            return jsonify({"mensaje": "Ya existe"}), 400

#--------------------------------------------------------------------
@app.route("/contactos/<int:codigo>", methods=["PUT"])
def modificar_amigo(codigo):
    #Recojo los datos del form
    nuevo_DNI = request.form.get("DNI")
    nuevo_nombre = request.form.get("nombre")
    nuevo_apellido = request.form.get("apellido")
    nuevo_mail = request.form.get("mail")
    nuevo_telefono = request.form.get("telefono")
    nuevo_consulta = request.form.get("consulta")
    nuevo_suscripcion = request.form.get("suscripcion")
    # # Procesamiento de la imagen
    # nombre_imagen = secure_filename(imagen.filename)
    # nombre_base, extension = os.path.splitext(nombre_imagen)
    # nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    # imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

    # Busco el producto guardado
    amigo = amigo = catalogo.consultar_amigo(codigo)
    if amigo: # Si existe el producto...
        # imagen_vieja = producto["imagen_url"]
        # # Armo la ruta a la imagen
        # ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe la borro.
        # if os.path.exists(ruta_imagen):
        #     os.remove(ruta_imagen)
    
        if catalogo.modificar_amigo(codigo,nuevo_DNI, nuevo_nombre, nuevo_apellido, nuevo_mail, nuevo_telefono, nuevo_consulta,nuevo_suscripcion):
            return jsonify({"mensaje": "Amigo modificado"}), 200
        else:
            return jsonify({"mensaje": "Amigo no encontrado"}), 403


#--------------------------------------------------------------------
@app.route("/contactos/<int:codigo>", methods=["DELETE"])
def eliminar_amigo(codigo):
    # Busco el producto guardado
    amigo = catalogo.consultar_amigo(codigo)
    if amigo: # Si existe el producto...
        # imagen_vieja = producto["imagen_url"]
        # # Armo la ruta a la imagen
        # ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # # Y si existe la borro.
        # if os.path.exists(ruta_imagen):
        #     os.remove(ruta_imagen)

        # Luego, elimina el producto del catálogo
        if catalogo.eliminar_amigo(codigo):
            return jsonify({"mensaje": "Amigo eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el amigo"}), 500
    

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)