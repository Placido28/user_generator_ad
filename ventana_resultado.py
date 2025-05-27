import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import csv

class VentanaResultado(ctk.CTkToplevel):
    def __init__(self, parent, resultados):
        super().__init__(parent)
        self.title("Usuarios Sugeridos")
        self.geometry("640x500")
        self.resizable(False, False)
        self.resultados = resultados

        # Mostrar encima de la ventana principal
        self.lift()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

        # Evitar interacción con la ventana principal mientras esté activa
        self.grab_set()
        self.focus()

        # Cambiar fondo general a un celeste suave
        self.configure(fg_color="#F3F6F9")

        # FRAME PRINCIPAL CON ESTILO
        contenedor = ctk.CTkFrame(self, corner_radius=15, fg_color="#ffffff")
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(contenedor, text="Resultados Generados", font=("Segoe UI", 20, "bold"), text_color="#1976D2").pack(pady=(10, 15))

        # TREEVIEW
        self.tree = ttk.Treeview(contenedor, columns=("Nombre", "Usuario", "Codigo"), show="headings", height=10)
        self.tree.heading("Nombre", text="Nombre Completo")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Codigo", text="Código")
        self.tree.column("Nombre", width=330, anchor="w")
        self.tree.column("Usuario", width=150, anchor="center")
        self.tree.column("Codigo", width=100, anchor="center")
        self.tree.bind("<Double-1>", self.copiar_celda)
        self.tree.bind("<Control-c>", self.copiar_seleccion)


        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#ffffff", foreground="#000000", rowheight=28, fieldbackground="#ffffff", font=("Segoe UI", 12))
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#B3E5FC")

        self.tree.pack(fill="x", padx=10, pady=5)

        # ZEBRA STRIPES
        for i, (nombre, usuario, codigo) in enumerate(resultados):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(nombre, usuario, codigo), tags=(tag,))
        self.tree.tag_configure("evenrow", background="#E3F2FD")
        self.tree.tag_configure("oddrow", background="#ffffff")

        # BOTONES
        boton_frame = ctk.CTkFrame(contenedor, fg_color="#F0F0F0")
        boton_frame.pack(pady=(15, 5), fill="x")

        btn_copiar = ctk.CTkButton(boton_frame, text="📋 Copiar todo",font=("Segoe UI", 14,"bold"), fg_color="#FBC02D", hover_color="#FBA22D", width=140, command=self.copiar_todo)
        btn_copiar.pack(side="left", padx=10)

        btn_exportar = ctk.CTkButton(boton_frame, text="📁 Exportar CSV",font=("Segoe UI", 14,"bold"), fg_color="#FBC02D", hover_color="#FBA22D", width=140, command=self.exportar_csv)
        btn_exportar.pack(side="left", padx=10)

        btn_cerrar = ctk.CTkButton(boton_frame, text="❌ Cerrar",font=("Segoe UI", 14,"bold"), fg_color="#1565C0", hover_color="#043E80", width=140, command=self.destroy)
        btn_cerrar.pack(side="right", padx=10)

        # LABEL DE CANTIDAD
        ctk.CTkLabel(contenedor, text=f"Total: {len(resultados)} usuario(s) generados.", font=("Segoe UI", 12), text_color="#424242").pack(pady=(5, 0))

    def copiar_todo(self):
        texto = "\n".join(["\t".join(self.tree.item(i, "values")) for i in self.tree.get_children()])
        self.clipboard_clear()
        self.clipboard_append(texto)
        messagebox.showinfo("Copiado", "Los resultados han sido copiados al portapapeles.")

    def exportar_csv(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if ruta:
            try:
                with open(ruta, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Nombre Completo", "Usuario", "Código"])
                    for nombre, usuario, codigo in self.resultados:
                        writer.writerow([nombre, usuario, codigo])
                messagebox.showinfo("Exportado", f"Archivo CSV guardado en:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
    
    def copiar_celda(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.tree.identify_row(event.y)
            col = self.tree.identify_column(event.x)
            if row_id and col:
                values = self.tree.item(row_id, "values")
                col_index = int(col.replace("#", "")) - 1
                if 0 <= col_index < len(values):
                    valor = values[col_index]
                    self.clipboard_clear()
                    self.clipboard_append(valor)

    def copiar_seleccion(self, event=None):
        selected = self.tree.selection()
        if selected:
            texto = "\n".join(["\t".join(self.tree.item(i, "values")) for i in selected])
            self.clipboard_clear()
            self.clipboard_append(texto)
        return "break"
