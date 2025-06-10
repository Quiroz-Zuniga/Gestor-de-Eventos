import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import EventoQueries, ParticipanteQueries, InscripcionQueries

class NuevaInscripcionForm(tk.Toplevel):
    def __init__(self, master=None, callback=None):
        super().__init__(master)
        self.title("Nueva Inscripción")
        self.geometry("400x400")
        self.resizable(False, False)
        self.callback = callback

        self.crear_widgets()

    def crear_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Combo de Eventos
        ttk.Label(frame, text="Evento").pack(anchor="w", pady=(10, 0))
        self.evento_var = tk.StringVar()
        self.evento_combo = ttk.Combobox(frame, textvariable=self.evento_var, state="readonly")
        self.evento_combo.pack(fill="x")

        # Combo de Participantes
        ttk.Label(frame, text="Participante").pack(anchor="w", pady=(10, 0))
        self.participante_var = tk.StringVar()
        self.participante_combo = ttk.Combobox(frame, textvariable=self.participante_var, state="readonly")
        self.participante_combo.pack(fill="x")

        # Notas
        ttk.Label(frame, text="Notas (opcional)").pack(anchor="w", pady=(10, 0))
        self.notas_text = tk.Text(frame, height=5)
        self.notas_text.pack(fill="x")

        # Boton Guardar
        ttk.Button(frame, text="Guardar Inscripción", command=self.guardar_inscripcion).pack(pady=20)

        # Cargar datos
        self.cargar_eventos()
        self.cargar_participantes()

    def cargar_eventos(self):
        eventos = EventoQueries.obtener_todos()
        self.eventos_dict = {f"{e['nombre']} (ID: {e['id_evento']})": e['id_evento'] for e in eventos if e['estado'] == 'activo'}
        self.evento_combo['values'] = list(self.eventos_dict.keys())

    def cargar_participantes(self):
        participantes = ParticipanteQueries.obtener_todos()
        self.participantes_dict = {f"{p['nombre']} {p['apellido']} (ID: {p['id_participante']})": p['id_participante'] for p in participantes}
        self.participante_combo['values'] = list(self.participantes_dict.keys())

    def guardar_inscripcion(self):
        evento_key = self.evento_var.get()
        participante_key = self.participante_var.get()

        if not evento_key or not participante_key:
            messagebox.showerror("Error", "Debe seleccionar un evento y un participante.")
            return

        id_evento = self.eventos_dict[evento_key]
        id_participante = self.participantes_dict[participante_key]

        # Verificar si ya está inscrito
        if InscripcionQueries.verificar_inscripcion_existe(id_evento, id_participante):
            messagebox.showerror("Error", "El participante ya está inscrito en este evento.")
            return

        notas = self.notas_text.get("1.0", tk.END).strip()

        result = InscripcionQueries.inscribir_participante(id_evento, id_participante, notas)

        if result:
            messagebox.showinfo("Éxito", "Inscripción realizada correctamente.")
            if self.callback:
                self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo realizar la inscripción.")
