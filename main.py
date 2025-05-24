# main.py

import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
from ad_connector import conectar_ad, usuario_existe_ad
from username_generator import generar_usuario_disponible

MAX_FILAS = 10

# ------LOGIN--------
def login():
    def intentar_login(event=None):
        user = entry_user.get().strip()
        password = entry_pass.get().strip()
        if not user or not password:
            messagebox.showerror("Error", "Ingrese usuario y contraseña")
            return
        try:
            global conn
            conn = conectar_ad(user, password)
            login_window.destroy()
            abrir_ventana_principal()
        except Exception as e:
            messagebox.showerror("Error", f"Error de autenticacion:\n{e}")

    fuente = ("Segoe UI", 11)
    login_window = tk.Tk()
    login_window.title("Conexión Active Directory")
    login_window.minsize(350, 170)
    login_window.configure(padx=24, pady=24)

    tk.Label(login_window, text="Usuario:", font=fuente).grid(row=0, column=0, sticky="e", pady=7)
    entry_user = tk.Entry(login_window, font=fuente)
    entry_user.grid(row=0, column=1, sticky="we", pady=7)

    tk.Label(login_window, text="Contraseña:", font=fuente).grid(row=1, column=0, sticky="e", pady=7)
    entry_pass = tk.Entry(login_window, show="*", font=fuente)
    entry_pass.grid(row=1, column=1, sticky="we", pady=7)

    btn_login = tk.Button(login_window, text="Ingresar", font=fuente, command=intentar_login)
    btn_login.grid(row=2,column=0, columnspan=2, pady=18, sticky="we")

    login_window.grid_columnconfigure(1, weight=1)
    entry_user.focus_set()
    login_window.bind('<Return>', intentar_login)
    centrar_ventana(login_window)
    login_window.mainloop()

