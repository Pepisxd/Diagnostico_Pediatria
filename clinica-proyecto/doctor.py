import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime
import locale

# Configurar el tema y el modo por defecto
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DoctorScreen(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuración básica de la ventana
        self.title("Sistema de Gestión Médica")
        self.geometry("1200x700")
        
        # Variables de estado
        self.current_page = ctk.StringVar(value="appointments")
        
        # Crear el diseño principal
        self.create_layout()
        
        # Mostrar la página inicial
        self.show_page()
        
    def create_layout(self):
        # Frame lateral (sidebar)
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Título del sidebar
        ctk.CTkLabel(
            self.sidebar,
            text="Panel de Médico",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 30))
        
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
            
        ctk.CTkLabel(
            self.main_frame,
            text="Pacientes",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            self.main_frame,
            text="Esta es la página de gestión de pacientes.",
            font=ctk.CTkFont(size=16)
        ).pack()
        
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
    app = DoctorScreen()
    app.mainloop()
