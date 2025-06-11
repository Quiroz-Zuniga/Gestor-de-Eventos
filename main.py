import tkinter as tk
from tkinter import ttk, messagebox
from themedes import ThemedTk # type: ignore
from datetime import datetime

from gui.evento_form import EventoForm
from gui.participante_form import ParticipanteForm

from models.event import Evento
from models.participante import Participante

class MainWindow:
    def __init__(self):
        self.root = ThemedTk(theme="equilux")
        self.root.title("Gestor de Eventos Universitario")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        self.eventos_list = []
        self.participantes_list = []

        self.crear_interfaz()

        self.cargar_eventos()
        self.cargar_participantes()

        self.verificar_conexion()

        self.root.mainloop()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title_label = ttk.Label(main_frame, text="Gestor de Eventos Universitario", font=('Arial', 16, 'bold'), foreground='#2E86AB')
        title_label.pack(pady=(0, 20))

        self.crear_frame_estadisticas(main_frame)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

    def actualizar_estadisticas(self):
        """
        Actualiza las estadísticas generales en la interfaz
        """
        datos_estadisticas = {
            "eventos_activos": len([evento for evento in self.eventos_list if evento.estado == "Activo"]),
            "total_participantes": len(self.participantes_list),
            "inscripciones_confirmadas": sum(evento.inscritos for evento in self.eventos_list),
            "eventos_proximos": len([evento for evento in self.eventos_list if evento.fecha_inicio > datetime.now()])
        }

        # Validar datos antes de actualizar
        es_valido, mensaje_error = Validaciones.validar_numero_entero(datos_estadisticas["total_participantes"], "Total Participantes", 0)
        if not es_valido:
            self.actualizar_status(f"Error en estadísticas: {mensaje_error}")
            return

        for key, value in datos_estadisticas.items():
            self.stats_labels[key].config(text=str(value))

        self.actualizar_status("Estadísticas actualizadas")

        self.crear_pestaña_eventos()
        self.crear_pestaña_participantes()
        self.crear_pestaña_inscripciones()

        self.crear_barra_estado(main_frame)

    def crear_frame_estadisticas(self, parent):
        stats_frame = ttk.LabelFrame(parent, text="Estadísticas Generales", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)

        self.stats_labels = {}
        stats_info = [
            ("eventos_activos", "Eventos Activos"),
            ("total_participantes", "Total Participantes"),
            ("inscripciones_confirmadas", "Inscripciones Confirmadas"),
            ("eventos_proximos", "Eventos Próximos")
        ]

        for i, (key, label) in enumerate(stats_info):
            frame = ttk.Frame(stats_grid)
            frame.grid(row=0, column=i, padx=20, pady=5, sticky="ew")

            ttk.Label(frame, text=label, font=('Arial', 12, 'bold')).pack()
            self.stats_labels[key] = ttk.Label(frame, text="0", font=('Arial', 20, 'bold'), foreground='#2E86AB')
            self.stats_labels[key].pack()

        for i in range(4):
            stats_grid.columnconfigure(i, weight=1)

    def crear_pestaña_eventos(self):
        eventos_frame = ttk.Frame(self.notebook)
        self.notebook.add(eventos_frame, text="Eventos")

        controles_frame = ttk.Frame(eventos_frame)
        controles_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(controles_frame, text="Nuevo Evento", command=self.nuevo_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Actualizar", command=self.cargar_eventos).pack(side=tk.LEFT, padx=5)

        self.crear_treeview_eventos(eventos_frame)

    def crear_treeview_eventos(self, parent):
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        columns = ('ID', 'Nombre', 'Fecha Inicio', 'Ubicación', 'Categoría', 'Inscritos/Capacidad', 'Estado')
        self.eventos_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.eventos_tree.heading(col, text=col)
            self.eventos_tree.column(col, anchor=tk.CENTER)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.eventos_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.eventos_tree.xview)
        self.eventos_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.eventos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def cargar_eventos(self):
        for item in self.eventos_tree.get_children():
            self.eventos_tree.delete(item)

        self.eventos_list = Evento.obtener_todos()

        for evento in self.eventos_list:
            self.eventos_tree.insert('', 'end', values=(
                evento.id_evento,
                evento.nombre,
                evento.fecha_inicio_str(),
                evento.ubicacion,
                evento.categoria,
                f"{evento.inscritos}/{evento.capacidad_maxima}",
                evento.estado
            ))

        self.actualizar_estadisticas()  # Llamar la actualización después de cargar eventos
        self.actualizar_status(f"Cargados {len(self.eventos_list)} eventos")

    def nuevo_evento(self):
        EventoForm(master=self.root, callback=self.cargar_eventos)

    def crear_pestaña_participantes(self):
        participantes_frame = ttk.Frame(self.notebook)
        self.notebook.add(participantes_frame, text="Participantes")

        controles_frame = ttk.Frame(participantes_frame)
        controles_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(controles_frame, text="Nuevo Participante", command=self.nuevo_participante).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Actualizar", command=self.cargar_participantes).pack(side=tk.LEFT, padx=5)

        self.crear_treeview_participantes(participantes_frame)

    def crear_treeview_participantes(self, parent):
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        columns = ('ID', 'Nombre', 'Apellido', 'Email', 'Teléfono', 'Fecha Registro', 'Total Eventos')
        self.participantes_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.participantes_tree.heading(col, text=col)
            self.participantes_tree.column(col, anchor=tk.CENTER)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.participantes_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.participantes_tree.xview)
        self.participantes_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.participantes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def cargar_participantes(self):
        for item in self.participantes_tree.get_children():
            self.participantes_tree.delete(item)

        self.participantes_list = Participante.obtener_todos()

        for participante in self.participantes_list:
            self.participantes_tree.insert('', 'end', values=(
                participante.id_participante,
                participante.nombre,
                participante.apellido,
                participante.email,
                participante.telefono,
                participante.fecha_registro,
                participante.total_eventos
            ))

        self.actualizar_estadisticas()  # Llamar la actualización después de cargar participantes
        self.actualizar_status(f"Cargados {len(self.participantes_list)} participantes")


    def nuevo_participante(self):
        ParticipanteForm(master=self.root, callback=self.cargar_participantes)

    def crear_pestaña_inscripciones(self):
        inscripciones_frame = ttk.Frame(self.notebook)
        self.notebook.add(inscripciones_frame, text="Inscripciones")

        controles_frame = ttk.Frame(inscripciones_frame)
        controles_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(controles_frame, text="Nueva Inscripción", command=self.nueva_inscripcion).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Ver Participantes del Evento", command=self.ver_participantes_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Ver Eventos del Participante", command=self.ver_eventos_participante).pack(side=tk.LEFT, padx=5)

    def crear_barra_estado(self, parent):
        self.status_bar = ttk.Label(parent, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

    def verificar_conexion(self):
        self.actualizar_status("Conectado a la base de datos")

    def actualizar_status(self, mensaje):
        self.status_bar.config(text=f"{datetime.now().strftime('%H:%M:%S')} - {mensaje}")
        self.root.update_idletasks()

    def nueva_inscripcion(self):
        messagebox.showinfo("Info", "Función 'Nueva Inscripción' no implementada aún")

    def ver_participantes_evento(self):
        messagebox.showinfo("Info", "Función 'Ver Participantes del Evento' no implementada aún")

    def ver_eventos_participante(self):
        messagebox.showinfo("Info", "Función 'Ver Eventos del Participante' no implementada aún")

if __name__ == "__main__":
    app = MainWindow() 
    
