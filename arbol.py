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
        """Devuelve (exito, mensaje)."""
        nombre_padre = nombre_padre.strip()
        nombre_hijo = nombre_hijo.strip()

        if not nombre_hijo:
            return False, "El nombre de la nueva carpeta no puede estar vacío."

        padre = self.buscar_carpeta(self.raiz, nombre_padre)
        if not padre:
            return False, f"No se encontró la carpeta '{nombre_padre}'."

        for hijo in padre.hijos:
            if hijo.nombre == nombre_hijo:
                return False, f"Ya existe '{nombre_hijo}' dentro de '{nombre_padre}'."

        padre.hijos.append(Nodo(nombre_hijo))
        return True, f"Carpeta '{nombre_hijo}' agregada exitosamente."

    def eliminar_carpeta(self, nombre):
        """Devuelve (exito, mensaje)."""
        nombre = nombre.strip()
        if self.raiz.nombre == nombre:
            return False, "No se puede eliminar la carpeta raíz."

        padre = self.buscar_padre(self.raiz, nombre)
        if not padre:
            return False, f"No se encontró la carpeta '{nombre}'."

        padre.hijos = [h for h in padre.hijos if h.nombre != nombre]
        return True, f"Carpeta '{nombre}' eliminada."


def crear_arbol_inicial():
    """Crea el árbol con las carpetas de ejemplo."""
    arbol = ArbolCarpetas("C:")
    estructura = {
        "Fotos": ["Vacaciones", "Familia"],
        "Documentos": ["Trabajo", "Escuela"],
        "Musica": ["Descargada", "favoritos", "Para_estudiar"],
        "Videos": ["Películas", "Personal"],
    }
    for padre, hijos in estructura.items():
        arbol.agregar_carpeta("C:", padre)
        for h in hijos:
            arbol.agregar_carpeta(padre, h)
    return arbol