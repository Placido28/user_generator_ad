# main.py

import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
from ad_connector import conectar_ad, usuario_existe_ad
from username_generator import generar_usuario_disponible

MAX_FILAS = 10

# ------LOGIN--------
def login():
    def intentar_login():
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

    login_window = tk.Tk()
    login_window.title("Conexión Active Directory")
    login_window.minsize(320, 150)
    login_window.configure(padx=20, pady=20)        

    tk.Label(login_window, text="Usuario:").grid(row=0, column=0, sticky="e", pady=5)
    entry_user = tk.Entry(login_window)
    entry_user.grid(row=0, column=1, sticky="we", pady=5)

    tk.Label(login_window, text="Contraseña:").grid(row=1, column=0, sticky="e", pady=5)
    entry_pass = tk.Entry(login_window, show="*")
    entry_pass.grid(row=1, column=1, sticky="we", pady=5)

    btn_login = tk.Button(login_window, text="Ingresar", command=intentar_login)
    btn_login.grid(row=2,column=0, columnspan=2, pady=15, sticky="we")

    login_window.grid_columnconfigure(1, weight=1)
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

    def generar_usuario():
        nombre1 = entry_nombre1.get().strip()
        nombre2 = entry_nombre2.get().strip()
        ap_paterno = entry_ap_paterno.get().strip()
        ap_materno = entry_ap_materno.get().strip()

        if not nombre1 or not ap_paterno or not ap_materno:
            messagebox.showerror("Error", "Debe completar al menos nombre1, apellido paterno y materno.")
            return

        usuario = generar_usuario_disponible(
            nombre1, nombre2, ap_paterno, ap_materno,
            lambda u: usuario_existe_ad(conn, u)
        )

        resultados.append((f"{nombre1} {nombre2} {ap_paterno} {ap_materno}", usuario if usuario else "SIN DISPONIBILIDAD"))
        mostrar_resultado()

    def mostrar_resultado():
        ventana_resultado = tk.Toplevel(ventana)
        ventana_resultado.title("Usuarios Sugeridos")
        ventana_resultado.minsize(400, 200)
        ventana_resultado.configure(padx=10, pady=10)

        tree = ttk.Treeview(ventana_resultado, columns=("Nombre Completo", "Usuario"), show="headings")
        tree.heading("Nombre Completo", text="Nombre Completo")
        tree.heading("Usuario", text="Usuario")
        tree.column("Nombre Completo", anchor="w", width=250)
        tree.column("Usuario", anchor="center", width=120)
        tree.pack(fill="both", expand=True)

        # Insertar resultados
        for nombre, usuario in resultados:
            tree.insert("", "end", values=(nombre, usuario))

        # Color personalizado para filas con "SIN DISPONIBILIDAD"
        for i, (_, usuario) in enumerate(resultados):
            if usuario == "SIN DISPONIBILIDAD":
                tree.tag_configure("no_disp", foreground="red")
                tree.item(tree.get_children()[i], tags=("no_disp",))
            else:
                tree.tag_configure("disp", foreground="green")
                tree.item(tree.get_children()[i], tags=("disp",))
        # Hacer seleccionable
        def copiar_seleccion(event=None):
            selected = tree.selection()
            if selected:
                texto = "\n".join(
                    ["\t".join(tree.item(item, 'values')) for item in selected]
                )
                ventana_resultado.clipboard_clear()
                ventana_resultado.clipboard_append(texto)
                ventana_resultado.update()

        # Asignar Ctrl+C para copiar
        ventana_resultado.bind("<Control-c>", copiar_seleccion)
        tree.bind("<Control-c>", copiar_seleccion)

    ventana = tk.Tk()
    ventana.title("Generador de Usuarios AD")
    ventana.minsize(350, 220)
    ventana.configure(padx=20, pady=20)

    tk.Label(ventana, text="Nombre 1:").grid(row=0, column=0, sticky="e", pady=5)
    entry_nombre1 = tk.Entry(ventana)
    entry_nombre1.grid(row=0, column=1, sticky="we", pady=5)

    tk.Label(ventana, text="Nombre 2:").grid(row=1, column=0, sticky="e", pady=5)
    entry_nombre2 = tk.Entry(ventana)
    entry_nombre2.grid(row=1, column=1, sticky="we", pady=5)

    tk.Label(ventana, text="Apellido Paterno:").grid(row=2, column=0, sticky="e", pady=5)
    entry_ap_paterno = tk.Entry(ventana)
    entry_ap_paterno.grid(row=2, column=1, sticky="we", pady=5)

    tk.Label(ventana, text="Apellido Materno:").grid(row=3, column=0, sticky="e", pady=5)
    entry_ap_materno = tk.Entry(ventana)
    entry_ap_materno.grid(row=3, column=1, sticky="we", pady=5)

    btn_generar = tk.Button(ventana, text="Generar Usuario", command=generar_usuario)
    btn_generar.grid(row=4,column=0, columnspan=2, pady=15, sticky="we")

    ventana.grid_columnconfigure(1, weight=1)

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
