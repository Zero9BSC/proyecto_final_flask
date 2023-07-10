# -------------------------------------------------------------------
# Definimos la clase "Profesional"
# -------------------------------------------------------------------
class Profesional:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, Matrícula, ApellidoNombre, DNI, CUIT, Profesión, Celular, mail):
        self.Matrícula = Matrícula          # Matricula Nacional
        self.ApellidoNombre = ApellidoNombre # Apellido-Nombre
        self.DNI = DNI       # DNI
        self.CUIT = CUIT          # CUIT
        self.Profesión = Profesión           # Profesión
        self.Celular = Celular          # Celular
        self.mail = mail           # Mail

    # Este método permite modificar el profesional.
    def modificar(self, nueva_Matrícula, nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesión, nuevo_Celular, nuevo_mail):
        self.Matrícula = nueva_Matrícula  # Modifica la Matricula
        self.ApellidoNombre = nuevo_ApellidoNombre       # Modifica el Apellido y Nombre
        self.DNI = nuevo_DNI            # Modifica el DNI
        self.CUIT = nuevo_CUIT           # Modifica el CUIT
        self.Profesión = nueva_Profesión            # Modifica la profesion
        self.Celular = nuevo_Celular            # Modifica el Celular
        self.mail = nuevo_mail           # Modifica Mail


# -------------------------------------------------------------------
# Definimos la clase "Inventario"
# El inventario gestiona una lista de productos.
# -------------------------------------------------------------------
class Inventario:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.Profesional = []  # Lista de profesional en el inventario (variable de clase)


    # Este método permite crear objetos de la clase "Profesional" y
    # agregarlos al inventario.
    def agregar_Profesional(self, Matrícula, ApellidoNombre, DNI, CUIT, Profesíon, Celular, mail):
        nuevo_Profesional = Profesional(Matrícula, ApellidoNombre, DNI, CUIT, Profesíon, Celular, mail)
        self.Profesional.append(nuevo_Profesional)  # Agrega un nuevo profesional a la lista


    # Este método permite consultar datos de profesional que están en el inventario
    # Devuelve el profesional correspondiente al código proporcionado o False si no existe.
    def consultar_Profesional(self, Matrícula):
        for Profesional in self.Profesional:
            if Profesional.Matrícula == Matrícula:
                return Profesional
        return False


    # Este método permite modificar datos de profesional que están en el inventario
    # Utiliza el método consultar_profesional del inventario y modificar del profesional.
    def modificar_Profesional(self, Matrícula, nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT, nueva_Profesional, nuevo_Celular, nuevo_mail):
        Profesional = self.consultar_Profesional(Matrícula)
        if Profesional:
            Profesional.modificar(nuevo_ApellidoNombre, nuevo_DNI, nuevo_CUIT,nueva_Profesional, nuevo_Celular, nuevo_mail )
            print("-"*50)
            print(f'Profesional modificado:\nMatrícula: {Profesional.Matrícula}\nApellidoNombre: {Profesional.ApellidoNombre}\nDNI: {Profesional.DNI}\nCUIT: {Profesional.CUIT}\nProfesión: {Profesional.Profesión}\nCelular: {Profesional.Celular}\nmail: {Profesional.mail}')


    # Este método elimina el profesional indicado por la matricula de la lista
    # mantenida en el inventario
    def eliminar_profesional(self, Matrícula):
        for Profesional in self.Profesional:
            if Profesional.Matrícula == Matrícula:
                self.profesional.remove(Profesional)
                print("Profesional {Matrícula} eliminado.")
                break
        else:
            print("Profesional {Matrícula} no encontrado.")


    # Este método imprime en la terminal una lista con los datos de los
    # profesionales que figuran en el inventario.
    def listar_Profesional(self):
        print("-"*50)
        print("INVENTARIO - Lista de profesional:")
        print("Matrícula Nacional\tApellido-Nombre\t\tDNI\tCUIT\tProfesión\tCelular\tmail")
        for Profesional in self.Profesional:
            print(f'{Profesional.Matrícula}\t{Profesional.ApellidoNombre}\t{Profesional.DNI}\t{Profesional.CUIT}\t{Profesional.Profesión}\t{Profesional.Celular}\t{Profesional.mail}')
        print("-"*50)



# -------------------------------------------------------------------
# Ejemplo de uso de las clases y objetos definidos antes:
# -------------------------------------------------------------------

# Crear una instancia de la clase Inventario
mi_inventario = Inventario()


# Crear 3 productos y agregarlos al inventario
mi_inventario.agregar_producto(1, 'Teclado USB 101 teclas', 10, 4500)
mi_inventario.agregar_producto(2, 'Mouse USB 3 botones', 5, 2500)
mi_inventario.agregar_producto(3, 'Monitor LCD 22 pulgadas', 15, 52500)

# Listar todos los productos del inventario
mi_inventario.listar_productos()

# Agregar 2 productos al carrito
mi_carrito.agregar(1, 5, mi_inventario) # Agregar 5 unidades del producto con código 1 al carrito
mi_carrito.agregar(3, 4, mi_inventario) # Agregar 4 unidades del producto con código 3 al carrito

# Listar todos los productos del carrito
mi_carrito.mostrar()

# Quitar 2 productos del carrito
mi_carrito.quitar(1, 2, mi_inventario) # Quitar 2 unidades del producto con código 1 en el carrito

# Listar todos los productos del carrito
mi_carrito.mostrar()

# Quitar 3 productos del carrito
mi_carrito.quitar(1, 3, mi_inventario) # Quitar 3 unidades del producto con código 1 en el carrito

# Listar todos los productos del carrito
mi_carrito.mostrar()

# Mostramos el inventario
mi_inventario.listar_productos()