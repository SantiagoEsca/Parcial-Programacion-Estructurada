import os

class NodoLibro:
    def __init__(self, titulo, autor, año, editorial, isbn, paginas):
        self.titulo = titulo
        self.autor = autor
        self.año = año
        self.editorial = editorial
        self.isbn = isbn
        self.paginas = paginas
        self.siguiente = None

class ListaLibros:
    def __init__(self):
        self.cabeza = None

    def agregar_libro(self, titulo, autor, año, editorial, isbn, paginas):
        nuevo_libro = NodoLibro(titulo, autor, año, editorial, isbn, paginas)
        if self.cabeza is None:
            self.cabeza = nuevo_libro
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_libro

    def ordenar_libros_por_titulo(self):
        self.cabeza = self.mergesort_titulo(self.cabeza)

    def mergesort_titulo(self, nodo):
        if not nodo or not nodo.siguiente:
            return nodo
        medio = self.obtener_medio(nodo)
        mitad_siguiente = medio.siguiente
        medio.siguiente = None
        izquierda = self.mergesort_titulo(nodo)
        derecha = self.mergesort_titulo(mitad_siguiente)
        return self.merge_titulo(izquierda, derecha)

    def merge_titulo(self, izquierda, derecha):
        if not izquierda:
            return derecha
        if not derecha:
            return izquierda
        if izquierda.titulo.lower() <= derecha.titulo.lower():
            resultado = izquierda
            resultado.siguiente = self.merge_titulo(izquierda.siguiente, derecha)
        else:
            resultado = derecha
            resultado.siguiente = self.merge_titulo(izquierda, derecha.siguiente)
        return resultado

    def obtener_medio(self, nodo):
        if not nodo:
            return nodo
        lento = nodo
        rapido = nodo.siguiente
        while rapido and rapido.siguiente:
            lento = lento.siguiente
            rapido = rapido.siguiente.siguiente
        return lento

    def mostrar_libros(self):
        actual = self.cabeza
        while actual:
            print(f"Título: {actual.titulo}, Autor: {actual.autor}, ISBN: {actual.isbn}")
            actual = actual.siguiente

    def buscar_libro(self, campo, valor):
        actual = self.cabeza
        while actual:
            if campo == 'titulo' and actual.titulo == valor:
                return actual
            elif campo == 'autor' and actual.autor == valor:
                return actual
            elif campo == 'isbn' and actual.isbn == valor:
                return actual
            actual = actual.siguiente
        return None

class NodoLector:
    def __init__(self, nombre, dni, libro_solicitado):
        self.nombre = nombre
        self.dni = dni
        self.libro_solicitado = libro_solicitado
        self.siguiente = None

class ColaLectores:
    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, nombre, dni, libro_solicitado):
        nuevo_lector = NodoLector(nombre, dni, libro_solicitado)
        if not self.frente:
            self.frente = nuevo_lector
            self.final = nuevo_lector
        else:
            self.final.siguiente = nuevo_lector
            self.final = nuevo_lector

    def desencolar(self):
        if self.frente:
            lector = self.frente
            self.frente = self.frente.siguiente
            return lector
        return None

    def mostrar_solicitudes(self):
        actual = self.frente
        while actual:
            print(f"Nombre: {actual.nombre}, DNI: {actual.dni}, Libro: {actual.libro_solicitado}")
            actual = actual.siguiente

class NodoOperacion:
    def __init__(self, operacion):
        self.operacion = operacion
        self.siguiente = None

class PilaHistorial:
    def __init__(self):
        self.tope = None

    def push(self, operacion):
        nueva_operacion = NodoOperacion(operacion)
        nueva_operacion.siguiente = self.tope
        self.tope = nueva_operacion

    def pop(self):
        if self.tope:
            operacion = self.tope.operacion
            self.tope = self.tope.siguiente
            return operacion
        return None

    def mostrar_historial(self):
        actual = self.tope
        while actual:
            print(f"Operación: {actual.operacion}")
            actual = actual.siguiente

def solicitar_libro(lista_libros, cola_lectores, pila_historial, nombre, dni, titulo):
    libro = lista_libros.buscar_libro('titulo', titulo)
    if libro:
        cola_lectores.encolar(nombre, dni, titulo)
        pila_historial.push(f"Solicitud de libro: {titulo} por {nombre}")
        print(f"Libro solicitado con éxito: {titulo}")
    else:
        print(f"Error: el libro '{titulo}' no existe en la biblioteca.")

def devolver_libro(cola_lectores, pila_historial):
    lector = cola_lectores.desencolar()
    if lector:
        pila_historial.push(f"Devolución de libro: {lector.libro_solicitado} por {lector.nombre}")
        print(f"Libro devuelto con éxito: {lector.libro_solicitado}")
    else:
        print("No hay solicitudes en espera.")

