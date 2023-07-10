import sqlite3

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
            Matrícula Nacional INTEGER PRIMARY KEY,
            Apellido-Nombre TEXT NOT NULL,
            DNI INTEGER NOT NULL,
            CUIT REAL NOT NULL
            Profesión TEXT NOT NULL,
            Celular INTEGER NOT NULL,
            mail INTEGER NOT NULL        
        ) ''')
    conn.commit()
    cursor.close()
    conn.close()

# Verificar si la base de datos existe, si no, crearla y crear la tabla
def create_database():
    print("Creando la BD...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

# Programa principal
# Crear la base de datos y la tabla Productos si no existen
create_database()


# -------------------------------------------------------------------
# Definimos la clase "Profesional"
# -------------------------------------------------------------------
class Profesional:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail):
        self.Matrícula = Matrícula           # Matrícula 
        self.ApellidoNombre = ApellidoNombre # ApellidoNombre
        self.DNI = DNI       # DNI 
        self.CUIT = CUIT          # CUIT
        self.Profesión = Profesión  # Profesion
        self.Celular = Celular # Celular
        self.mail = mail # mail

    # Este método permite modificar un profesional.
    def modificar(self, nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesión, nuevo_Celular, nuevo_Mail):
        self.ApellidoNombre = nuevo_ApellidoNombre  # Modifica El apellido y nombre
        self.DNI = nuevo_DNI        # Modifica el DNI
        self.CUIT = nuevo_CUIT            # Modifica el CUIT


# -------------------------------------------------------------------
# Definimos la clase "Inventario"
# -------------------------------------------------------------------
class Inventario:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_profesional(self, Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail):
        profesional_existente = self.consultar_profesional(Matrícula)
        if profesional_existente:
            print("Ya existe un profesional con esa Matrícula.")
            return False
        nuevo_profesional = Profesional(Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail)
        sql = f'INSERT INTO profesional VALUES ({Matrícula}, "{ApellidoNombre}", {DNI}, {CUIT}, "{Profesión}", {Celular}, "{mail}");'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True

    def consultar_profesional(self, Matrícula):
        sql = f'SELECT * FROM profesional WHERE Matrícula = {Matrícula};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail = row
            return Profesional(Matrícula, ApellidoNombre, DNI, CUIT,Profesión, Celular, mail )
        return False

    def modificar_profesional(self, Matrícula, nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesión, nuevo_Celular, nuevo_mail):
        Profesional = self.consultar_profesional(Matrícula)
        if Profesional:
            Profesional.modificar(nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesión, nuevo_Celular, nuevo_mail)
            sql = f'UPDATE Profesional SET Matrícula = "{nuevo_ApellidoNombre}", DNI = {nuevo_DNI}, CUIT = {nuevo_CUIT}, Profesión = {nueva_Profesión}, Celular = {nuevo_Celular}, mail = {nuevo_mail} WHERE Matrícula = {Matrícula};' 
            print("-"*50)
            print(f'Profesional modificado:\nMatrícula: {Profesional.Matrícula}\nApellidoNombre: {Profesional.ApellidoNombre}\nDNI: {Profesional.DNI}\nCUIT: {Profesional.CUIT}\nProfesión: {Profesional.Profesión}\nCelular: {Profesional.Celular}\nmail: {Profesional.mail}')
            self.cursor.execute(sql)
            self.conexion.commit()

    def eliminar_profesional(self, Matrícula):
        sql = f'DELETE FROM Profesional WHERE Matrícula = {Matrícula};' 
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'Profesional {Matrícula} eliminado.')
            self.conexion.commit()
        else:
            print(f'Profesional {Matrícula} no encontrado.')

    def listar_profesional(self):
        print("-"*50)
        print("INVENTARIO - Lista de Profesional:")
        print("Matrícula Nacional\tApellido-Nombre\tDNI\tCUIT\tProfesión\tCelular\tmail")
        self.cursor.execute("SELECT * FROM Profesional")
        rows = self.cursor.fetchall()
        for row in rows:
            Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail = row
            print(f'{Matrícula}\t{ApellidoNombre}\t{DNI}\t{CUIT}\t{Profesión}\t{Celular}\t{mail}')
        print("-"*50)



# -------------------------------------------------------------------
# Ejemplo de uso de las clases y objetos definidos antes:
# -------------------------------------------------------------------
# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()

# Crear una instancia de la clase Inventario
mi_inventario = Inventario()

# Crear una instancia de la clase Carrito
mi_carrito = Carrito()

# Crear 3 productos y agregarlos al inventario
mi_inventario.agregar_producto(1, 'Teclado USB 101 teclas', 10, 4500)
mi_inventario.agregar_producto(2, 'Mouse USB 3 botones', 5, 2500)
mi_inventario.agregar_producto(3, 'Monitor LCD 22 pulgadas', 15, 52500)

# Listar todos los productos del inventario
mi_inventario.listar_productos()

# Agregar 2 productos al carrito
mi_carrito.agregar(1, 2, mi_inventario) # Agregar 2 unidades del producto con código 1 al carrito
mi_carrito.agregar(3, 4, mi_inventario) # Agregar 1 unidad del producto con código 3 al carrito

# Listar todos los productos del carrito
mi_carrito.mostrar()

# Quitar 1 producto al carrito
mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del producto con código 1 al carrito

# Listar todos los productos del carrito
mi_carrito.mostrar()

# Mostramos el inventario
mi_inventario.listar_productos()















'''
# Clase inventario: Programa principal
# Crear una instancia de la clase Inventario
mi_inventario = Inventario() 

# Agregar productos 
mi_inventario.agregar_producto(1, 'Teclado USB 101 teclas', 10, 4500)
mi_inventario.agregar_producto(2, 'Mouse USB 3 botones', 5, 2500)
mi_inventario.agregar_producto(3, 'Monitor LCD 22 pulgadas', 15, 52500)
mi_inventario.agregar_producto(4, 'Monitor LCD 27 pulgadas', 25, 78500)
mi_inventario.agregar_producto(5, 'Mouse Pad color azul', 5, 500)

# Consultar un producto 
producto = mi_inventario.consultar_producto(30)
if producto != False:
    print(f'Producto encontrado:\nCódigo: {producto.codigo}\nDescripción: {producto.descripcion}\nCantidad: {producto.cantidad}\nPrecio: {producto.precio}')  
else:
    print("Producto no encontrado.")

# Modificar un producto 
mi_inventario.modificar_producto(3, 'Monitor LCD 24 pulgadas', 5, 62000)

# Listar todos los productos
mi_inventario.listar_productos()

# Eliminar un producto 
mi_inventario.eliminar_producto(2)

# Confirmamos que haya sido eliminado
mi_inventario.listar_productos()
'''


'''
# Programa principal
producto = Producto(1, 'Teclado USB 101 teclas', 10, 4500)
# Accedemos a los atributos del objeto
print(f'{producto.codigo} | {producto.descripcion} | {producto.cantidad} | {producto.precio}')
# Modificar los datos del producto
producto.modificar('Teclado Mecánico USB', 20, 4800) 
print(f'{producto.codigo} | {producto.descripcion} | {producto.cantidad} | {producto.precio}')
'''
