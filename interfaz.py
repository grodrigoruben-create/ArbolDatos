import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from arbol import crear_arbol_inicial

FONDO = "#f0f2f5"
ACENTO = "#0078d7"


class vent(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Árbol de Carpetas")
        self.geometry("520x500")
        self.configure(bg=FONDO)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background=FONDO)
        style.configure("Treeview", rowheight=25, fieldbackground="white")
        style.map("Treeview", background=[("selected", ACENTO)], foreground=[("selected", "white")])

        self.arbol = crear_arbol_inicial()
        self.iid_por_nodo = {}
        self.iconos = {}
        self.iconphoto(True, self.cargar_icono("ventana", "imagenes/administrador.png"))

        self.crear_barra()
        self.crear_widgets()
        self.refrescar_arbol()

    def cargar_icono(self, nombre, ruta):
        img = Image.open(ruta).resize((24, 24), Image.LANCZOS)
        self.iconos[nombre] = ImageTk.PhotoImage(img)
        return self.iconos[nombre]

    def crear_barra(self):
        barra = tk.Frame(self, bg=FONDO)
        barra.pack(fill="x")
        for texto, comando in (("Agregar", self.agregar), ("Buscar", self.buscar),
                               ("Eliminar", self.eliminar), ("Salir", self.destroy)):
            tk.Button(
                barra, text=texto, image=self.cargar_icono(texto, f"imagenes/{texto}.png"),
                compound="top", bg=FONDO, activebackground=FONDO, bd=0,
                cursor="hand2", command=comando
            ).pack(side="left", padx=15, pady=4)

    def crear_widgets(self):
        marco = ttk.LabelFrame(self, text="Acciones", padding=10)
        marco.pack(fill="x", padx=10, pady=(0, 10))
        marco.columnconfigure(1, weight=1)

        ttk.Label(marco, text="Carpeta padre:").grid(row=0, column=0, sticky="w", pady=3)
        self.entry_padre = ttk.Entry(marco)
        self.entry_padre.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        ttk.Label(marco, text="Nueva carpeta:").grid(row=1, column=0, sticky="w", pady=3)
        self.entry_nueva = ttk.Entry(marco)
        self.entry_nueva.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
        self.entry_nueva.bind("<Return>", lambda e: self.agregar())

        self.estado = tk.StringVar(value="Selecciona una carpeta del árbol para usarla como padre.")
        ttk.Label(self, textvariable=self.estado, relief="sunken", anchor="w",
                  padding=(6, 2)).pack(fill="x", side="bottom")

        self.tree = ttk.Treeview(self, show="tree")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar)

        self.cargar_icono("carpeta", "imagenes/carpeta.png")
        self.cargar_icono("c", "imagenes/c_icon.png")

    def refrescar_arbol(self):
        self.tree.delete(*self.tree.get_children())
        self.iid_por_nodo.clear()
        self._insertar("", self.arbol.raiz)

    def _insertar(self, padre_iid, nodo):
        icono = self.iconos["c"] if nodo.nombre.lower() == "c:" else self.iconos["carpeta"]
        iid = self.tree.insert(padre_iid, "end", image=icono,
                            text=f" {nodo.nombre}", open=True)
        self.iid_por_nodo[nodo.nombre] = iid
        for hijo in nodo.hijos:
            self._insertar(iid, hijo)

    def nombre_seleccionado(self):
        sel = self.tree.selection()
        return self.tree.item(sel[0], "text").strip() if sel else None

    def al_seleccionar(self, _event):
        nombre = self.nombre_seleccionado()
        if nombre:
            self.entry_padre.delete(0, tk.END)
            self.entry_padre.insert(0, nombre)

    def agregar(self):
        ok, msg = self.arbol.agregar_carpeta(self.entry_padre.get(), self.entry_nueva.get())
        if ok:
            self.refrescar_arbol()
            self.entry_nueva.delete(0, tk.END)
            self.estado.set(msg)
        else:
            messagebox.showwarning("Aviso", msg)

    def eliminar(self):
        nombre = self.nombre_seleccionado() or self.entry_padre.get().strip()
        if not nombre:
            messagebox.showwarning("Aviso", "Selecciona la carpeta que quieres eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}' y todo su contenido?"):
            return
        ok, msg = self.arbol.eliminar_carpeta(nombre)
        if ok:
            self.refrescar_arbol()
            self.estado.set(msg)
        else:
            messagebox.showwarning("Aviso", msg)

    def buscar(self):
        nombre = self.entry_nueva.get().strip() or self.entry_padre.get().strip()
        if not nombre:
            messagebox.showinfo("Buscar", "Escribe el nombre de la carpeta a buscar.")
            return
        nodo = self.arbol.buscar_carpeta(self.arbol.raiz, nombre)
        if nodo:
            iid = self.iid_por_nodo[nodo.nombre]
            self.tree.selection_set(iid)
            self.tree.see(iid)
            self.estado.set(f"Carpeta '{nombre}' encontrada.")
        else:
            messagebox.showinfo("Buscar", f"No se encontró la carpeta '{nombre}'.")