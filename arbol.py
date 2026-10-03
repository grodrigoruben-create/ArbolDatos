class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []

class ArbolCarpetas:
    def __init__(self, nombre_raiz="C:"):
        self.raiz = Nodo(nombre_raiz)

    def buscar_carpeta(self, nodo, nombre):
        if nodo.nombre == nombre:
            return nodo
        for hijo in nodo.hijos:
            encontrado = self.buscar_carpeta(hijo, nombre)
            if encontrado:
                return encontrado

    def buscar_padre(self, nodo, nombre):
        for hijo in nodo.hijos:
            if hijo.nombre == nombre:
                return nodo
            padre = self.buscar_padre(hijo, nombre)
            if padre:
                return padre

    def agregar_carpeta(self, nombre_padre, nombre_hijo):
        nombre_padre, nombre_hijo = nombre_padre.strip(), nombre_hijo.strip()
        if not nombre_hijo:
            return False, "El nombre de la nueva carpeta no puede estar vacío."

        padre = self.buscar_carpeta(self.raiz, nombre_padre)
        if not padre:
            return False, f"No se encontró la carpeta '{nombre_padre}'."
        if any(h.nombre == nombre_hijo for h in padre.hijos):
            return False, f"Ya existe '{nombre_hijo}' dentro de '{nombre_padre}'."

        padre.hijos.append(Nodo(nombre_hijo))
        return True, f"Carpeta '{nombre_hijo}' agregada exitosamente."

    def eliminar_carpeta(self, nombre):
        nombre = nombre.strip()
        if nombre == self.raiz.nombre:
            return False, "No se puede eliminar la carpeta raíz."

        padre = self.buscar_padre(self.raiz, nombre)
        if not padre:
            return False, f"No se encontró la carpeta '{nombre}'."

        padre.hijos = [h for h in padre.hijos if h.nombre != nombre]
        return True, f"Carpeta '{nombre}' eliminada."


def crear_arbol_inicial():
    arbol = ArbolCarpetas()
    estructura = {
        "Fotos": ["Vacaciones", "Familia"],
        "Documentos": ["Trabajo", "Escuela"],
        "Musica": ["Descargada", "favoritos", "Para_estudiar"],
        "Videos": ["Películas", "Personal"],
    }
    for padre, hijos in estructura.items():
        arbol.agregar_carpeta("C:", padre)
        for hijo in hijos:
            arbol.agregar_carpeta(padre, hijo)
    return arbol