class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []

class ArbolCarpetas:
    def __init__(self, nombre_raiz="C:"):
        self.raiz = Nodo(nombre_raiz)

    def buscar_carpeta(self, nodo_actual, nombre):
        """Busca recursivamente una carpeta por su nombre."""
        if nodo_actual.nombre == nombre:
            return nodo_actual
        for hijo in nodo_actual.hijos:
            resultado = self.buscar_carpeta(hijo, nombre)
            if resultado:
                return resultado
        return None

    def buscar_padre(self, nodo_actual, nombre):
        """Encuentra el nodo padre de una carpeta dada."""
        for hijo in nodo_actual.hijos:
            if hijo.nombre == nombre:
                return nodo_actual
            resultado = self.buscar_padre(hijo, nombre)
            if resultado:
                return resultado
        return None

    def agregar_carpeta(self, nombre_padre, nombre_hijo):
        nombre_padre = nombre_padre.strip()
        nombre_hijo = nombre_hijo.strip()

        if not nombre_hijo:
            print("El nombre de la nueva carpeta no puede estar vacío.")
            return

        padre = self.buscar_carpeta(self.raiz, nombre_padre)
        if padre:
            # Evita crear dos carpetas con el mismo nombre dentro del mismo padre
            for hijo in padre.hijos:
                if hijo.nombre == nombre_hijo:
                    print(f"Ya existe una carpeta '{nombre_hijo}' dentro de '{nombre_padre}'.")
                    return

            padre.hijos.append(Nodo(nombre_hijo))
            print(f"Carpeta '{nombre_hijo}' agregada exitosamente.")
        else:
            print(f"No se encontró la carpeta '{nombre_padre}'.")

    def eliminar_carpeta(self, nombre):
        nombre = nombre.strip()

        if self.raiz.nombre == nombre:
            print("No se puede eliminar la carpeta raíz.")
            return

        padre = self.buscar_padre(self.raiz, nombre)
        if padre:
            # Filtra la lista para quitar la carpeta
            padre.hijos = [hijo for hijo in padre.hijos if hijo.nombre != nombre]
            print(f"Carpeta '{nombre}' eliminada.")
        else:
            print(f"No se encontró la carpeta '{nombre}'.")

    def mostrar_arbol(self, nodo_actual=None, nivel=0):
        if nodo_actual is None:
            nodo_actual = self.raiz

        print(" " * nivel * 4 + f"- {nodo_actual.nombre}")
        for hijo in nodo_actual.hijos:
            self.mostrar_arbol(hijo, nivel + 1)

    def buscar_carpeta_por_nombre(self, nombre):
        nombre = nombre.strip()
        resultado = self.buscar_carpeta(self.raiz, nombre)
        if resultado:
            print(f"Carpeta '{nombre}' encontrada.")
        else:
            print(f"No se encontró la carpeta '{nombre}'.")

arbol = ArbolCarpetas("C:")

arbol.agregar_carpeta("C:", "Fotos")
arbol.agregar_carpeta("Fotos", "Vacaciones")
arbol.agregar_carpeta("Fotos", "Familia")

arbol.agregar_carpeta("C:", "Documentos")
arbol.agregar_carpeta("Documentos", "Trabajo")
arbol.agregar_carpeta("Documentos", "Escuela")

arbol.agregar_carpeta("C:", "Musica")
arbol.agregar_carpeta("Musica", "Descargada")
arbol.agregar_carpeta("Musica", "favoritos")
arbol.agregar_carpeta("Musica", "Para_estudiar")

arbol.agregar_carpeta("C:", "Videos")
arbol.agregar_carpeta("Videos", "Películas")
arbol.agregar_carpeta("Videos", "Personal")

while True:
    print("\nMenú de opciones:")
    print("1. Agregar carpeta")
    print("2. Mostrar árbol de carpetas")
    print("3. Eliminar carpeta")
    print("4. Buscar carpeta")
    print("5. Salir")

    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        nombre_padre = input("Ingrese el nombre de la carpeta padre: ")
        nombre_hijo = input("Ingrese el nombre de la nueva carpeta: ")
        arbol.agregar_carpeta(nombre_padre, nombre_hijo)

    elif opcion == "2":
        arbol.mostrar_arbol()

    elif opcion == "3":
        nombre_carpeta = input("Ingrese el nombre de la carpeta a eliminar: ")
        arbol.eliminar_carpeta(nombre_carpeta)

    elif opcion == "4":
        nombre_carpeta = input("Ingrese el nombre de la carpeta a buscar: ")
        arbol.buscar_carpeta_por_nombre(nombre_carpeta)

    elif opcion == "5":
        print("¡Hasta luego!")
        break

    else:
        print("Opción no válida. Intente nuevamente.")