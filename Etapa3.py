import sqlite3
from flask import Flask,  jsonify, request
from flask_cors import CORS


# Configurar la conexión a la base de datos SQLite
DATABASE = 'inventario.db'

def get_db_connection():
    print("Obteniendo conexión...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla 'Profesional' si no existe
def create_table():
    print("Creando tabla Profesionales...") # Para probar que se ejecuta la función
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profesional (
            matricula INTEGER PRIMARY KEY,
            apellido_nombre TEXT NOT NULL,
            dni INTEGER NOT NULL,
            cuit INTEGER NOT NULL,
            profesion TEXT NOT NULL,
            celular INTEGER NOT NULL,
            mail TEXT NOT NULL          
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Verificar si la base de datos existe, si no, crearla y crear la tabla
def create_database():
    print("Creando la BD...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

# Crear la base de datos y la tabla si no existen
create_database()

# -------------------------------------------------------------------
# Definimos la clase "Profesional"
# -------------------------------------------------------------------
class Profesional:
    def __init__(self, matricula, apellidoNombre, dni, cuit, profesion, celular, mail):
        self.matricula = matricula
        self.apellidoNombre = apellidoNombre
        self.dni = dni
        self.cuit = cuit
        self.profesion = profesion
        self.celular = celular
        self.mail = mail

    def modificar(self, nuevo_apellidoNombre, nuevo_dni, nuevo_cuit, nueva_profesion, nuevo_celular, nuevo_mail):
        self.apellidoNombre = nuevo_apellidoNombre
        self.dni = nuevo_dni
        self.cuit = nuevo_cuit
        self.profesion = nueva_profesion
        self.celular = nuevo_celular
        self.mail = nuevo_mail


# -------------------------------------------------------------------
# Definimos la clase "Inventario"
# -------------------------------------------------------------------
class Inventario:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_profesional(self, matricula, apellidoNombre, dni, cuit, profesion, celular, mail):
        profesional_existente = self.consultar_profesional(matricula)
        if profesional_existente:
            return jsonify({'message': 'Ya existe un profesional con esa matricula.'}), 400

        self.cursor.execute("INSERT INTO profesional VALUES (?, ?, ?, ?, ?, ?, ?)", (matricula, apellidoNombre, dni, cuit, profesion, celular, mail))
        self.conexion.commit()
        return jsonify({'message': 'Profesional agregado correctamente.'}), 200

    def consultar_profesional(self, matricula):
        self.cursor.execute("SELECT * FROM profesional WHERE matricula = ?", (matricula))
        row = self.cursor.fetchone()
        if row:
            matricula, apellidoNombre, dni, cuit, profesion, celular, mail = row
            return Profesional(matricula, apellidoNombre, dni, cuit, profesion, celular, mail)
        return None

    def modificar_profesional(self, matricula, nuevo_apellidoNombre, nuevo_dni, nuevo_cuit, nueva_profesion, nuevo_celular, nuevo_mail):
        profesional = self.consultar_profesional(matricula)
        if profesional:
            profesional.modificar(nuevo_apellidoNombre, nuevo_dni, nuevo_cuit, nueva_profesion, nuevo_celular, nuevo_mail)
            self.cursor.execute("UPDATE profesion SET apellidoNombre = ?, dni = ?, cuit = ?, profesion = ?, celular = ?, mail = ? WHERE matricula = ?",
                                (nuevo_apellidoNombre, nuevo_dni, nuevo_cuit, nueva_profesion, nuevo_celular, nuevo_mail,  matricula))
            self.conexion.commit()
            return jsonify({'message': 'Profesional modificado correctamente.'}), 200
        return jsonify({'message': 'Profesional no encontrado.'}), 404

    def listar_productos(self):
        self.cursor.execute("SELECT * FROM profesional")
        rows = self.cursor.fetchall()
        profesional = []
        for row in rows:
            matricula, apellidoNombre, dni, cuit, profesion, celular, mail = row
            profesional = {'matricula': matricula, 'apellidoNombre': apellidoNombre, 'dni': dni, 'cuit': cuit, 'profesion': profesion, 'celular': celular, 'mail': mail}
            profesional.append(profesional)
        return jsonify(profesional), 200

    def eliminar_Profesional(self, matricula):
        self.cursor.execute("DELETE FROM profesional WHERE matricula = ?", (matricula))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Profesional eliminado correctamente.'}), 200
        return jsonify({'message': 'Profesional no encontrado.'}), 404



# -------------------------------------------------------------------
# Configuración y rutas de la API Flask
# -------------------------------------------------------------------
#1)	Importación de los módulos y creación de la aplicación Flask

app = Flask(__name__)
CORS(app)

inventario = Inventario()   # Instanciamos un inventario

# 2 - Ruta para obtener los datos de un producto según su matricula
# GET: envía la información haciéndola visible en la URL de la página web.
@app.route('/profesional/<int:matricula>', methods=['GET'])
def obtener_profesional(matricula):
    profesional = inventario.consultar_profesional(matricula)
    if profesional:
        return jsonify({
            'matricula': profesional.matricula,
            'apellidoNombre': profesional.apellidoNombre,
            'dni': profesional.dni,
            'cuit': profesional.cuit,
            'profesion': profesional.profesion,
            'celular': profesional.celular,
            'mail': profesional.mail
        }), 200
    return jsonify({'message': 'Profesional no encontrado.'}), 404

# 3 - Ruta para obtener la lista de Profesional del inventario
@app.route('/profesional', methods=['GET'])
def obtener_profesional():
    return inventario.listar_profesional()

# 4 - Ruta para agregar un Profesional al inventario
# POST: envía la información ocultándola del usuario.
@app.route('/profesional', methods=['POST'])
def agregar_profesional():
    matricula = request.json.get('matricula')
    apellidoNombre = request.json.get('apellidoNombre')
    dni = request.json.get('dni')
    cuit = request.json.get('cuit')
    profesion = request.json.get('profesion')
    celular = request.json.get('celular')
    mail = request.json.get('mail')
    
    return inventario.agregar_profesional(matricula, apellidoNombre, dni, cuit, profesion, celular, mail)

# 5 - Ruta para modificar un Profesional del inventario
# PUT: permite actualizar información.
@app.route('/profesional/<int:matricula>', methods=['PUT'])
def modificar_profesional(matricula):
    nuevo_apellidoNombre = request.json.get('apellidoNombre')
    nuevo_dni = request.json.get('dni')
    nuevo_cuit = request.json.get('cuit')
    nueva_profesion = request.json.get('profesion')
    nuevo_celular = request.json.get('celular')
    nuevo_mail = request.json.get('mail')
    return inventario.modificar_profesional(matricula, nuevo_apellidoNombre, nuevo_dni, nuevo_cuit, nueva_profesion, nuevo_celular, nuevo_mail )

# 6 - Ruta para eliminar un Profesional del inventario
# DELETE: permite eliminar información.
@app.route('/productos/<int:codigo>', methods=['DELETE'])
def eliminar_producto(codigo):
    return inventario.eliminar_producto(codigo)

# 7 - Ruta para agregar un producto al carrito
@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    return carrito.agregar(codigo, cantidad, inventario)

# 8 - Ruta para quitar un producto del carrito
@app.route('/carrito', methods=['DELETE'])
def quitar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    return carrito.quitar(codigo, cantidad, inventario)

# 9 - Ruta para obtener el contenido del carrito
@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return carrito.mostrar()

# 10 - Ruta para obtener el index
@app.route('/')
def index():
    return 'API de Inventario'

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run()