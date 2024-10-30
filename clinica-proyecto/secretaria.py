import customtkinter as ctk
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from db_connection import conexion_db

class SecretaryPanel(ctk.CTk):
    def __init__(self, user_data=None):
        super().__init__()  # Llamada al constructor de la clase base
        


        self.user_data = user_data
        self.title("Panel de Secretaria")  # Configura la ventana actual en lugar de self.root
        self.geometry("1200x700")
        
        # Set the color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create the main layout
        self.create_layout()


        
    def create_layout(self):
        # Create sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)  # Usa 'self' en lugar de 'self.root'
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Title in sidebar
        title = ctk.CTkLabel(self.sidebar, text="Panel de Secretaria", 
                             font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Navigation buttons
        self.create_nav_buttons()
        
        # Main content area
        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Initially show appointments page
        self.show_appointments()
        
    def create_nav_buttons(self):
        # Appointments button
        self.appointments_btn = ctk.CTkButton(
            self.sidebar, text="Citas",
            command=self.show_appointments
        )
        self.appointments_btn.pack(pady=10, padx=20, fill="x")
        
        # Patients button
        self.patients_btn = ctk.CTkButton(
            self.sidebar, text="Pacientes",
            command=self.show_patients
        )
        self.patients_btn.pack(pady=10, padx=20, fill="x")
        
        # Billing button
        self.billing_btn = ctk.CTkButton(
            self.sidebar, text="Facturación",
            command=self.show_billing
        )
        self.billing_btn.pack(pady=10, padx=20, fill="x")
        
        # Logout button at bottom
        self.logout_btn = ctk.CTkButton(
            self.sidebar, text="Cerrar Sesión",
            command=self.quit
        )
        self.logout_btn.pack(side="bottom", pady=20, padx=20, fill="x")
        
    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
    def show_appointments(self):
        self.clear_main_content()
        
        # Title
        title = ctk.CTkLabel(self.main_content, text="Citas",
                             font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=10)
        
        # Calendar frame
        calendar_frame = ctk.CTkFrame(self.main_content)
        calendar_frame.pack(pady=10, fill="x")
        
        # Calendar
        cal = Calendar(calendar_frame, selectmode='day',
                       year=datetime.now().year,
                       month=datetime.now().month,
                       day=datetime.now().day)
        cal.pack(pady=10)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.main_content)
        nav_frame.pack(pady=10, fill="x")
        
        ctk.CTkButton(nav_frame, text="Semana Anterior").pack(side="left", padx=5)
        ctk.CTkButton(nav_frame, text="Semana Siguiente").pack(side="left", padx=5)
        ctk.CTkButton(nav_frame, text="Agendar Cita").pack(side="left", padx=5)
        
        # Appointments table
        table_frame = ctk.CTkFrame(self.main_content)
        table_frame.pack(pady=10, fill="both", expand=True)
        
        # Create Treeview for appointments
        columns = ('Fecha', 'Hora', 'Paciente', 'Estado')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        # Add sample data
        sample_data = [
            ('2023-05-01', '09:00', 'Juan Pérez', 'Confirmado'),
            ('2023-05-02', '10:30', 'María García', 'Pendiente'),
            ('2023-05-03', '14:00', 'Carlos Rodríguez', 'Confirmado'),
        ]
        
        for item in sample_data:
            tree.insert('', tk.END, values=item)
            
        tree.pack(fill="both", expand=True)

    def fetch_doctors(self):
        conn = conexion_db()
        cursor = conn.cursor()

        cursor.execute("SELECT CONCAT(Nombre, ' ', Apellidos) AS NombreCompleto, ID_Usuario FROM Usuario WHERE Rol = 2")
        doctors = cursor.fetchall()
        conn.close()
        return doctors

        
    def show_patients(self):
        self.clear_main_content()
        
        # Title
        title = ctk.CTkLabel(self.main_content, text="Pacientes",
                             font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=10)
        
        # Search frame
        search_frame = ctk.CTkFrame(self.main_content)
        search_frame.pack(pady=10, fill="x")
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar pacientes...")
        search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        search_btn = ctk.CTkButton(search_frame, text="Buscar")
        search_btn.pack(side="left", padx=5)
        
        # Patients table
        table_frame = ctk.CTkFrame(self.main_content)
        table_frame.pack(pady=10, fill="both", expand=True)
        
        columns = ('Nombre', 'Email', 'Teléfono', 'Acciones')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        sample_data = [
            ('Juan Pérez', 'juan@example.com', '+1234567890', 'Ver'),
            ('María García', 'maria@example.com', '+0987654321', 'Ver'),
        ]
        
        for item in sample_data:
            tree.insert('', tk.END, values=item)
            
        tree.pack(fill="both", expand=True)
        
        # Add patient button
        add_btn = ctk.CTkButton(self.main_content, text="Agregar Nuevo Paciente", command=self.open_add_patient_window)
        add_btn.pack(pady=10)
    
    def open_add_patient_window(self):
        # Crear una nueva ventana
        doctors = self.fetch_doctors()
        doctor_names = [doctor[0] for doctor in doctors]
        doctor_id = [doctor[1] for doctor in doctors]
        self.add_patient_window = ctk.CTkToplevel(self)
        self.add_patient_window.title("Agregar Nuevo Paciente")
        self.add_patient_window.geometry("400x700")
        
        # Título en la nueva ventana
        title = ctk.CTkLabel(self.add_patient_window, text="Agregar Nuevo Paciente", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=10)
        
        # Formulario de entrada
        form_frame = ctk.CTkFrame(self.add_patient_window)
        form_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Nombre del paciente
        ctk.CTkLabel(form_frame, text="Nombre del Paciente").pack(pady=5)
        patient_name_entry = ctk.CTkEntry(form_frame)
        patient_name_entry.pack(fill="x", padx=10)

        # Apellido del paciente
        ctk.CTkLabel(form_frame, text="Apellido del Paciente").pack(pady=5)
        patient_last_name_entry = ctk.CTkEntry(form_frame)
        patient_last_name_entry.pack(fill="x", padx=10)

        # Email del paciente
        ctk.CTkLabel(form_frame, text="Correo Electrónico").pack(pady=5)
        patient_email_entry = ctk.CTkEntry(form_frame)
        patient_email_entry.pack(fill="x", padx=10)
        
        # Teléfono del paciente
        ctk.CTkLabel(form_frame, text="Teléfono").pack(pady=5)
        patient_phone_entry = ctk.CTkEntry(form_frame)
        patient_phone_entry.pack(fill="x", padx=10)

        #Dirección del paciente
        ctk.CTkLabel(form_frame, text="Dirección").pack(pady=5)
        patient_address_entry = ctk.CTkEntry(form_frame)
        patient_address_entry.pack(fill="x", padx=10)

        # Fecha de Nacimiento
        ctk.CTkLabel(form_frame, text="Fecha de Nacimiento (YYYY-MM-DD)").pack(pady=5)
        patient_birth_entry = ctk.CTkEntry(form_frame)
        patient_birth_entry.pack(fill="x", padx=10)

        # Número Social
        ctk.CTkLabel(form_frame, text="Número Social").pack(pady=5)
        patient_social_entry = ctk.CTkEntry(form_frame)
        patient_social_entry.pack(fill="x", padx=10)

        # Obtener doctores de la base de datos

        
        # Doctor asignado
        ctk.CTkLabel(form_frame, text="Asignar Doctor").pack(pady=5)
        # Función para obtener el ID del doctor seleccionado
        def get_doctor_id(selected_doctor_name):
            index = doctor_names.index(selected_doctor_name)
            return doctor_id[index]  # Devuelve el ID correspondiente
        # Crear el menú de selección de doctores
        doctor_selection = ctk.CTkOptionMenu(form_frame, values=doctor_names, command=lambda name: get_doctor_id(name))
        doctor_selection.pack(fill="x", padx=10)


        # Botón para guardar el paciente
        save_btn = ctk.CTkButton(form_frame, text="Guardar Paciente", command=lambda: self.save_patient(
            patient_name_entry.get(),
            patient_last_name_entry.get(),
            patient_email_entry.get(),
            patient_phone_entry.get(),
            patient_address_entry.get(),
            get_doctor_id(doctor_selection.get()),
            patient_birth_entry.get(),
            patient_social_entry.get()
        ))
        save_btn.pack(pady=20)
    
    def update_doctor_id(self, selected_name):
        doctors = self.fetch_doctors()
        for doctor in doctors:
            if doctor[0] == selected_name:  # Compara con el nombre completo
                self.selected_doctor_id.set(doctor[1])  # Establece el ID del doctor
                break


    def get_selected_doctor(self, selected_name, doctors):
        for doctor in doctors:
            if doctor[1] == selected_name:
                return doctor[0]
        return None

    def save_patient(self, name, last_name, email, phone, address, doctor_id, birth_date, social_number):
        # Establecer conexión a la base de datos
        conn = conexion_db()
        cursor = conn.cursor()
        
        # Insertar nuevo paciente en la base de datos
        try:
            cursor.execute("""
                INSERT INTO paciente (Nombre, Apellidos, Correo, Telefono, Direccion, ID_Medico, Fecha_Nacimiento, Numero_Social)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, last_name, email, phone, address, doctor_id, birth_date, social_number))
            
            # Confirmar la transacción
            conn.commit()
            print(f"Paciente guardado: {name} {last_name}, Doctor Asignado: {doctor_id}")
            
        except Exception as e:
            print(f"Error al guardar paciente: {e}")  # Manejo de errores
            conn.rollback()  # Revertir en caso de error

        finally:
            # Cerrar la conexión
            conn.close()
        
        # Cerrar ventana después de guardar
        self.add_patient_window.destroy()

    def show_billing(self):
        self.clear_main_content()
        
        # Title
        title = ctk.CTkLabel(self.main_content, text="Facturación",
                             font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=10)
        
        # Tabs
        tabview = ctk.CTkTabview(self.main_content)
        tabview.pack(fill="both", expand=True)
        
        # Create tabs
        tab_create = tabview.add("Crear Factura")
        tab_history = tabview.add("Historial de Facturas")
        
        # Create Invoice Form
        form_frame = ctk.CTkFrame(tab_create)
        form_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Form fields
        ctk.CTkLabel(form_frame, text="Paciente").pack(pady=5)
        ctk.CTkEntry(form_frame, placeholder_text="Seleccionar paciente").pack(fill="x", padx=10)
        
        ctk.CTkLabel(form_frame, text="Servicio").pack(pady=5)
        ctk.CTkEntry(form_frame, placeholder_text="Seleccionar servicio").pack(fill="x", padx=10)
        
        ctk.CTkLabel(form_frame, text="Monto").pack(pady=5)
        ctk.CTkEntry(form_frame, placeholder_text="0.00").pack(fill="x", padx=10)
        
        ctk.CTkLabel(form_frame, text="Fecha").pack(pady=5)
        ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD").pack(fill="x", padx=10)
        
        ctk.CTkButton(form_frame, text="Crear Factura").pack(pady=20)
        
        # Invoice History Table
        columns = ('Número', 'Fecha', 'Paciente', 'Monto', 'Estado')
        tree = ttk.Treeview(tab_history, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        sample_data = [
            ('001', '2023-05-01', 'Juan Pérez', '$100.00', 'Pagada'),
            ('002', '2023-05-02', 'María García', '$150.00', 'Pendiente'),
        ]
        
        for item in sample_data:
            tree.insert('', tk.END, values=item)
            
        tree.pack(fill="both", expand=True)

# Para ejecutar la aplicación
if __name__ == "__main__":
    app = SecretaryPanel()
    app.mainloop()
