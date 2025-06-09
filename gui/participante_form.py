'''mobal para partisipante_form.py'''
import tkinter as tk
from tkinter import ttk, messagebox
from models.participante import Participante
from utils.validations import Validaciones

class ParticipanteForm(tk.Toplevel):
    def __init__(self, master=None, callback=None):
        super().__init__(master)
        self.title("Nuevo Participante")
        self.geometry("400x450")
        self.resizable(False, False)
        self.callback = callback

        self.participante = Participante()

        self.crear_widgets()

    def crear_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        campos = [
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Email", "email"),
            ("Teléfono", "telefono")
        ]

        self.entries = {}
        for label, key in campos:
            ttk.Label(frame, text=label).pack(anchor="w", pady=(10, 0))
            entry = ttk.Entry(frame)
            entry.pack(fill="x")
            self.entries[key] = entry

        ttk.Button(frame, text="Guardar", command=self.guardar_participante).pack(pady=20)

    def guardar_participante(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}

        errores = []

        for campo in ["nombre", "apellido"]:
            valido, mensaje = Validaciones.validar_nombre(datos[campo], campo)
            if not valido:
                errores.append(mensaje)

        valido, mensaje = Validaciones.validar_email(datos["email"])
        if not valido:
            errores.append(mensaje)

        valido, mensaje = Validaciones.validar_telefono(datos["telefono"])
        if not valido:
            errores.append(mensaje)

        if errores:
            messagebox.showerror("Errores de validación", "\n".join(errores))
            return

        self.participante.nombre = datos["nombre"]
        self.participante.apellido = datos["apellido"]
        self.participante.email = datos["email"]
        self.participante.telefono = datos["telefono"]

        if self.participante.guardar():
            messagebox.showinfo("Éxito", "Participante guardado correctamente.")
            if self.callback:
                self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar el participante.")
