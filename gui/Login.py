import tkinter as tk
from tkinter import font, messagebox
import sys
import os

# Importa la clase MainWindow desde main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import MainWindow

class EventoLogin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Eventos - Login")
        self.geometry("420x520")
        self.resizable(False, False)
        self.configure(bg="#1a1a2e")

        # Center the window on the screen
        self.eval('tk::PlaceWindow . center')

        # Fonts
        self.title_font = font.Font(family="Montserrat", size=28, weight="bold")
        self.subtitle_font = font.Font(family="Montserrat", size=11, weight="normal")
        self.label_font = font.Font(family="Montserrat", size=13)
        self.entry_font = font.Font(family="Montserrat", size=12)
        self.button_font = font.Font(family="Montserrat", size=15, weight="bold")

        # Colors
        self.bg_color = "#1a1a2e"
        self.fg_color = "#eaeaea"
        self.accent_color = "#e94560"
        self.entry_bg = "#16213e"
        self.entry_fg = "#eaeaea"
        self.button_bg = "#e94560"
        self.button_hover = "#d73756"
        self.error_color = "#ff6b6b"

        self.create_widgets()

    def create_widgets(self):
        # Create a header frame with a gradient-like banner by layered frames
        self.header_frame = tk.Frame(self, bg=self.bg_color)
        self.header_frame.pack(fill='x', pady=(20, 30))

        # Title label
        self.title_label = tk.Label(self.header_frame, text="Gestor de Eventos", bg=self.bg_color,
                                    fg=self.accent_color, font=self.title_font)
        self.title_label.pack()

        # Subtitle label to give theme
        self.subtitle_label = tk.Label(self.header_frame, text="Inicia sesión para continuar",
                                       bg=self.bg_color, fg=self.fg_color,
                                       font=self.subtitle_font)
        self.subtitle_label.pack(pady=(5,0))

        # Username label and entry
        self.username_label = tk.Label(self, text="Usuario", bg=self.bg_color,
                                       fg=self.fg_color, font=self.label_font, anchor="w")
        self.username_label.pack(fill='x', padx=60, pady=(0, 7))

        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(self, textvariable=self.username_var, bg=self.entry_bg,
                                       fg=self.entry_fg, font=self.entry_font, borderwidth=0,
                                       insertbackground=self.entry_fg)
        self.username_entry.pack(fill='x', padx=60, ipady=10, pady=(0, 20))
        self.username_entry.focus()

        # Password label and entry
        self.password_label = tk.Label(self, text="Contraseña", bg=self.bg_color,
                                       fg=self.fg_color, font=self.label_font, anchor="w")
        self.password_label.pack(fill='x', padx=60, pady=(0, 7))

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self, textvariable=self.password_var, bg=self.entry_bg,
                                       fg=self.entry_fg, font=self.entry_font, show="*",
                                       borderwidth=0, insertbackground=self.entry_fg)
        self.password_entry.pack(fill='x', padx=60, ipady=10, pady=(0, 30))

        # Login button
        self.login_button = tk.Label(self, text="Iniciar Sesión", bg=self.button_bg,
                                     fg=self.fg_color, font=self.button_font,
                                     cursor="hand2", relief="flat", bd=0, padx=15, pady=12)
        self.login_button.pack(padx=60, fill='x')
        self.login_button.bind("<Enter>", self.on_button_hover)
        self.login_button.bind("<Leave>", self.on_button_leave)
        self.login_button.bind("<Button-1>", self.on_login_clicked)

        # Message label for feedback
        self.message_label = tk.Label(self, text="", bg=self.bg_color, fg=self.error_color, font=self.label_font)
        self.message_label.pack(pady=15)

        # Decorative footer with event theme text
        self.footer_label = tk.Label(self, text="© 2024 Gestor de Eventos. Todos los derechos reservados.",
                                     bg=self.bg_color, fg="#555a77", font=("Montserrat", 9))
        self.footer_label.pack(side="bottom", pady=20)

    def on_button_hover(self, event):
        self.login_button.config(bg=self.button_hover)

    def on_button_leave(self, event):
        self.login_button.config(bg=self.button_bg)

    def on_login_clicked(self, event):
        username = self.username_var.get().strip().lower()
        password = self.password_var.get().strip()

        # Diccionario de usuarios válidos (en minúsculas)
        usuarios_validos = {
            "ariana": "Hola123",
            "razor": "Gaia05"
        }

        if not username or not password:
            self.message_label.config(text="Por favor, ingresa usuario y contraseña.")
            return

        if username in usuarios_validos and password == usuarios_validos[username]:
            self.message_label.config(text="")
            messagebox.showinfo("Acceso concedido", f"¡Bienvenido/a, {username.capitalize()}!")
            self.destroy()  # Cierra la ventana de login
            main_app = MainWindow()  # Abre la ventana principal
            main_app.root.mainloop()
        else:
            self.message_label.config(text="Usuario o contraseña incorrectos.")

if __name__ == "__main__":
    app = EventoLogin()
    app.mainloop()


