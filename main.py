"""
Ventana principal del Gestor de Eventos
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime
from ttkthemes import ThemedTk

class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        self.root = ThemedTk(theme="Equilux")
        self.root.title("Gestor de Eventos Universitario")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Variables
        self.eventos_list = []
        self.participantes_list = []
        
        # Configurar estilo
        # self.configurar_estilo()
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Cargar datos de ejemplo
        self.cargar_datos_ejemplo()
        
        # Verificar conexión (simulada)
        self.verificar_conexion()
        
        self.root.mainloop()
    
    def configurar_estilo(self):
        """Configura el estilo de la aplicación"""
        style = ttk.Style()
        # self.style = ThemedTk(theme='yaru')
    
        
        # Configurar colores
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2E86AB')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='#28A745')
        style.configure('Error.TLabel', foreground='#DC3545')
        style.configure('Warning.TLabel', foreground='#FFC107')
    
    def crear_interfaz(self):
        """Crea la interfaz principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestor de Eventos Universitario", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Frame de estadísticas
        self.crear_frame_estadisticas(main_frame)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Pestaña de eventos
        self.crear_pestaña_eventos()
        
        # Pestaña de participantes
        self.crear_pestaña_participantes()
        
        # Pestaña de inscripciones
        self.crear_pestaña_inscripciones()
        
        # Barra de estado
        self.crear_barra_estado(main_frame)
    
    def crear_frame_estadisticas(self, parent):
        """Crea el frame con estadísticas generales"""
        stats_frame = ttk.LabelFrame(parent, text="Estadísticas Generales", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid para estadísticas
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)
        
        # Labels de estadísticas
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
            
            ttk.Label(frame, text=label, style='Heading.TLabel').pack()
            self.stats_labels[key] = ttk.Label(frame, text="0", font=('Arial', 20, 'bold'), foreground='#2E86AB')
            self.stats_labels[key].pack()
        
        # Configurar grid
        for i in range(4):
            stats_grid.columnconfigure(i, weight=1)
    
    def crear_pestaña_eventos(self):
        """Crea la pestaña de gestión de eventos"""
        eventos_frame = ttk.Frame(self.notebook)
        self.notebook.add(eventos_frame, text="Eventos")
        
        # Frame de controles
        controles_frame = ttk.Frame(eventos_frame)
        controles_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones
        ttk.Button(controles_frame, text="Nuevo Evento", command=self.nuevo_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Editar Evento", command=self.editar_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Eliminar Evento", command=self.eliminar_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Actualizar", command=self.cargar_eventos).pack(side=tk.LEFT, padx=5)
        
        # Frame de búsqueda
        search_frame = ttk.Frame(controles_frame)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.evento_search_var = tk.StringVar()
        self.evento_search_entry = ttk.Entry(search_frame, textvariable=self.evento_search_var, width=20)
        self.evento_search_entry.pack(side=tk.LEFT, padx=5)
        self.evento_search_entry.bind('<KeyRelease>', self.buscar_eventos)
        
        # Treeview para eventos
        self.crear_treeview_eventos(eventos_frame)
    
    def crear_treeview_eventos(self, parent):
        """Crea el treeview para mostrar eventos"""
        # Frame para treeview
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Configurar columnas
        columns = ('ID', 'Nombre', 'Fecha Inicio', 'Ubicación', 'Categoría', 'Inscritos/Capacidad', 'Estado')
        self.eventos_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados
        self.eventos_tree.heading('ID', text='ID')
        self.eventos_tree.heading('Nombre', text='Nombre')
        self.eventos_tree.heading('Fecha Inicio', text='Fecha Inicio')
        self.eventos_tree.heading('Ubicación', text='Ubicación')
        self.eventos_tree.heading('Categoría', text='Categoría')
        self.eventos_tree.heading('Inscritos/Capacidad', text='Inscritos/Capacidad')
        self.eventos_tree.heading('Estado', text='Estado')
        
        # Configurar anchos de columna
        self.eventos_tree.column('ID', width=50, anchor=tk.CENTER)
        self.eventos_tree.column('Nombre', width=200)
        self.eventos_tree.column('Fecha Inicio', width=120, anchor=tk.CENTER)
        self.eventos_tree.column('Ubicación', width=150)
        self.eventos_tree.column('Categoría', width=100, anchor=tk.CENTER)
        self.eventos_tree.column('Inscritos/Capacidad', width=120, anchor=tk.CENTER)
        self.eventos_tree.column('Estado', width=80, anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.eventos_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.eventos_tree.xview)
        self.eventos_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar
        self.eventos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind para doble click
        self.eventos_tree.bind('<Double-1>', lambda e: self.editar_evento())
    
    def crear_pestaña_participantes(self):
        """Crea la pestaña de gestión de participantes"""
        participantes_frame = ttk.Frame(self.notebook)
        self.notebook.add(participantes_frame, text="Participantes")
        
        # Frame de controles
        controles_frame = ttk.Frame(participantes_frame)
        controles_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones
        ttk.Button(controles_frame, text="Nuevo Participante", command=self.nuevo_participante).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Editar Participante", command=self.editar_participante).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Eliminar Participante", command=self.eliminar_participante).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Actualizar", command=self.cargar_participantes).pack(side=tk.LEFT, padx=5)
        
        # Frame de búsqueda
        search_frame = ttk.Frame(controles_frame)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.participante_search_var = tk.StringVar()
        self.participante_search_entry = ttk.Entry(search_frame, textvariable=self.participante_search_var, width=20)
        self.participante_search_entry.pack(side=tk.LEFT, padx=5)
        self.participante_search_entry.bind('<KeyRelease>', self.buscar_participantes)
        
        # Treeview para participantes
        self.crear_treeview_participantes(participantes_frame)
    
    def crear_treeview_participantes(self, parent):
        """Crea el treeview para mostrar participantes"""
        # Frame para treeview
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Configurar columnas
        columns = ('ID', 'Nombre', 'Apellido', 'Email', 'Teléfono', 'Fecha Registro', 'Total Eventos')
        self.participantes_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados
        self.participantes_tree.heading('ID', text='ID')
        self.participantes_tree.heading('Nombre', text='Nombre')
        self.participantes_tree.heading('Apellido', text='Apellido')
        self.participantes_tree.heading('Email', text='Email')
        self.participantes_tree.heading('Teléfono', text='Teléfono')
        self.participantes_tree.heading('Fecha Registro', text='Fecha Registro')
        self.participantes_tree.heading('Total Eventos', text='Total Eventos')
        
        # Configurar anchos de columna
        self.participantes_tree.column('ID', width=50, anchor=tk.CENTER)
        self.participantes_tree.column('Nombre', width=120)
        self.participantes_tree.column('Apellido', width=120)
        self.participantes_tree.column('Email', width=200)
        self.participantes_tree.column('Teléfono', width=120, anchor=tk.CENTER)
        self.participantes_tree.column('Fecha Registro', width=120, anchor=tk.CENTER)
        self.participantes_tree.column('Total Eventos', width=100, anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.participantes_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.participantes_tree.xview)
        self.participantes_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar
        self.participantes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind para doble click
        self.participantes_tree.bind('<Double-1>', lambda e: self.editar_participante())
    
    def crear_pestaña_inscripciones(self):
        """Crea la pestaña de gestión de inscripciones"""
        inscripciones_frame = ttk.Frame(self.notebook)
        self.notebook.add(inscripciones_frame, text="Inscripciones")
        
        # Frame de controles
        controles_frame = ttk.Frame(inscripciones_frame)
        controles_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones
        ttk.Button(controles_frame, text="Nueva Inscripción", command=self.nueva_inscripcion).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Ver Participantes del Evento", command=self.ver_participantes_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(controles_frame, text="Ver Eventos del Participante", command=self.ver_eventos_participante).pack(side=tk.LEFT, padx=5)
        
        # Labels informativos
        info_frame = ttk.Frame(inscripciones_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text="Selecciona un evento o participante en sus respectivas pestañas para ver las inscripciones relacionadas.", 
                 style='Heading.TLabel').pack()
    
    def crear_barra_estado(self, parent):
        """Crea la barra de estado en la parte inferior"""
        self.status_bar = ttk.Label(parent, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
    
    def verificar_conexion(self):
        """Verifica la conexión a la base de datos (simulada)"""
        self.actualizar_status("Conectado a la base de datos (simulado)")
    
    def actualizar_status(self, mensaje):
        """Actualiza el mensaje de la barra de estado"""
        self.status_bar.config(text=f"{datetime.now().strftime('%H:%M:%S')} - {mensaje}")
        self.root.update_idletasks()
    
    def cargar_datos_ejemplo(self):
        """Carga datos de ejemplo para mostrar la interfaz"""
        # Cargar estadísticas de ejemplo
        self.stats_labels["eventos_activos"].config(text="5")
        self.stats_labels["total_participantes"].config(text="25")
        self.stats_labels["inscripciones_confirmadas"].config(text="45")
        self.stats_labels["eventos_proximos"].config(text="3")
        
        # Cargar eventos de ejemplo
        self.cargar_eventos()
        self.cargar_participantes()
    
    def cargar_eventos(self):
        """Carga eventos de ejemplo"""
        # Limpiar treeview
        for item in self.eventos_tree.get_children():
            self.eventos_tree.delete(item)
        
        # Datos de ejemplo
        eventos_ejemplo = [
            (1, "Conferencia IA", "2024-07-15", "Auditorio A", "Académico", "15/50", "Activo"),
            (2, "Taller Python", "2024-07-20", "Lab 101", "Taller", "8/20", "Activo"),
            (3, "Seminario Web", "2024-07-25", "Virtual", "Seminario", "25/30", "Activo"),
            (4, "Expo Ciencias", "2024-08-01", "Patio Central", "Exposición", "0/100", "Programado"),
            (5, "Hackathon", "2024-08-10", "Lab 201", "Competencia", "12/40", "Activo")
        ]
        
        for evento in eventos_ejemplo:
            self.eventos_tree.insert('', 'end', values=evento)
        
        self.actualizar_status(f"Cargados {len(eventos_ejemplo)} eventos")
    
    def cargar_participantes(self):
        """Carga participantes de ejemplo"""
        # Limpiar treeview
        for item in self.participantes_tree.get_children():
            self.participantes_tree.delete(item)
        
        # Datos de ejemplo
        participantes_ejemplo = [
            (1, "Juan", "Pérez", "juan.perez@universidad.edu", "555-0101", "2024-01-15", "3"),
            (2, "María", "García", "maria.garcia@universidad.edu", "555-0102", "2024-01-20", "2"),
            (3, "Carlos", "López", "carlos.lopez@universidad.edu", "555-0103", "2024-02-01", "4"),
            (4, "Ana", "Martínez", "ana.martinez@universidad.edu", "555-0104", "2024-02-05", "1"),
            (5, "Luis", "Rodríguez", "luis.rodriguez@universidad.edu", "555-0105", "2024-02-10", "2")
        ]
        
        for participante in participantes_ejemplo:
            self.participantes_tree.insert('', 'end', values=participante)
        
        self.actualizar_status(f"Cargados {len(participantes_ejemplo)} participantes")
    
    # Métodos de evento (placeholder)
    def nuevo_evento(self):
        messagebox.showinfo("Info", "Función 'Nuevo Evento' no implementada aún")
    
    def editar_evento(self):
        messagebox.showinfo("Info", "Función 'Editar Evento' no implementada aún")
    
    def eliminar_evento(self):
        messagebox.showinfo("Info", "Función 'Eliminar Evento' no implementada aún")
    
    def buscar_eventos(self, event=None):
        # Implementar búsqueda aquí
        pass
    
    # Métodos de participante (placeholder)
    def nuevo_participante(self):
        messagebox.showinfo("Info", "Función 'Nuevo Participante' no implementada aún")
    
    def editar_participante(self):
        messagebox.showinfo("Info", "Función 'Editar Participante' no implementada aún")
    
    def eliminar_participante(self):
        messagebox.showinfo("Info", "Función 'Eliminar Participante' no implementada aún")
    
    def buscar_participantes(self, event=None):
        # Implementar búsqueda aquí
        pass
    
    # Métodos de inscripción (placeholder)
    def nueva_inscripcion(self):
        messagebox.showinfo("Info", "Función 'Nueva Inscripción' no implementada aún")
    
    def ver_participantes_evento(self):
        messagebox.showinfo("Info", "Función 'Ver Participantes del Evento' no implementada aún")
    
    def ver_eventos_participante(self):
        messagebox.showinfo("Info", "Función 'Ver Eventos del Participante' no implementada aún")

if __name__ == "__main__":
    app = MainWindow()