import customtkinter as ctk
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class EditUserWindow(ctk.CTkToplevel):
    def __init__(self, parent, user_data, on_save):
        super().__init__(parent)
        self.title("Editar Usuario")
        self.geometry("400x500")
        
        # Datos del usuario y callback
        self.user_data = user_data
        self.on_save = on_save
        
        # Roles disponibles
        self.roles = ["Admin", "Doctor"]
        
        # Hacer la ventana modal
        self.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        title = ctk.CTkLabel(self, text="Editar Usuario", font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        # Frame para los campos
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Campos normales (nombre y email)
        fields = [
            ("Nombre:", self.user_data[0]),
            ("Email:", self.user_data[1])
        ]
        
        self.entries = {}
        
        for label_text, default_value in fields:
            # Container para cada campo
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10)
            
            # Label
            label = ctk.CTkLabel(field_frame, text=label_text)
            label.pack(anchor="w")
            
            # Entry
            entry = ctk.CTkEntry(field_frame)
            entry.pack(fill="x", pady=(5, 0))
            entry.insert(0, default_value)
            
            self.entries[label_text] = entry
        
        # Campo de rol con ComboBox
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(fill="x", pady=10)
        
        role_label = ctk.CTkLabel(role_frame, text="Rol:")
        role_label.pack(anchor="w")
        
        self.role_combobox = ctk.CTkComboBox(
            role_frame,
            values=self.roles,
            state="readonly"
        )
        self.role_combobox.pack(fill="x", pady=(5, 0))
        
        # Establecer el valor actual del rol
        if self.user_data[2] in self.roles:
            self.role_combobox.set(self.user_data[2])
        else:
            self.role_combobox.set(self.roles[0])
        
        # Botones
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # Botón cancelar
        ctk.CTkButton(
            button_frame, 
            text="Cancelar", 
            command=self.destroy,
            fg_color="gray"
        ).pack(side="left", padx=5, expand=True)
        
        # Botón guardar
        ctk.CTkButton(
            button_frame, 
            text="Guardar", 
            command=self.save_changes
        ).pack(side="left", padx=5, expand=True)
        
    def save_changes(self):
        # Recopilar datos actualizados
        nombre = self.entries["Nombre:"].get().strip()
        email = self.entries["Email:"].get().strip()
        rol = self.role_combobox.get()
        
        # Validar campos
        if not nombre or not email:
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return
        
        # Validar formato de email básico
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Por favor ingrese un email válido")
            return
        
        # Crear datos actualizados
        updated_data = [nombre, email, rol]
        
        # Llamar al callback con los datos actualizados
        self.on_save(updated_data)
        self.destroy()

class AdminDashboard(ctk.CTk):
    def __init__(self, user_data=None):
        super().__init__()
        # Configuración inicial
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Almacena los datos de los usuarios
        self.user_data = user_data if user_data else {}
        self.users_data = [
            ("Juan Pérez", "juan@example.com", "Admin"),
            ("María García", "maria@example.com", "Doctor")
        ]

        # Ventana principal
        self.title("Panel de Administrador")
        self.geometry("1200x700")

        self.active_frame = None
        self.current_tab = "users"

        self.create_layout()
        
    def create_layout(self):
        # Frame principal que divide la pantalla en sidebar y contenido
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        # Sidebar
        self.create_sidebar()
        
        # Área de contenido principal
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Crear cards de métricas
        self.create_metric_cards()
        
        # Mostrar el contenido inicial (usuarios)
        self.show_users()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.main_frame, width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Título del sidebar
        user_name = f"{self.user_data.get('nombre', '')} {self.user_data.get('apellidos', '')}"
        title = ctk.CTkLabel(sidebar, text=f"Bienvenido\n{user_name}", 
                           font=("Arial", 20, "bold"), wraplength=180)
        title.pack(pady=20, padx=10)

         # Rol del usuario
        rol_text = "Administrador" if self.user_data.get('rol') == 1 else "Usuario"
        rol_label = ctk.CTkLabel(sidebar, text=rol_text, font=("Arial", 14))
        rol_label.pack(pady=(0, 20), padx=10)       

        # Botones de navegación
        buttons_data = [
            ("Usuarios", "users", self.show_users),
            ("Servicios", "services", self.show_services),
            ("Reportes", "reports", self.show_reports),
            ("Cerrar Sesión", "logout", self.quit)
        ]
        
        for text, tab, command in buttons_data:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                anchor="w",
                height=40
            )
            btn.pack(fill="x", padx=10, pady=5)
    
    def create_metric_cards(self):
        metrics_frame = ctk.CTkFrame(self.content_frame)
        metrics_frame.pack(fill="x", pady=(0, 20))
        
        # Configurar el grid con 4 columnas
        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1)
        
        metrics_data = [
            ("Total Usuarios", str(len(self.users_data))),
            ("Servicios Activos", "15"),
            ("Ingresos Mensuales", "$45,231"),
            ("Nuevos Pacientes", "+73")
        ]
        
        for i, (title, value) in enumerate(metrics_data):
            card = ctk.CTkFrame(metrics_frame)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=("Arial", 12)).pack(pady=(10, 5))
            ctk.CTkLabel(card, text=value, font=("Arial", 20, "bold")).pack(pady=(0, 10))
    
    def create_table(self, parent, headers, data):
        # Crear frame para la tabla
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear Treeview
        tree = ttk.Treeview(table_frame, columns=headers, show="headings", height=10)
        
        # Configurar encabezados
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, width=150)
        
        # Agregar datos
        for row in data:
            tree.insert("", "end", values=row)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar elementos
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return tree
    
    def edit_user(self, tree):
        # Obtener el item seleccionado
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un usuario para editar")
            return
        
        # Obtener los datos del usuario seleccionado
        user_data = tree.item(selected_item)['values']
        
        def on_save(updated_data):
            # Actualizar los datos en la tabla
            index = tree.index(selected_item)
            tree.item(selected_item, values=updated_data)
            self.users_data[index] = updated_data
            
        # Crear ventana de edición
        edit_window = EditUserWindow(self, user_data, on_save)

    def show_users(self):
        # Limpiar contenido previo
        self.clear_content()

        # Encabezados y datos de la tabla
        headers = ["Nombre", "Email", "Rol"]
        self.users_data = [
            ("Juan Pérez", "juan@example.com", "Admin"),
            ("María García", "maria@example.com", "Doctor")
        ]
        
        # Crear tabla de usuarios
        user_tree = self.create_table(self.content_frame, headers, self.users_data)
        user_tree.pack(fill="both", expand=True)

        # Botón para editar usuario
        edit_button = ctk.CTkButton(
            self.content_frame,
            text="Editar Usuario",
            command=lambda: self.edit_user(user_tree)
        )
        edit_button.pack(pady=10)

    def show_services(self):
        # Implementar lógica para mostrar servicios
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Servicios").pack(pady=20)

    def show_reports(self):
        # Implementar lógica para mostrar reportes
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Reportes").pack(pady=20)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
