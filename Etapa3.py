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
    print("Creando tabla Profesional...") # Para probar que se ejecuta la función
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profesional (
            Matrícula INTEGER PRIMARY KEY,
            Apellido-Nombre TEXT NOT NULL,
            DNI INTEGER NOT NULL,
            CUIT REAL NOT NULL
            Profesión TEXT NOT NULL,
            Celular INTEGER NOT NULL,
            mail INTEGER NOT NULL 
                   
                   
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
    def __init__(self, Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail):
        self.Matrícula = Matrícula
        self.ApellidoNombre = ApellidoNombre
        self.DNI = DNI
        self.CUIT = CUIT
        self.Profesión = Profesión
        self.Celular = Celular
        self.mail = mail

    def modificar(self, nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesión, nuevo_Celular, nuevo_mail):
        self.ApellidoNombre = nuevo_ApellidoNombre
        self.DNI = nuevo_DNI
        self.CUIT = nuevo_CUIT
        self.Profesión = nueva_Profesión
        self.Celular = nuevo_Celular
        self.mail = nuevo_mail


# -------------------------------------------------------------------
# Definimos la clase "Inventario"
# -------------------------------------------------------------------
class Inventario:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_Profesional(self, Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail):
        Profesional_existente = self.consultar_Profesional(Matrícula)
        if Profesional_existente:
            return jsonify({'message': 'Ya existe un profesional con esa Matrícula.'}), 400

        #nuevo_Profesiona = Producto(codigo, descripcion, cantidad, precio)
        self.cursor.execute("INSERT INTO Profesional VALUES (?, ?, ?, ?)", (Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail))
        self.conexion.commit()
        return jsonify({'message': 'Profesional agregado correctamente.'}), 200

    def consultar_Profesional(self, Matrícula):
        self.cursor.execute("SELECT * FROM Profesional WHERE Matrícula = ?", (Matrícula,))
        row = self.cursor.fetchone()
        if row:
            Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail = row
            return Profesional(Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail)
        return None

    def modificar_Profesional(self, Matrícula, nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesión, nuevo_Celular, nuevo_mail):
        Profesional = self.consultar_Profesional(Matrícula)
        if Profesional:
            Profesional.modificar(nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesión, nuevo_Celular, nuevo_mail)
            self.cursor.execute("UPDATE Profesión SET ApellidoNombre = ?, DNI = ?, CUIT = ?, Profesión = ?, Celular = ?, mail = ? WHERE Matrícula = ?",
                                (nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesión, nuevo_Celular, nuevo_mail,  Matrícula))
            self.conexion.commit()
            return jsonify({'message': 'Profesional modificado correctamente.'}), 200
        return jsonify({'message': 'Profesional no encontrado.'}), 404

    def listar_productos(self):
        self.cursor.execute("SELECT * FROM Profesional")
        rows = self.cursor.fetchall()
        productos = []
        for row in rows:
            Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail = row
            Profesional = {'Matrícula': Matrícula, 'ApellidoNombre': ApellidoNombre, 'DNI': DNI, 'CUIT': CUIT, 'Profesión': Profesión, 'Celular': Celular, 'mail': mail}
            Profesional.append(Profesional)
        return jsonify(Profesional), 200

    def eliminar_Profesional(self, Matrícula):
        self.cursor.execute("DELETE FROM Profesional WHERE Matrícula = ?", (Matrícula,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Profesional eliminado correctamente.'}), 200
        return jsonify({'message': 'Profesioal no encontrado.'}), 404



# -------------------------------------------------------------------
# Configuración y rutas de la API Flask
# -------------------------------------------------------------------
#1)	Importación de los módulos y creación de la aplicación Flask

app = Flask(__name__)
CORS(app)

inventario = Inventario()   # Instanciamos un inventario

# 2 - Ruta para obtener los datos de un producto según su Matrícula
# GET: envía la información haciéndola visible en la URL de la página web.
@app.route('/Profesional/<int:Matrícuña>', methods=['GET'])
def obtener_Profesional(Matrícula):
    Profesional = inventario.consultar_Profesional(Matrícula)
    if Profesional:
        return jsonify({
            'Matrícula': Profesional.Matrícula,
            'ApellidoNombre': Profesional.ApellidoNombre,
            'DNI': Profesional.DNI,
            'CUIT': Profesional.CUIT,
            'Profesión': Profesional.Profesión,
            'Celular': Profesional.Celular,
            'mail': Profesional.mail


        }), 200
    return jsonify({'message': 'Profesional no encontrado.'}), 404

# 3 - Ruta para obtener la lista de Profesional del inventario
@app.route('/Profesional', methods=['GET'])
def obtener_Profesioanl():
    return inventario.listar_Profesional()

# 4 - Ruta para agregar un Profesional al inventario
# POST: envía la información ocultándola del usuario.
@app.route('/Profesional', methods=['POST'])
def agregar_Profesional():
    Matrícula = request.json.get('Matrícula')
    ApellidoNojmbre = request.json.get('ApellidoNombre')
    DNI = request.json.get('DNI')
    CUIT = request.json.get('CUIT')
    Profesión = request.json.get('Profesión')
    Celular = request.json.get('Celular')
    mail = request.json.get('mail')
    
    return inventario.agregar_Profesional(Matrícula, ApellidoNojmbre, DNI, CUIT, Profesión, Celular, mail)

# 5 - Ruta para modificar un Profesional del inventario
# PUT: permite actualizar información.
@app.route('/Profesional/<int:Matrícula>', methods=['PUT'])
def modificar_Profesional(Matrícula):
    nuevo_ApellidoNombre = request.json.get('ApellidoNombre')
    nuevo_DNI = request.json.get('DNI')
    nuevo_CUIT = request.json.get('CUIT')
    nueva_Profesión = request.json.get('Profesión')
    nuevo_Celular = request.json.get('Celular')
    nuevo_mail = request.json.get('mail')
    return inventario.modificar_Profesional(Matrícula, nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesión, nuevo_Celular, nuevo_mail )

# 6 - Ruta para eliminar un Profesional del inventario
# DELETE: permite eliminar información.
@app.route('/Profesional/<int:Matrícula>', methods=['DELETE'])
def eliminar_Profesional(Matrícula):
    return inventario.eliminar_Profesional(Matrícula)


# 7 - Ruta para obtener el index
@app.route('/')
def index():
    return 'API de Inventario'

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run()