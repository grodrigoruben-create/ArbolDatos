import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from arbol import crear_arbol_inicial


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Árbol de Carpetas")
        self.geometry("520x500")
        self.minsize(420, 400)

        self.paleta = {
            "fondo_barra": "#e9ecef",
            "texto_principal": "#1f1f1f",
            "fondo": "#ffffff",
            "acento": "#4a86e8",
        }

        self.arbol = crear_arbol_inicial()
        self.iid_por_nodo = {}  # nombre -> iid del Treeview
        self.iconos_guardados = {}
        self.tab_feed = ttk.Frame(self)
        self.tab_historial = ttk.Frame(self)
        self._vista_actual = None

        self.icon_frame = tk.Frame(self, bg=self.paleta["fondo_barra"], height=42)
        self.icon_frame.pack(fill="x")
        self.icon_frame.pack_propagate(False)

        self.crear_widgets()
        self.refrescar_arbol()

        self.crear_boton_nav("Agregar", "imagenes/Agregar.png", self.agregar)
        self.crear_boton_nav("Eliminar", "imagenes/Eliminar.png", self.eliminar)
        self.crear_boton_nav("Buscar", "imagenes/Buscar.png", self.buscar)
        self.crear_boton_nav("Salir", "imagenes/Salir.png", self.destroy)


    def crear_boton_nav(self, texto, ruta_imagen, comando):

        img_original = Image.open(ruta_imagen)
        img_redimensionada = img_original.resize((24, 24), Image.LANCZOS)

        icono = ImageTk.PhotoImage(img_redimensionada)

        self.iconos_guardados[texto] = icono

        btn = tk.Button(self.icon_frame, text=texto, image=icono, compound="top",
                        bg=self.paleta["fondo_barra"], fg=self.paleta["texto_principal"],
                        activebackground=self.paleta["fondo_barra"],
                        bd=0, cursor="hand2", font=("Arial", 9), command=comando)

        btn.pack(side="left", padx=15)

    def crear_widgets(self):
        # --- Árbol con scrollbar ---
        marco_arbol = ttk.Frame(self, padding=10)
        marco_arbol.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(marco_arbol, show="tree", selectmode="browse")
        scroll = ttk.Scrollbar(marco_arbol, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar)

        # --- Controles ---
        marco = ttk.LabelFrame(self, text="Acciones", padding=10)
        marco.pack(fill="x", padx=10, pady=(0, 10))
        marco.columnconfigure(1, weight=1)

        ttk.Label(marco, text="Carpeta padre:").grid(row=0, column=0, sticky="w", pady=3)
        self.entry_padre = ttk.Entry(marco)
        self.entry_padre.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        ttk.Label(marco, text="Nueva carpeta:").grid(row=1, column=0, sticky="w", pady=3)
        self.entry_nueva = ttk.Entry(marco)
        self.entry_nueva.grid(row=1, column=1, sticky="ew", padx=5, pady=3)

        botones = ttk.Frame(marco)
        botones.grid(row=2, column=0, columnspan=2, pady=(8, 0))
        ttk.Button(botones, text="Agregar", command=self.agregar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(botones, text="Buscar", command=self.buscar).pack(side="left", padx=4)
        ttk.Button(botones, text="Salir", command=self.destroy).pack(side="left", padx=4)

        self.entry_nueva.bind("<Return>", lambda e: self.agregar())

        # --- Barra de estado ---
        self.estado = tk.StringVar(
            value="Selecciona una carpeta del árbol para usarla como padre."
        )
        ttk.Label(self, textvariable=self.estado, relief="sunken", anchor="w",
                  padding=(6, 2)).pack(fill="x", side="bottom")

        self.crear_icono_carpeta("carpeta", "imagenes/carpeta.png")


    def crear_icono_carpeta(self, nombre, ruta_imagen):
        img_original = Image.open(ruta_imagen)
        img_redimensionada = img_original.resize((24, 24), Image.LANCZOS)
        icono = ImageTk.PhotoImage(img_redimensionada)
        self.iconos_guardados[nombre] = icono

    def cambiar_vista(self, vista):
        if vista is None:
            return
        for frame in (self.tab_feed, self.tab_historial):
            if frame is not None and frame.winfo_exists() and frame is not vista:
                frame.pack_forget()
        if not vista.winfo_ismapped():
            vista.pack(fill="both", expand=True)
        self._vista_actual = vista
        nombre_vista = "Acciones" if vista is self.tab_feed else "Historial"
        self.estado.set(f"Vista activa: {nombre_vista}.")

    # ---------- Utilidades ----------
    def refrescar_arbol(self):
        self.tree.delete(*self.tree.get_children())
        self.iid_por_nodo.clear()
        self._insertar("", self.arbol.raiz)

    def _insertar(self, padre_iid, nodo):
        iid = self.tree.insert(padre_iid, "end", image=self.iconos_guardados.get("carpeta"), text=f" {nodo.nombre}", open=True)
        self.iid_por_nodo[nodo.nombre] = iid
        for hijo in nodo.hijos:
            self._insertar(iid, hijo)

    def nombre_seleccionado(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0], "text").strip()

    def al_seleccionar(self, _event):
        nombre = self.nombre_seleccionado()
        if nombre:
            self.entry_padre.delete(0, tk.END)
            self.entry_padre.insert(0, nombre)

    # ---------- Acciones ----------
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

