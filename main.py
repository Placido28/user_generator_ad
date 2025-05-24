import customtkinter as ctk
from tkinter import ttk, messagebox
from ad_connector import conectar_ad, usuario_existe_ad
from username_generator import generar_usuario_disponible

MAX_FILAS = 10

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
        self.withdraw()  # Oculta la ventana principal hasta login exitoso
        self.crear_login()
        self.iconbitmap("logo.png")

    def crear_login(self):
        self.login_win = ctk.CTkToplevel(self)
        self.login_win.title("Conexión Active Directory")
        centrar_ventana(self.login_win, 370, 200)
        self.login_win.resizable(False, False)
        self.login_win.protocol("WM_DELETE_WINDOW", self.cerrar_todo)
        self.login_win.grab_set()
        self.login_win.focus_set()

        frame = ctk.CTkFrame(self.login_win)#, fg_color="#2623C7")
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(frame, text="USUARIO:", font=self.fuente).grid(row=0, column=0, padx=10, pady=12)
        self.entry_user = ctk.CTkEntry(frame, font=self.fuente, width=200)
        self.entry_user.grid(row=0, column=1, padx=10, pady=12)

        ctk.CTkLabel(frame, text="CONTRASEÑA:", font=self.fuente).grid(row=1, column=0, padx=10, pady=12)
        self.entry_pass = ctk.CTkEntry(frame, show="*", font=self.fuente, width=200)
        self.entry_pass.grid(row=1, column=1, padx=10, pady=12)

        btn_login = ctk.CTkButton(
            frame,
            text="INGRESAR",
            font=self.fuente,
            width=90,     # ancho del botón en píxeles
            height=40,     # alto del botón
            corner_radius=10,  # esquinas redondeadas
            command=self.intentar_login,
            # fg_color="#e6e6e6",      # Azul oscuro (igual que el fondo)
            # hover_color="#e6e6e6",    # Color al pasar el mouse (opcional)
            # text_color="#050505"
        )
        btn_login.grid(row=2, column=1, columnspan=2, pady=20, sticky="nsew")

        self.entry_user.focus_set()
        self.login_win.bind('<Return>', lambda e: self.intentar_login())

    def intentar_login(self):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        if not user or not password:
            messagebox.showerror("Error", "Ingrese usuario y contraseña")
            return
        try:
            self.conn = conectar_ad(user, password)
            self.login_win.destroy()
            self.deiconify()  # Muestra la ventana principal
            self.crear_principal()
        except Exception as e:
            messagebox.showerror("Error", f"Error de autenticación:\n{e}")

    def crear_principal(self):
        columnas = ["Nombre 1", "Nombre 2", "Apellido Paterno", "Apellido Materno"]
        # Tamaño recomendado para que todo sea visible
        centrar_ventana(self, 900, 520)
        self.resizable(False, False)

        for col, texto in enumerate(columnas):
            ctk.CTkLabel(self, text=texto, font=self.fuente).grid(row=0, column=col, padx=8, pady=8)

        for fila in range(MAX_FILAS):
            fila_entries = []
            for col in range(len(columnas)):
                entry = ctk.CTkEntry(self, font=self.fuente, width=180)
                entry.grid(row=fila+1, column=col, padx=8, pady=4)
                fila_entries.append(entry)
            self.entries.append(fila_entries)

        btn_generar = ctk.CTkButton(self, text="Generar Usuarios", font=self.fuente, command=self.generar_usuarios)
        btn_generar.grid(row=MAX_FILAS+2, column=0, columnspan=2, pady=18, sticky="we", padx=8)

        btn_cancelar = ctk.CTkButton(self, text="Cancelar", font=self.fuente, command=self.cerrar_todo)
        btn_cancelar.grid(row=MAX_FILAS+2, column=2, columnspan=2, pady=18, sticky="we", padx=8)

        self.grid_columnconfigure(tuple(range(len(columnas))), weight=1)
        self.entries[0][0].focus_set()
        self.bind('<Return>', lambda e: self.generar_usuarios())

    def generar_usuarios(self):
        self.resultados.clear()
        for fila_entries in self.entries:
            nombre1 = fila_entries[0].get().strip()
            nombre2 = fila_entries[1].get().strip()
            ap_paterno = fila_entries[2].get().strip()
            ap_materno = fila_entries[3].get().strip()
            if nombre1 and ap_paterno and ap_materno:
                usuario = generar_usuario_disponible(
                    nombre1, nombre2, ap_paterno, ap_materno,
                    lambda u: usuario_existe_ad(self.conn, u)
                )
                nombre_completo = f"{nombre1.title()} {nombre2.title()} {ap_paterno.title()} {ap_materno.title()}".strip()
                self.resultados.append((nombre_completo, usuario if usuario else "SIN DISPONIBILIDAD"))
        if self.resultados:
            self.mostrar_resultado()
        else:
            messagebox.showwarning("Advertencia", "Debe completar al menos una fila con Nombre 1, Apellido Paterno y Materno.")

    def mostrar_resultado(self):
        ventana_resultado = ctk.CTkToplevel(self)
        ventana_resultado.title("Usuarios Sugeridos")
        centrar_ventana(ventana_resultado, 500, 300)
        ventana_resultado.grab_set()

        tree = ttk.Treeview(
            ventana_resultado,
            columns=("Nombre Completo", "Usuario"),
            show="headings",
            selectmode="extended"
        )
        tree.heading("Nombre Completo", text="Nombre Completo")
        tree.heading("Usuario", text="Usuario")
        tree.column("Nombre Completo", anchor="w", width=280)
        tree.column("Usuario", anchor="center", width=140)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for nombre, usuario in self.resultados:
            tree.insert("", "end", values=(nombre, usuario))

        def copiar_celda(event):
            region = tree.identify("region", event.x, event.y)
            if region == "cell":
                row_id = tree.identify_row(event.y)
                col = tree.identify_column(event.x)
                if row_id and col:
                    values = tree.item(row_id, "values")
                    col_index = int(col.replace("#", "")) - 1
                    if 0 <= col_index < len(values):
                        valor = values[col_index]
                        try:
                            ventana_resultado.clipboard_clear()
                            ventana_resultado.clipboard_append(valor)
                        except Exception:
                            pass

        def copiar_seleccion(event=None):
            if ventana_resultado.focus_get() == tree:
                selected = tree.selection()
                if selected:
                    texto = "\n".join(
                        ["\t".join(tree.item(item, 'values')) for item in selected]
                    )
                    try:
                        ventana_resultado.clipboard_clear()
                        ventana_resultado.clipboard_append(texto)
                    except Exception:
                        pass
                return "break"

        tree.bind("<Control-c>", copiar_seleccion)
        tree.bind("<Double-1>", copiar_celda)

    def cerrar_todo(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()