import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime
import locale
from db_connection import conexion_db
# Configurar el tema y el modo por defecto
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DoctorScreen(ctk.CTk):
    def __init__(self, doctor_email, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print(f"Email del médico: {doctor_email}")

        self.conn = self.conexion_db()
        if not self.conn:
            raise ConnectionError("No se pudo establecer conexión con la base de datos")
        
        self.cursor = self.conn.cursor()
        

        
    
        self.doctor_id = self.get_doctor_id(doctor_email)
        print(f"ID del médico: {self.doctor_id}")
        # Configuración básica de la ventana
        self.title("Sistema de Gestión Médica")
        self.geometry("1200x700")


        # Variables de estado
        self.current_page = ctk.StringVar(value="appointments")
        
        # Crear el diseño principal
        self.create_layout()
        
        # Mostrar la página inicial
        self.show_page()

        # Asegurarse de cerrar la conexión al cerrar la aplicación
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def conexion_db(self):
        try:
            return conexion_db()
        except Exception as e:
            print(f"Error al conectar con la base de datos: {str(e)}")
            return None

    def on_closing(self):
        try:
            if hasattr(self, 'conn') and self.conn:
                # Hacer commit de cualquier transacción pendiente
                self.conn.commit()
                
                if hasattr(self, 'cursor') and self.cursor:
                    self.cursor.close()
                self.conn.close()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
        finally:
            self.destroy()

    def get_doctor_id(self, email):
        if not email:
            raise ValueError("Email no proporcionado")
            
        query = """
            SELECT ID_Usuario FROM Usuario
            WHERE Correo = %s AND Rol = 2
        """
        try:
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError(f"No se encontró el médico con email: {email}")
        except Exception as e:
            raise ValueError(f"Error en la consulta: {str(e)}")
    
        
    def get_doctor_name(self):
        query = "SELECT Nombre, Apellidos FROM Usuario WHERE ID_Usuario = %s"
        self.cursor.execute(query, (self.doctor_id,))
        result = self.cursor.fetchone()
        if result:
            return f"Dr. {result[0]} {result[1]}"
        return "Doctor"



        
    def create_layout(self):
        # Frame lateral (sidebar)
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        doctor_name = self.get_doctor_name()
        ctk.CTkLabel(
            self.sidebar,
            text=doctor_name,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 10))

        
        # Título del sidebar
        ctk.CTkLabel(
            self.sidebar,
            text="Panel de Médico",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 30))
        
        # Botones de navegación
        self.nav_buttons = {}
        for page in [("appointments", "Mis Citas"), 
                    ("patients", "Pacientes"), 
                    ("diagnosis", "Diagnóstico")]:
            self.nav_buttons[page[0]] = ctk.CTkButton(
                self.sidebar,
                text=page[1],
                command=lambda p=page[0]: self.change_page(p),
                width=180
            )
            self.nav_buttons[page[0]].pack(pady=5)
            
        # Botón de cerrar sesión
        ctk.CTkButton(
            self.sidebar,
            text="Cerrar Sesión",
            command=self.quit,
            width=180
        ).pack(side="bottom", pady=20)
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
    def create_appointments_page(self):
        # Limpiar el frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Título
        ctk.CTkLabel(
            self.main_frame,
            text="Mis Citas",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 10))
        
        # Calendario
        cal_frame = ctk.CTkFrame(self.main_frame)
        cal_frame.pack(pady=10, padx=20)
        
        cal = Calendar(
            cal_frame,
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            showweeknumbers=False
        )
        cal.pack(pady=10)
        
        # Botones de navegación
        nav_frame = ctk.CTkFrame(self.main_frame)
        nav_frame.pack(pady=10)
        
        ctk.CTkButton(
            nav_frame,
            text="Semana Anterior",
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            nav_frame,
            text="Semana Siguiente",
        ).pack(side="left", padx=5)
        
        # Tabla de citas
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Encabezado de la tabla
        headers = ["Fecha", "Hora", "Paciente", "Estado"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                table_frame,
                text=header,
                font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=col, padx=10, pady=5, sticky="w")
            
        # Datos de ejemplo
        appointments = [
            ("2023-05-01", "09:00", "Paciente 1", "Confirmado"),
            ("2023-05-02", "10:30", "Paciente 2", "Pendiente"),
            ("2023-05-03", "14:00", "Paciente 3", "Confirmado"),
            ("2023-05-04", "11:00", "Paciente 4", "Cancelado"),
            ("2023-05-05", "16:30", "Paciente 5", "Confirmado")
        ]
        
        for row, appointment in enumerate(appointments, start=1):
            for col, value in enumerate(appointment):
                ctk.CTkLabel(
                    table_frame,
                    text=value
                ).grid(row=row, column=col, padx=10, pady=5, sticky="w")
                
    def create_patients_page(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
                
        # Título
        ctk.CTkLabel(
            self.main_frame,
            text="Gestión de Pacientes",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20,10))

        # Frame superior para búsqueda y botón de nuevo paciente
        top_frame = ctk.CTkFrame(self.main_frame)
        top_frame.pack(fill="x", padx=20, pady=10)

        # Barra de búsqueda
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            top_frame, 
            placeholder_text="Buscar paciente...",
            width=300,
            textvariable=search_var
        )
        search_entry.pack(side="left", padx=(0,10))

        # Botón de búsqueda
        ctk.CTkButton(
            top_frame,
            text="Buscar",
            width=100,
            command=lambda: self.search_patients(search_var.get())
        ).pack(side="left", padx=5)

        # Botón de nuevo paciente
        ctk.CTkButton(
            top_frame,
            text="Nuevo Paciente",
            width=150,
            command=self.show_patient_form
        ).pack(side="right", padx=5)

        # Frame para la lista de pacientes
        list_frame = ctk.CTkFrame(self.main_frame)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Cabeceras de la tabla
        headers = ["Nombre", "Apellidos", "Fecha Nacimiento", "Teléfono", "Acciones"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                list_frame,
                text=header,
                font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        # Ejemplo de cómo mostrar los pacientes (esto se conectará con la base de datos)
        self.display_patients(list_frame)



    def display_patients(self, list_frame):
        # Aquí iría la consulta a la base de datos
        # Por ahora usamos datos de ejemplo
        pacientes = self.get_doctor_patients()  # Esta función obtendría los pacientes de la BD

        for row, paciente in enumerate(pacientes, start=1):
            ctk.CTkLabel(
                list_frame,
                text=paciente[1]  # Nombre
            ).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            ctk.CTkLabel(
                list_frame,
                text=paciente[2]  # Apellidos
            ).grid(row=row, column=1, padx=10, pady=5, sticky="w")
            
            ctk.CTkLabel(
                list_frame,
                text=paciente[3]  # Fecha Nacimiento
            ).grid(row=row, column=2, padx=10, pady=5, sticky="w")
            
            ctk.CTkLabel(
                list_frame,
                text=paciente[6]  # Teléfono
            ).grid(row=row, column=3, padx=10, pady=5, sticky="w")

            actions_frame = ctk.CTkFrame(list_frame)
            actions_frame.grid(row=row, column=4, padx=10, pady=5)

            ctk.CTkButton(
                actions_frame,
                text="Editar",
                width=70,
                command=lambda p=paciente: self.edit_patient(p)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                actions_frame,
                text="Eliminar",
                width=70,
                fg_color="red",
                command=lambda p=paciente: self.delete_patient(p[0])
            ).pack(side="left", padx=2)

    def show_patient_form(self, patient=None):
        # Crear una nueva ventana para el formulario
        form_window = ctk.CTkToplevel(self)
        form_window.title("Nuevo Paciente" if patient is None else "Editar Paciente")
        form_window.geometry("500x800")

        # Debugging: Imprimir los datos del paciente si existe
        print(f"Datos del paciente recibidos en form: {patient}")

        # Variables para los campos del formulario con valores por defecto vacíos
        nombre_var = ctk.StringVar(value=patient[1] if patient else "")
        apellidos_var = ctk.StringVar(value=patient[2] if patient else "")
        fecha_var = ctk.StringVar(value=patient[3] if patient else "")
        direccion_var = ctk.StringVar(value=patient[4] if patient else "")
        correo_var = ctk.StringVar(value=patient[5] if patient else "")
        telefono_var = ctk.StringVar(value=patient[6] if patient else "")
        nss_var = ctk.StringVar(value=patient[7] if patient else "")

        # Crear los campos del formulario
        fields = [
            ("Nombre:", nombre_var),
            ("Apellidos:", apellidos_var),
            ("Fecha Nacimiento (YYYY-MM-DD):", fecha_var),
            ("Dirección:", direccion_var),
            ("Correo:", correo_var),
            ("Teléfono:", telefono_var),
            ("Número Social:", nss_var)
        ]

        for i, (label, var) in enumerate(fields):
            ctk.CTkLabel(
                form_window,
                text=label
            ).pack(padx=20, pady=(20 if i == 0 else 5))

            entry = ctk.CTkEntry(
                form_window,
                textvariable=var,
                width=300
            )
            entry.pack(padx=20, pady=5)
            
            # Debugging: Imprimir el valor inicial de cada campo
            print(f"Valor inicial de {label}: {var.get()}")

        # Botones de acción
        buttons_frame = ctk.CTkFrame(form_window)
        buttons_frame.pack(pady=20)

        def on_save():
            # Debugging: Imprimir valores antes de guardar
            data = {
                'nombre': nombre_var.get(),
                'apellidos': apellidos_var.get(),
                'fecha_nacimiento': fecha_var.get(),
                'direccion': direccion_var.get(),
                'correo': correo_var.get(),
                'telefono': telefono_var.get(),
                'numero_social': nss_var.get()
            }
            print("Datos a guardar:", data)
            
            # Validar que los campos no estén vacíos
            if not all(data.values()):
                self.show_error("Todos los campos son obligatorios")
                return
                
            # Validar formato de fecha
            try:
                datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d')
            except ValueError:
                self.show_error("Formato de fecha inválido. Use YYYY-MM-DD")
                return

            self.save_patient(
                patient[0] if patient else None,
                data,
                form_window
            )

        ctk.CTkButton(
            buttons_frame,
            text="Guardar",
            command=on_save
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=form_window.destroy
        ).pack(side="left", padx=5)

    def get_doctor_patients(self):
        query = "SELECT * FROM Paciente WHERE ID_Medico = %s"
        print(f"Buscando pacientes para el doctor ID: {self.doctor_id}")  
        self.cursor.execute(query, (self.doctor_id,))  # ID del médico actual
        patients = self.cursor.fetchall()
        print(f"Pacientes encontrados: {len(patients)}")
        return patients

    def save_patient(self, patient_id, data, form_window):
            try:
                # Debugging: Imprimir datos recibidos
                print("=== Debug save_patient ===")
                print(f"Patient ID: {patient_id}")
                print(f"Doctor ID: {self.doctor_id}")
                print(f"Data recibida: {data}")

                if not all(data.values()):
                    raise ValueError("Todos los campos son obligatorios")

                if patient_id is None:
                    # Nuevo paciente
                    query = """
                        INSERT INTO Paciente 
                        (Nombre, Apellidos, Fecha_Nacimiento, Direccion, Correo, Telefono, Numero_Social, ID_Medico)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        data['nombre'],
                        data['apellidos'],
                        data['fecha_nacimiento'],
                        data['direccion'],
                        data['correo'],
                        data['telefono'],
                        data['numero_social'],
                        self.doctor_id
                    )
                    print("Ejecutando INSERT con valores:", values)
                else:
                    # Actualizar paciente existente
                    query = """
                        UPDATE Paciente
                        SET Nombre = %s, Apellidos = %s, Fecha_Nacimiento = %s, 
                            Direccion = %s, Correo = %s, Telefono = %s, 
                            Numero_Social = %s, ID_Medico = %s
                        WHERE ID_Paciente = %s
                    """
                    values = (
                        data['nombre'],
                        data['apellidos'],
                        data['fecha_nacimiento'],
                        data['direccion'],
                        data['correo'],
                        data['telefono'],
                        data['numero_social'],
                        self.doctor_id,
                        patient_id
                    )
                    print("Ejecutando UPDATE con valores:", values)

                self.cursor.execute(query, values)
                self.conn.commit()
                print("Operación exitosa")
                form_window.destroy()
                self.create_patients_page()

            except Exception as e:
                print(f"Error al guardar paciente: {e}")
                self.show_error(f"Error al guardar: {str(e)}")

    def edit_patient(self, patient):
        self.show_patient_form(patient)

    def delete_patient(self, patient_id):
        query = "DELETE FROM Paciente WHERE ID_Paciente = %s"
        try:
            self.cursor.execute(query, (patient_id,))
            self.conn.commit()
            print("Paciente eliminado:", patient_id)
            self.create_patients_page()  # Actualizar la lista
        except Exception as e:
            print(f"Error al eliminar paciente: {e}")
            self.show_error(f"Error al eliminar paciente: {e}")


    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x150")
        
        ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=250
        ).pack(pady=20)
        
        ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        ).pack(pady=10)
    
    def search_patients(self, query):
        search_query = """
            SELECT * FROM Paciente
            WHERE Nombre LIKE %s OR Apellidos LIKE %s OR Telefono LIKE %s
        """
        like_query = f"%{query}%"
        self.cursor.execute(search_query, (like_query, like_query, like_query))
        results = self.cursor.fetchall()
        print("Resultados de la búsqueda:", results)
        self.create_patients_page(results)  
            
    def create_diagnosis_page(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(
            self.main_frame,
            text="Diagnóstico",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            self.main_frame,
            text="Esta es la página de diagnóstico médico.",
            font=ctk.CTkFont(size=16)
        ).pack()
        
    def change_page(self, page):
        self.current_page.set(page)
        self.show_page()
        
    def show_page(self):
        # Actualizar el estilo de los botones
        for page, button in self.nav_buttons.items():
            if page == self.current_page.get():
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color=("gray70", "gray30"))
        
        # Mostrar la página correspondiente
        if self.current_page.get() == "appointments":
            self.create_appointments_page()
        elif self.current_page.get() == "patients":
            self.create_patients_page()
        elif self.current_page.get() == "diagnosis":
            self.create_diagnosis_page()

if __name__ == "__main__":
    app = DoctorScreen(doctor_email="juan.pediatra@hospital.com")
    app.mainloop()