def guardar_historial(pila_historial):
    with open("historial.txt", "w") as f:
        actual = pila_historial.tope
        while actual:
            f.write(f"{actual.operacion}\n")
            actual = actual.siguiente
    print("Historial guardado en 'historial.txt'.")

def cargar_historial(pila_historial):
    if os.path.exists("historial.txt"):
        with open("historial.txt", "r") as f:
            for linea in f:
                pila_historial.push(linea.strip())
        print("Historial cargado desde 'historial.txt'.")

def guardar_datos(lista_libros, cola_lectores):
    lista_libros.ordenar_libros_por_titulo()
    with open("biblioteca.txt", "w") as f:
        actual = lista_libros.cabeza
        while actual:
            f.write(f"{actual.titulo},{actual.autor},{actual.año},{actual.editorial},{actual.isbn},{actual.paginas}\n")
            actual = actual.siguiente
    with open("solicitudes.txt", "w") as f:
        actual = cola_lectores.frente
        while actual:
            f.write(f"{actual.nombre},{actual.dni},{actual.libro_solicitado}\n")
            actual = actual.siguiente
    print("Datos de la biblioteca y solicitudes guardados con éxito.")

def cargar_datos(lista_libros, cola_lectores):
    if os.path.exists("biblioteca.txt"):
        with open("biblioteca.txt", "r") as f:
            for linea in f:
                titulo, autor, año, editorial, isbn, paginas = linea.strip().split(',')
                lista_libros.agregar_libro(titulo, autor, int(año), editorial, isbn, int(paginas))
    if os.path.exists("solicitudes.txt"):
        with open("solicitudes.txt", "r") as f:
            for linea in f:
                nombre, dni, libro_solicitado = linea.strip().split(',')
                cola_lectores.encolar(nombre, dni, libro_solicitado)
    print("Datos de la biblioteca y solicitudes cargados con éxito.")

def mostrar_historial_completo(pila_historial):
    print("Historial completo de operaciones:")
    pila_historial.mostrar_historial()

def sistema_gestion_biblioteca():
    lista_libros = ListaLibros()
    cola_lectores = ColaLectores()
    pila_historial = PilaHistorial()

    cargar_datos(lista_libros, cola_lectores)
    cargar_historial(pila_historial)

    while True:
        print("\n--- Menú de Gestión de Biblioteca Digital ---")
        print("1. Agregar libro")
        print("2. Mostrar libros")
        print("3. Ordenar libros por título")
        print("4. Buscar libro")
        print("5. Solicitar libro")
        print("6. Devolver libro")
        print("7. Mostrar historial de operaciones")
        print("8. Guardar historial en archivo")
        print("9. Guardar y salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor: ")
            año = int(input("Ingrese el año de edición: "))
            editorial = input("Ingrese la editorial: ")
            isbn = input("Ingrese el ISBN: ")
            paginas = int(input("Ingrese el número de páginas: "))
            lista_libros.agregar_libro(titulo, autor, año, editorial, isbn, paginas)
            pila_historial.push(f"Agregado libro: {titulo}")
            print("Libro agregado con éxito.")
        
        elif opcion == '2':
            lista_libros.mostrar_libros()

        elif opcion == '3':
            lista_libros.ordenar_libros_por_titulo()
            pila_historial.push("Libros ordenados por título.")
            print("Libros ordenados por título con éxito.")

        elif opcion == '4':
            campo = input("Buscar por (titulo/autor/isbn): ")
            valor = input(f"Ingrese el {campo} a buscar: ")
            libro = lista_libros.buscar_libro(campo, valor)
            if libro:
                print(f"Libro encontrado: {libro.titulo}, Autor: {libro.autor}, ISBN: {libro.isbn}")
            else:
                print("Libro no encontrado.")

        elif opcion == '5':
            nombre = input("Ingrese su nombre: ")
            dni = input("Ingrese su DNI: ")
            titulo = input("Ingrese el título del libro a solicitar: ")
            solicitar_libro(lista_libros, cola_lectores, pila_historial, nombre, dni, titulo)

        elif opcion == '6':
            devolver_libro(cola_lectores, pila_historial)

        elif opcion == '7':
            mostrar_historial_completo(pila_historial)

        elif opcion == '8':
            guardar_historial(pila_historial)

        elif opcion == '9':
            guardar_datos(lista_libros, cola_lectores)
            guardar_historial(pila_historial)
            print("Datos y historial guardados. Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    sistema_gestion_biblioteca()
