import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from models.event import Evento
from utils.validations import Validaciones


class EventoForm(tk.Toplevel):
    def __init__(self, master=None, callback=None):
        super().__init__(master)
        self.title("Nuevo Evento")
        self.geometry("400x650")
        self.resizable(False, False)
        self.callback = callback
        self.evento = Evento()
        self.crear_widgets()

    def crear_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Campos de texto
        campos = [
            ("Nombre", "nombre"),
            ("Descripción", "descripcion"),
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

        # Calendario Fecha Inicio
        ttk.Label(frame, text="Fecha de Inicio").pack(anchor="w", pady=(10, 0))
        self.fecha_inicio_entry = DateEntry(frame, date_pattern="yyyy-mm-dd")
        self.fecha_inicio_entry.pack(fill="x")

        # Hora Inicio (AM/PM)
        hora_frame_inicio = ttk.Frame(frame)
        hora_frame_inicio.pack(fill="x", pady=2)
        self.hora_inicio = ttk.Combobox(hora_frame_inicio, values=[f"{h:02}" for h in range(1, 13)], width=5)
        self.hora_inicio.set("08")
        self.hora_inicio.pack(side="left")
        self.minuto_inicio = ttk.Combobox(hora_frame_inicio, values=[f"{m:02}" for m in range(0, 60, 5)], width=5)
        self.minuto_inicio.set("00")
        self.minuto_inicio.pack(side="left", padx=5)
        self.ampm_inicio = ttk.Combobox(hora_frame_inicio, values=["AM", "PM"], width=5)
        self.ampm_inicio.set("AM")
        self.ampm_inicio.pack(side="left")

        # Calendario Fecha Fin
        ttk.Label(frame, text="Fecha de Fin").pack(anchor="w", pady=(10, 0))
        self.fecha_fin_entry = DateEntry(frame, date_pattern="yyyy-mm-dd")
        self.fecha_fin_entry.pack(fill="x")

        # Hora Fin (AM/PM)
        hora_frame_fin = ttk.Frame(frame)
        hora_frame_fin.pack(fill="x", pady=2)
        self.hora_fin = ttk.Combobox(hora_frame_fin, values=[f"{h:02}" for h in range(1, 13)], width=5)
        self.hora_fin.set("12")
        self.hora_fin.pack(side="left")
        self.minuto_fin = ttk.Combobox(hora_frame_fin, values=[f"{m:02}" for m in range(0, 60, 5)], width=5)
        self.minuto_fin.set("00")
        self.minuto_fin.pack(side="left", padx=5)
        self.ampm_fin = ttk.Combobox(hora_frame_fin, values=["AM", "PM"], width=5)
        self.ampm_fin.set("PM")
        self.ampm_fin.pack(side="left")

        # Estado
        self.estado_var = tk.StringVar(value="activo")
        ttk.Label(frame, text="Estado").pack(anchor="w", pady=(10, 0))
        estado_combo = ttk.Combobox(frame, textvariable=self.estado_var, values=["activo", "programado", "cancelado"])
        estado_combo.pack(fill="x")

        # Botón guardar
        ttk.Button(frame, text="Guardar", command=self.guardar_evento).pack(pady=20)

    def convertir_a_24h(self, hora, minuto, ampm):
        hora = int(hora)
        minuto = int(minuto)
        if ampm == "PM" and hora != 12:
            hora += 12
        elif ampm == "AM" and hora == 12:
            hora = 0
        return f"{hora:02}:{minuto:02}"

    def guardar_evento(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}
        datos["estado"] = self.estado_var.get()

        # Combinar fecha y hora
        hora_inicio = self.convertir_a_24h(self.hora_inicio.get(), self.minuto_inicio.get(), self.ampm_inicio.get())
        hora_fin = self.convertir_a_24h(self.hora_fin.get(), self.minuto_fin.get(), self.ampm_fin.get())

        fecha_inicio_str = f"{self.fecha_inicio_entry.get()} {hora_inicio}"
        fecha_fin_str = f"{self.fecha_fin_entry.get()} {hora_fin}"

        # Validar fechas
        valido, fechas = Validaciones.validar_fecha_evento(fecha_inicio_str, fecha_fin_str)
        if not valido:
            messagebox.showerror("Error de fecha", fechas)
            return

        # Validar capacidad
        valido_cap, cap = Validaciones.validar_numero_entero(datos["capacidad_maxima"], "capacidad", minimo=1)
        if not valido_cap:
            messagebox.showerror("Error de capacidad", cap)
            return

        # Asignar datos al objeto
        self.evento.nombre = datos["nombre"]
        self.evento.descripcion = datos["descripcion"]
        self.evento.fecha_inicio = fechas["fecha_inicio"]
        self.evento.fecha_fin = fechas["fecha_fin"]
        self.evento.ubicacion = datos["ubicacion"]
        self.evento.capacidad_maxima = cap
        self.evento.categoria = datos["categoria"]
        self.evento.estado = datos["estado"]

        # Guardar
        if self.evento.guardar():
            messagebox.showinfo("Éxito", "Evento guardado correctamente.")
            if self.callback:
                self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar el evento.")


