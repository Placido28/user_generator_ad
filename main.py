import customtkinter as ctk
import tkinter as tk
import os
import pandas as pd
from tkinter import messagebox
from PIL import Image
from ad_connector import conectar_ad, usuario_existe_ad
from username_generator import generar_usuario_disponible
from ventana_resultado import VentanaResultado

MAX_FILAS = 10
RUTA_BASE = os.path.dirname(__file__)
ruta_logo = os.path.join(RUTA_BASE, "logo_prymera.png")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.resultados = []
        self.entries = []
        self.fuente = ("Segoe UI", 14)
        self.title("Generador de Usuarios AD")
        self.logo_img_main = ctk.CTkImage(Image.open(ruta_logo), size=(80, 45))
        self.logo_img_login = ctk.CTkImage(Image.open(ruta_logo), size=(120, 70))
        self.withdraw()  # Oculta la ventana principal hasta login exitoso
        self.crear_login()

        try:
            df_inactivos = pd.read_csv("data/usuarios_inactivos.csv", encoding='utf-8')  # Reemplaza con la ruta real
            self.codigos_inactivos = set(df_inactivos['COD_USR'].dropna().astype(str).str.strip())
            #print("Codigos inactivos cargados:", self.codigos_inactivos)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo de usuarios inactivos:\n{e}")
            self.codigos_inactivos = set()   

    def crear_login(self):
        self.login_win = ctk.CTkToplevel(self)
        self.login_win.title("Conexión Active Directory")
        self.login_win.configure(fg_color="#E3F2FD")  # Fondo celeste suave
        centrar_ventana(self.login_win, 400, 320)
        self.login_win.resizable(False, False)
        self.login_win.protocol("WM_DELETE_WINDOW", self.cerrar_todo)
        self.login_win.grab_set()
        self.login_win.focus_set()

        # Contenedor estilo tarjeta
        frame = ctk.CTkFrame(self.login_win, corner_radius=12, fg_color="white")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Logo
        ctk.CTkLabel(frame, image=self.logo_img_login, text="", fg_color="transparent").grid(row=0, column=0, columnspan=2, pady=(5, 10))

        # Título
        ctk.CTkLabel(frame, text="Acceso al Sistema de Usuarios",
                    font=("Segoe UI", 18, "bold"), text_color="#0D47A1").grid(
            row=1, column=0, columnspan=2, pady=(0, 15)
        )

        # Usuario
        ctk.CTkLabel(frame, text="Usuario:", font=("Segoe UI", 14,"bold"), text_color="#0D47A1").grid(row=2, column=0, padx=10, pady=8, sticky="e")
        self.entry_user = ctk.CTkEntry(frame, font=self.fuente, width=220,
                                    placeholder_text="Ingrese su usuario",
                                    fg_color="white", border_color="#90CAF9",
                                    text_color="black")
        self.entry_user.grid(row=2, column=1, padx=10, pady=8)

        # Contraseña
        ctk.CTkLabel(frame, text="Contraseña:", font=("Segoe UI", 14,"bold"), text_color="#0D47A1").grid(row=3, column=0, padx=10, pady=8, sticky="e")
        self.entry_pass = ctk.CTkEntry(frame, font=self.fuente, show="*", width=220,
                                    placeholder_text="Ingrese su contraseña",
                                    fg_color="white", border_color="#90CAF9",
                                    text_color="black")
        self.entry_pass.grid(row=3, column=1, padx=10, pady=8)

        # Botón de ingreso
        btn_login = ctk.CTkButton(
            frame,
            text="INGRESAR",
            font=("Segoe UI", 14,"bold"),
            width=120,
            height=36,
            fg_color="#FBC02D",
            hover_color="#FBA22D",
            text_color="white",
            corner_radius=8,
            command=self.intentar_login
        )
        btn_login.grid(row=4, column=0, columnspan=2, pady=20)

        self.entry_user.focus_set()
        self.login_win.bind('<Return>', lambda e: self.intentar_login())

    def intentar_login(self):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        if not user or not password:
            messagebox.showerror("Error", "Por favor, ingrese usuario y contraseña")
            return
        try:
            self.conn = conectar_ad(user, password)
            self.login_win.destroy()
            self.deiconify()  # Muestra la ventana principal
            self.crear_principal()
        except Exception as e:
            messagebox.showerror("Error", f"Error de autenticación:\n{e}")
            self.entry_pass.delete(0, tk.END)  # Borra solo la contraseña
            self.entry_pass.focus()  # Enfoca el campo para volver a escribir
    
    def mostrar_ayuda(self):
        ventana_ayuda = ctk.CTkToplevel(self)
        ventana_ayuda.title("Guía del Sistema")
        centrar_ventana(ventana_ayuda, 460, 300)
        ventana_ayuda.resizable(False, False)
        ventana_ayuda.grab_set()

        ayuda_texto = (
            "🛈 Esta herramienta permite generar nombres de usuario para Active Directory.\n\n"
            "1. Ingrese su usuario y contraseña para conectarse al AD.\n"
            "2. Complete los campos de nombres y apellidos.\n"
            "3. Presione 'Generar Usuarios'.\n"
            "4. Se mostrarán los nombres sugeridos según disponibilidad.\n"
            "5. Puede copiar con doble clic o Ctrl+C.\n\n"
            "✔ Solo es obligatorio llenar: Nombre 1, Apellido Paterno y Apellido Materno."
        )

        texto = ctk.CTkTextbox(
            ventana_ayuda,
            wrap="word",
            font=("Segoe UI", 13),
            text_color="#1B1B1B",
            fg_color="#FAFAFA",
            corner_radius=8,
            border_width=1
        )
        texto.insert("1.0", ayuda_texto)
        texto.configure(state="disabled")
        texto.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkButton(
            ventana_ayuda,
            text="Cerrar",
            fg_color="#B0BEC5",
            hover_color="#90A4AE",
            text_color="white",
            corner_radius=6,
            command=ventana_ayuda.destroy
        ).pack(pady=(0, 12))

    def crear_principal(self):
        import re

        def solo_letras(caracter):
            # Permite letras, tildes y espacios
            return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]*", caracter))

        vcmd = (self.register(solo_letras), "%P")
        
        columnas = ["Nombre 1", "Nombre 2", "Apellido Paterno", "Apellido Materno"]
        centrar_ventana(self, 900, 580)
        self.resizable(False, False)
        self.configure(fg_color="#E3F2FD")  # Fondo general claro, profesional

        # ------------------ NAVBAR ------------------
        navbar = ctk.CTkFrame(self, height=60, fg_color="#1976D2", corner_radius=0)
        navbar.grid(row=0, column=0, columnspan=4, sticky="nwe")
        navbar.grid_propagate(False)
        navbar.grid_columnconfigure(0, weight=1)  # izquierda (logo)
        navbar.grid_columnconfigure(1, weight=2)  # centro (título)
        navbar.grid_columnconfigure(2, weight=1)  # derecha (botón ayuda)

        ctk.CTkLabel(navbar, image=self.logo_img_main, text="", fg_color="transparent").grid(row=0, column=0, padx=(15, 5), pady=10, sticky="nsw")
        ctk.CTkLabel(navbar, text="Generador de Usuarios - Caja Prymera",
             font=("Segoe UI", 16, "bold"), text_color="white", fg_color="transparent").grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        # Botón de ayuda
        btn_ayuda = ctk.CTkButton(navbar,
            text="❓ Guía",
            font=("Segoe UI", 14,"bold"),
            fg_color="#42A5F5",
            hover_color="#1E88E5",
            text_color="white",
            corner_radius=6,
            width=90,
            height=32,
            command=self.mostrar_ayuda
        )
        btn_ayuda.grid(row=0, column=2, padx=(0, 15), pady=10, sticky="nse")

        # ------------------ TÍTULOS ------------------
        for col, texto in enumerate(columnas):
            ctk.CTkLabel(self, text=texto, font=("Segoe UI", 14, "bold"), text_color="#333333").grid(row=1, column=col, padx=8, pady=(16, 8))

        # ------------------ INPUTS ------------------
        for fila in range(MAX_FILAS):
            fila_entries = []
            color_fila = "#FFFFFF" if fila % 2 == 0 else "#F0F8FF"  # Alternar colores

            for col in range(len(columnas)):
                entry = ctk.CTkEntry(
                    self,
                    font=self.fuente,
                    width=180,
                    border_width=1,
                    corner_radius=6,
                    fg_color=color_fila,
                    text_color="#1B1B1B",
                    validate="key",
                    validatecommand=vcmd
                )
                entry.grid(row=fila + 2, column=col, padx=8, pady=4)
                fila_entries.append(entry)

            self.entries.append(fila_entries)
        # ------------------ BOTONES ------------------
        botones_frame = ctk.CTkFrame(self, fg_color="transparent")
        botones_frame.grid(row=MAX_FILAS + 3, column=0, columnspan=4, pady=20, sticky="we")
        botones_frame.grid_columnconfigure((0, 1, 2), weight=1)

        btn_generar = ctk.CTkButton(
            botones_frame,
            text="Generar Usuarios",
            font=("Segoe UI", 16, "bold"),
            fg_color="#FBC02D",
            hover_color="#FBA22D",
            text_color="white",
            width=150,
            height=40,
            corner_radius=10,
            command=self.generar_usuarios
        )
        btn_generar.grid(row=0, column=0, padx=16, sticky="we")

        btn_limpiar = ctk.CTkButton(
            botones_frame,
            text="Limpiar",
            font=("Segoe UI", 16, "bold"),
            fg_color="#B0BEC5",
            hover_color="#90A4AE",
            text_color="black",
            width=150,
            height=40,
            corner_radius=10,
            command=self.limpiar_celdas
        )
        btn_limpiar.grid(row=0, column=1, padx=16, sticky="we")

        btn_cancelar = ctk.CTkButton(
            botones_frame,
            text="Cancelar",
            font=("Segoe UI", 16, "bold"),
            fg_color="#1565C0",
            hover_color="#043E80",
            text_color="white",
            width=150,
            height=40,
            corner_radius=10,
            command=self.cerrar_todo
        )
        btn_cancelar.grid(row=0, column=2, padx=16, sticky="we")

        self.grid_columnconfigure(tuple(range(len(columnas))), weight=1)
        self.entries[0][0].focus_set()
        self.bind('<Return>', lambda e: self.generar_usuarios())


    def limpiar_celdas(self):
        for fila_entries in self.entries:
            for entry in fila_entries:
                entry.delete(0, tk.END)
        self.entries[0][0].focus_set()

    def generar_usuarios(self):
        self.resultados.clear()
        usuarios_generados = set()
        codigos_generados = set()

        for fila_entries in self.entries:
            nombre1 = fila_entries[0].get().strip()
            nombre2 = fila_entries[1].get().strip()
            ap_paterno = fila_entries[2].get().strip()
            ap_materno = fila_entries[3].get().strip()

            if not (nombre1 and ap_paterno and ap_materno):
                continue  # Saltar filas incompletas

            def es_valido(usuario):
                if usuario in usuarios_generados:
                    return False
                if usuario_existe_ad(self.conn, usuario):
                    return False
                codigo = usuario[:6].lower()
                if codigo in self.codigos_inactivos or codigo in codigos_generados:
                    return False
                return True

            usuario = generar_usuario_disponible(
                nombre1, nombre2, ap_paterno, ap_materno,
                es_valido
            )

            if usuario:
                codigo_final = usuario[:6].lower()
                usuarios_generados.add(usuario)
                codigos_generados.add(codigo_final)
            else:
                usuario = "SIN DISPONIBILIDAD"
                codigo_final = "N/A"

            nombre_completo = f"{nombre1.title()} {nombre2.title()} {ap_paterno.title()} {ap_materno.title()}".strip()
            self.resultados.append((nombre_completo, usuario, codigo_final))

        if self.resultados:
            self.mostrar_resultado()
        else:
            messagebox.showwarning("Advertencia", "Debe completar al menos una fila con Nombre 1, Apellido Paterno y Materno.")

    def mostrar_resultado(self):
        VentanaResultado(self, self.resultados)

    def cerrar_todo(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()