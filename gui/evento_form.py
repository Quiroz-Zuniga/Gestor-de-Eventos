'''Mobal para evento_form.py'''
import tkinter as tk
from tkinter import ttk, messagebox
from models.event import Evento
from utils.validations import Validaciones

class EventoForm(tk.Toplevel):
    def __init__(self, master=None, callback=None):
        super().__init__(master)
        self.title("Nuevo Evento")
        self.geometry("400x550")
        self.resizable(False, False)
        self.callback = callback

        self.evento = Evento()

        self.crear_widgets()

    def crear_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        campos = [
            ("Nombre", "nombre"),
            ("Descripción", "descripcion"),
            ("Fecha Inicio (AAAA-MM-DD HH:MM)", "fecha_inicio"),
            ("Fecha Fin (AAAA-MM-DD HH:MM)", "fecha_fin"),
            ("Ubicación", "ubicacion"),
            ("Capacidad Máxima", "capacidad_maxima"),
            ("Categoría", "categoria")
        ]

        self.entries = {}
        for label, key in campos:
            ttk.Label(frame, text=label).pack(anchor="w", pady=(10, 0))
            entry = ttk.Entry(frame)
            entry.pack(fill="x")
            self.entries[key] = entry

        self.estado_var = tk.StringVar(value="activo")
        ttk.Label(frame, text="Estado").pack(anchor="w", pady=(10, 0))
        estado_combo = ttk.Combobox(frame, textvariable=self.estado_var, values=["activo", "programado", "cancelado"])
        estado_combo.pack(fill="x")

        ttk.Button(frame, text="Guardar", command=self.guardar_evento).pack(pady=20)

    def guardar_evento(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}
        datos["estado"] = self.estado_var.get()

        # Validaciones básicas (pueden expandirse)
        valido, fechas = Validaciones.validar_fecha_evento(datos["fecha_inicio"], datos["fecha_fin"])
        if not valido:
            messagebox.showerror("Error de fecha", fechas)
            return

        valido_cap, cap = Validaciones.validar_numero_entero(datos["capacidad_maxima"], "capacidad", minimo=1)
        if not valido_cap:
            messagebox.showerror("Error de capacidad", cap)
            return

        self.evento.nombre = datos["nombre"]
        self.evento.descripcion = datos["descripcion"]
        self.evento.fecha_inicio = fechas["fecha_inicio"]
        self.evento.fecha_fin = fechas.get("fecha_fin")
        self.evento.ubicacion = datos["ubicacion"]
        self.evento.capacidad_maxima = cap
        self.evento.categoria = datos["categoria"]
        self.evento.estado = datos["estado"]

        if self.evento.guardar():
            messagebox.showinfo("Éxito", "Evento guardado correctamente.")
            if self.callback:
                self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar el evento.")
