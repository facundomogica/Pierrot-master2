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
class Helado:
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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS helados (
            codigo INT NOT NULL,
            gusto VARCHAR(255) NOT NULL,                
            categoria VARCHAR(255) NOT NULL)
            
            ''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def agregar_helado(self, codigo,gusto, categoria):
        # Verificamos si ya existe un producto con el mismo código
        self.cursor.execute(f"SELECT * FROM helados WHERE codigo = {codigo}")
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        sql = "INSERT INTO helados (codigo, gusto, categoria) VALUES (%s,%s, %s)"
        valores = (codigo,gusto, categoria)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True

    #----------------------------------------------------------------
    def consultar_helado(self, codigo):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM helados WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_helado(self, codigo,nuevo_gusto, nuevo_categoria):
        sql = "UPDATE helados SET  gusto = %s,categoria = %s WHERE codigo = %s"
        valores = (nuevo_gusto,nuevo_categoria, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_helados(self):
        self.cursor.execute("SELECT * FROM helados")
        helados = self.cursor.fetchall()
        return helados

    #----------------------------------------------------------------
    def eliminar_helado(self, codigo):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM helados WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def mostrar_helado(self, codigo):
        # Mostramos los datos de un producto a partir de su código
        helado = self.consultar_helado(codigo)
        if helado:
            print("-" * 40)
            print(f"Gusto........: {helado['gusto']}")
            print(f"Categoria........: {helado['categoria']}")
    

            print("-" * 40)
        else:
            print("Gusto no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase helado
helado = Helado(host='localhost', user='root', password='', database='miapp') 
""" helado = Catalogo(host='BasedeDatosPython.mysql.pythonanywhere-services.com', user='BasedeDatosPytho', password='1234sd4321', database='BasedeDatosPytho$default')  """
# Carpeta para guardar las imagenes.
#RUTA_DESTINO = './static/imagenes/'
helado.agregar_helado(1,"Crema Pierrot","Recomendamos")
helado.agregar_helado(2,"Flan completo","Recomendamos")
helado.agregar_helado(3,"Crema Mantecol","Recomendamos")
helado.agregar_helado(4,"Alfajor","Recomendamos")
helado.agregar_helado(5,"Milka","Recomendamos")
helado.agregar_helado(6,"Pistacho","Cremas soniadas")
helado.agregar_helado(7,"Crema del cielo","Cremas soniadas")
helado.agregar_helado(8,"Chocolate con almendras","Cremas soniadas")
helado.agregar_helado(9,"Vainilla","Cremas soniadas")
helado.agregar_helado(10,"Americana","Cremas soniadas")
helado.agregar_helado(11,"Tramontana","Cremas soniadas")
helado.agregar_helado(12,"Almendrado","Cremas soniadas")
helado.agregar_helado(13,"Dulce De Leche","Cremas soniadas")
helado.agregar_helado(14,"DDL Granizado","Cremas soniadas")
helado.agregar_helado(15,"DDL con nuez","Cremas soniadas")
helado.agregar_helado(16,"Súper DDL","Cremas soniadas")
helado.agregar_helado(17,"Dulce De Leche","Dulces placeres")
helado.agregar_helado(18,"Dulce De Leche","Dulces placeres")
helado.agregar_helado(19,"DDL Granizado","Dulces placeres")
helado.agregar_helado(20,"DDL con nuez","Dulces placeres")
helado.agregar_helado(21,"Chocolate","Chocolates perfectos")
helado.agregar_helado(22,"Chocolate blanco","Chocolates perfectos")
helado.agregar_helado(23,"Chocolate con almendras","Chocolates perfectos")
helado.agregar_helado(24,"Chocolate granizado","Chocolates perfectos")
helado.agregar_helado(25,"Chocolate granizado blanco","Chocolates perfectos")
helado.agregar_helado(26,"Chocolate con frutos rojos","Chocolates perfectos")
helado.agregar_helado(27,"Chocolate con nuez","Chocolates perfectos")
helado.agregar_helado(28,"Limón","Frutales")
helado.agregar_helado(29,"Frutilla","Frutales")
helado.agregar_helado(30,"Banana Split","Frutales")
helado.agregar_helado(31,"Durazno","Frutales")
helado.agregar_helado(32,"Kiwi y frutilla","Frutales")
helado.agregar_helado(33,"Ananá","Frutales")

#--------------------------------------------------------------------
@app.route("/helados", methods=["GET"])
def listar_helados():
    helados = helado.listar_helados()
    return jsonify(helados)


#--------------------------------------------------------------------
@app.route("/helados/<int:codigo>", methods=["GET"])
def mostrar_helado(codigo):
    helado = helado.consultar_helado(codigo)
    if helado:
        return jsonify(helado), 201
    else:
        return "Gusto no encontrado", 404



#--------------------------------------------------------------------
@app.route("/helados", methods=["POST"])
def agregar_helado():
    #Recojo los datos del form
    codigo = time.time()
    gusto = request.form['gusto']
    categoria = request.form['categoria']
    helado = helado.consultar_helado(codigo)    
 # Me aseguro que el producto exista
    helado = helado.consultar_helado(codigo)
    if not helado: # Si no existe el producto...
    #     # Genero el nombre de la imagen
    #     nombre_imagen = secure_filename(imagen.filename)
    #     nombre_base, extension = os.path.splitext(nombre_imagen)
    #     nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

        if helado.agregar_helado(codigo,gusto, categoria):
            # imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
            return jsonify({"mensaje": "Gusto agregado"}), 201
        else:
            return jsonify({"mensaje": "Ya existe"}), 400


#--------------------------------------------------------------------
@app.route("/helados/<int:codigo>", methods=["PUT"])
def modificar_helado(codigo):
    #Recojo los datos del form
    nuevo_gusto = request.form.get("gusto")
    nuevo_categoria = request.form.get("categoria")
    
    # Busco el producto guardado
    helado = helado = helado.consultar_helado(codigo)
    if helado: # Si existe el producto...
        # imagen_vieja = producto["imagen_url"]
        # # Armo la ruta a la imagen
        # ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe la borro.
        # if os.path.exists(ruta_imagen):
        #     os.remove(ruta_imagen)
    
        if helado.modificar_helado(codigo,nuevo_gusto,nuevo_categoria):
            return jsonify({"mensaje": "Gusto modificado"}), 200
        else:
            return jsonify({"mensaje": "Gusto no encontrado"}), 403


#--------------------------------------------------------------------
@app.route("/helados/<int:codigo>", methods=["DELETE"])
def eliminar_helado(codigo):
    # Busco el producto guardado
    helado = helado.consultar_helado(codigo)
    if helado: # Si existe el producto...
        # imagen_vieja = producto["imagen_url"]
        # # Armo la ruta a la imagen
        # ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # # Y si existe la borro.
        # if os.path.exists(ruta_imagen):
        #     os.remove(ruta_imagen)

        # Luego, elimina el producto del catálogo
        if helado.eliminar_helado(codigo):
            return jsonify({"mensaje": "helado eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el helado"}), 500
    

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)