# ---------- CENTRAR VENTANA ----------
def centrar_ventana(win):
    win.update_idletasks()
    ancho = win.winfo_width()
    alto = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (ancho // 2)
    y = (win.winfo_screenheight() // 2) - (alto // 2)
    win.geometry(f"{ancho}x{alto}+{x}+{y}")

# ---------- VENTANA PRINCIPAL ----------
def abrir_ventana_principal():
    resultados = []

    fuente = ("Segoe UI", 11)
    ventana = tk.Tk()
    ventana.title("Generador de Usuarios AD")
    ventana.minsize(650, 350)
    ventana.configure(padx=24, pady=24)

    columnas = ["Nombre 1", "Nombre 2", "Apellido Paterno", "Apellido Materno"]
    entries = []

    # Encabezados
    for col, texto in enumerate(columnas):
        tk.Label(ventana, text=texto, font=fuente).grid(row=0, column=col, padx=5, pady=5, sticky="we")

    # Entradas (10 filas)
    for fila in range(MAX_FILAS):
        fila_entries = []
        for col in range(len(columnas)):
            entry = tk.Entry(ventana, font=fuente, width=18)
            entry.grid(row=fila+1, column=col, padx=5, pady=3, sticky="we")
            fila_entries.append(entry)
        entries.append(fila_entries)

    def generar_usuarios(event=None):
        resultados.clear()
        for fila_entries in entries:
            nombre1 = fila_entries[0].get().strip()
            nombre2 = fila_entries[1].get().strip()
            ap_paterno = fila_entries[2].get().strip()
            ap_materno = fila_entries[3].get().strip()
            if nombre1 and ap_paterno and ap_materno:
                usuario = generar_usuario_disponible(
                    nombre1, nombre2, ap_paterno, ap_materno,
                    lambda u: usuario_existe_ad(conn, u)
                )
                nombre_completo = f"{nombre1.title()} {nombre2.title()} {ap_paterno.title()} {ap_materno.title()}".strip()
                resultados.append((nombre_completo, usuario if usuario else "SIN DISPONIBILIDAD"))
        if resultados:
            mostrar_resultado()
        else:
            messagebox.showwarning("Advertencia", "Debe completar al menos una fila con Nombre 1, Apellido Paterno y Materno.")

    def mostrar_resultado():
        ventana_resultado = tk.Toplevel(ventana)
        ventana_resultado.title("Usuarios Sugeridos")
        ventana_resultado.minsize(400, 220)
        ventana_resultado.configure(padx=14, pady=14)
        ventana_resultado.grab_set()  # Modal

        # Permitir selección de filas completas
        tree = ttk.Treeview(
            ventana_resultado,
            columns=("Nombre Completo", "Usuario"),
            show="headings",
            selectmode="extended"  # Permite seleccionar varias filas con Shift/Ctrl
        )
        tree.heading("Nombre Completo", text="Nombre Completo")
        tree.heading("Usuario", text="Usuario")
        tree.column("Nombre Completo", anchor="w", width=250)
        tree.column("Usuario", anchor="center", width=120)
        tree.pack(fill="both", expand=True)

        for nombre, usuario in resultados:
            tree.insert("", "end", values=(nombre, usuario))

        for i, (_, usuario) in enumerate(resultados):
            if usuario == "SIN DISPONIBILIDAD":
                tree.tag_configure("no_disp", foreground="red")
                tree.item(tree.get_children()[i], tags=("no_disp",))
            else:
                tree.tag_configure("disp", foreground="green")
                tree.item(tree.get_children()[i], tags=("disp",))

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
                        ventana_resultado.clipboard_clear()
                        ventana_resultado.clipboard_append(valor)
                        ventana_resultado.update()

        def copiar_seleccion(event=None):
            # Solo copia si el foco está en el treeview
            if ventana_resultado.focus_get() == tree:
                selected = tree.selection()
                if selected:
                    texto = "\n".join(
                        ["\t".join(tree.item(item, 'values')) for item in selected]
                    )
                    ventana_resultado.clipboard_clear()
                    ventana_resultado.clipboard_append(texto)
                    ventana_resultado.update()
                return "break"  # Evita que el evento siga propagándose

        # Solo copia si el foco está en el treeview
        tree.bind("<Control-c>", copiar_seleccion)
        tree.bind("<Double-1>", copiar_celda)


    # Botones
    btn_generar = tk.Button(ventana, text="Generar Usuario", font=fuente, command=generar_usuarios)
    btn_generar.grid(row=MAX_FILAS+2, column=0, columnspan=2, pady=18, sticky="we", padx=5)

    btn_cancelar = tk.Button(ventana, text="Cancelar", font=fuente, command=ventana.destroy)
    btn_cancelar.grid(row=MAX_FILAS+2, column=2, columnspan=2, pady=18, sticky="we", padx=5)

    ventana.grid_columnconfigure(tuple(range(len(columnas))), weight=1)
    entries[0][0].focus_set()
    ventana.bind('<Return>', generar_usuarios)
    centrar_ventana(ventana)
    ventana.mainloop()

# ---------- INICIO ----------
if __name__ == "__main__":
    login()

# import csv
# from username_generator import generar_usuario_disponible
# from ad_connector import conectar_ad, usuario_existe_ad

# input_path = 'data/empleados.csv'
# output_path = 'output/usuarios_generados.csv'

# conn = conectar_ad()  # Conexión al AD
# resultado = []

# with open(input_path, newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         nombre1 = row['Nombre1'].strip()
#         nombre2 = row['Nombre2'].strip()
#         ap_paterno = row['ApellidoPaterno'].strip()
#         ap_materno = row['ApellidoMaterno'].strip()

#         usuario = generar_usuario_disponible(
#             nombre1, nombre2, ap_paterno, ap_materno,
#             lambda u: usuario_existe_ad(conn, u)
#         )

#         resultado.append({
#             "NombreCompleto": f"{nombre1} {nombre2} {ap_paterno} {ap_materno}",
#             "UsuarioSugerido": usuario if usuario else "SIN DISPONIBILIDAD"
#         })

# # Guardar resultados
# with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
#     fieldnames = ['NombreCompleto', 'UsuarioSugerido']
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(resultado)

# print("✅ Consulta contra Active Directory completada.")
