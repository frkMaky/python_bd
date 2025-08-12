### Impotaciones
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tkinter as tk
import os
from PIL import Image 
import bd.base_datos as sqlbd

# Configuraciones globales

#-->Rutas
# Carpeta Principal
carpeta_principal = os.path.dirname(__file__) # c:\apache\htdocs\python_master\proyecto-bd\interfaz
# Carpeta Imagenes
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes") # c:\apache\htdocs\python_master\proyecto-bd\interfaz\imagenes

# Objeto para manejar base de datos SQL
base_datos = sqlbd.BaseDatos(**sqlbd.acceso_bd)

# Modo de color y tema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# Fuentes del Programa
fuente_widget = ('Raleway',16, tk.font.BOLD)


class Login:
    """ Ventana de logueo del programa """
    def __init__(self):
        # Creacion de la ventana principal 
        self.root = ctk.CTk()
        self.root.title("Bases de Datos - Login")
        self.root.iconbitmap(os.path.join(carpeta_imagenes,"logo.ico"))
        self.root.geometry("450x650")
        self.root.resizable(False, False)

        # Contenido de la ventana principal
        # Logo
        logo = ctk.CTkImage(
            light_image = Image.open((os.path.join(carpeta_imagenes,"logo_claro.png"))),
            dark_image  = Image.open((os.path.join(carpeta_imagenes,"logo_oscuro.png"))),
            size=(250,250)
        )
        # Etiqueta para mostrar la imagen
        etiqueta = ctk.CTkLabel(master = self.root, image=logo , text="")
        etiqueta.pack(pady = 15)

        # Campos de Texto
        # Usuario
        ctk.CTkLabel(master = self.root,text="Usuario: ").pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.insert(0, "Usuario")
        self.usuario.bind("<Button-1>",lambda e:self.usuario.delete(0,'end'))
        self.usuario.pack()

        # Contraseña
        ctk.CTkLabel(self.root,text="Password: ").pack()
        self.contrasenha = ctk.CTkEntry(self.root)
        self.contrasenha.insert(0, "*******")
        self.contrasenha.bind("<Button-1>",lambda e:self.contrasenha.delete(0,'end'))
        self.contrasenha.pack()

        # Boton de envío
        ctk.CTkButton(self.root, text="Entrar", command=self.validar).pack(pady=10)

        # Bucle de ejecucion
        self.root.mainloop()

    def validar(self):
        """ Validar el Login """
        obtener_usuario = self.usuario.get()
        obtener_contrasenha = self.contrasenha.get()

        if obtener_usuario != sqlbd.acceso_bd['user'] or obtener_contrasenha != sqlbd.acceso_bd['password']:
            # En caso de tener ya un elemento  "info_login" (etiqueta) creado, lo borra
            if hasattr(self, 'info_login'):
                self.info_login.configure(text=f"Usuario o contraseña incorrectos.")
            else:
                # Se crea y muestra elemento info_login
                self.info_login = ctk.CTkLabel(master=self.root, text="Usuario o contraseña incorrectos.")
                self.info_login.pack()
        else:
            # En caso de tener ya un elemento  "info_login" (etiqueta) creado, lo borra
            if hasattr(self, 'info_login'):
                self.info_login.configure(text=f"Hola {obtener_usuario}, Espera unos instantes...")
            else:
                # Se crea y muestra elemento info_login
                self.info_login = ctk.CTkLabel(master=self.root, text=f"Hola {obtener_usuario}, Espera unos instantes...")
                self.info_login.pack()
            # Destruir ventana login
            self.root.destroy()

            # Se instancia ventana de opciones del programa
            ventana_opciones = VentanaOpciones()

class FuncionesPrograma:
    """ Ventanas TopLevel con cada OPCION para gestionar la BBDD"""

    def ventana_consultas(self):
        """ Ventana para realizar consultas SQL"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana de consultas SQL")
        ventana.grab_set() # Obtener el foco

        # Crea el frame y añadelo a la ventana
        marco = ctk.CTkFrame(ventana)
        marco.pack(padx=10,pady=10)

        # Crea el Entry y establece su tamaño a 300px de ancho
        self.entrada = ctk.CTkEntry(marco,width=300)
        # Establece fuente personalizada
        self.entrada.configure(font=fuente_widget)
        # Posiciona el elemento en el grid
        self.entrada.grid(row=0, column=0, pady=10)

        # método para consulta_sql de bases_datos.py
        def procesar_datos():
            try:
                # Borrar el contenido  de la caja de resultado
                self.texto.delete('1.0','end')
                # Obtiene el contenido del entry
                datos = self.entrada.get()
                # LLama al metodo  bases_datos.consulta() con los datos del argumento
                resultado = base_datos.consulta(datos)
                for registro in resultado:
                    self.texto.insert('end', registro)
                    self.texto.insert('end', '\n')
                # Actualiza el contador de registro devueltos
                n_registros = len(resultado)
                self.contador_registros.configure(text=f"Registros devueltos: {n_registros}")
            except Exception:
                self.contador_registros.configure(text=f"Hay un error en tu consulta SLQ. Por favor, revísela.")
                CTkMessagebox(title="ERROR",message="¡Hay un error en tu consulta SQL! Por favor, revísela", icon="cancel")

        # Crea el boton de envio
        boton_envio = ctk.CTkButton(
            master=marco,
            text="Enviar",
            command=lambda : procesar_datos()
        )
        # Posiciona el boton  a la derecha del Entry()
        boton_envio.grid(row=0,column=1)

        # Crea el boton de borrado
        boton_borrado = ctk.CTkButton(
            master=marco,
            text="Borrar",
            command=self.limpiar_texto
        )
        # Posiciona el boton a la derecha del boton envío
        boton_borrado.grid(row=0, column=2)

        # Crea el widget  de texto
        self.texto = ctk.CTkTextbox(master=marco, width=600,height=300)
        # Coloca el widget debajo del Entry y el boton
        self.texto.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    
        # Agrega widget Label para mostrar el número de registro devueltos
        self.contador_registros = ctk.CTkLabel(master=marco, text="Esperando una instrucción")
        self.contador_registros.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def limpiar_texto(self):
        """ Limpia el contenido del textbox"""
        self.texto.delete('1.0','end')

    def ventana_mostrar_bases_datos(self):
        """ Ventana para mostrar las Bases de Datos"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar las bases de datos del servidor.")
        ventana.geometry("400x565")
        ventana.resizable(0,0)
        ventana.grab_set() # coge el foco

        # Se crea el marco
        marco = ctk.CTkFrame(master=ventana)
        marco.pack(padx=10,pady=10)

        # Se crea etiqueta informativa para la ventana
        ctk.CTkLabel(master=marco, text="Listado de las bases de datos del servidor.", font=fuente_widget).pack(padx=10, pady=10)

       # Agrega una entrada para la busqueda
        self.busqueda_control = tk.StringVar()

        # Se crea la entrada de texto para busquedas
        ctk.CTkEntry(master=marco, font=fuente_widget, textvariable=self.busqueda_control, width=300).pack(padx=10)

        # Caja de resultados
        self.texto = ctk.CTkTextbox(master=marco, font=fuente_widget, width=300, height=300)
        self.texto.pack(padx=10, pady=10)
        # Etiqueta para el numero de resultados
        self.resultados_label = ctk.CTkLabel(master=marco, text="", font=fuente_widget)
        self.resultados_label.pack(pady=10)

        # Funcion interna de actualizacion SHOW DATATABLES
        def actualizar():
            self.busqueda_control.set('') # Se establece el valor de la variable de control a string vacio
            self.texto.delete('1.0','end')  # Se vacia caja de resultados
            # Se llama a mostrar_bd() y se guarda resultados
            resultado = base_datos.mostrar_bd()
            # Se itera el resultado y agrega a la caja de resultados
            for bd in resultado:
                self.texto.insert('end',text=f"-{bd[0]}\n")
            # Se actualiza el numero de resultados encontrados
            numero_resultados = len(resultado)
            self.resultados_label.configure(text=f"Resultados encontrados: {numero_resultados}")
        
        # Funcion interna para buscar bd concreta
        def buscar():
            self.texto.delete('1.0','end')  # Se vacia caja de resultados
            # Se llama a mostrar_bd() y se guarda resultados
            resultado = base_datos.mostrar_bd()
            # Se obtiene el valor string de la variable de control Entry
            busqueda = self.busqueda_control.get().lower() # Se pasa a minusculas para evitar case sensitive
            # Se crea una lista vacia para almacenar los resultados filtrados
            resultado_filtrado =[]
            # Se itera tupla fetchall
            for bd in resultado:
                # Se comprueba si contiene cadena buscada y añade a lista filtrada
                if busqueda in bd[0]:
                    resultado_filtrado.append(bd)
            # Se incluye la lista filtrada en la caja de resultados
            for bd in resultado_filtrado:
                self.texto.insert('end', f"-{bd[0]}\n")
            # Se actualiza el numero de resultados encontrados
            numero_resultados = len(resultado_filtrado)
            self.resultados_label.configure(text=f"Resultados encontrados: {numero_resultados}")
        
        # Botones 
        self.boton_buscar = ctk.CTkButton(marco,text="Buscar", command=buscar)
        self.boton_buscar.pack(pady=10)

        self.boton_actualizar = ctk.CTkButton(marco,text="Actualizar", command=actualizar)
        self.boton_actualizar.pack(pady=10)

        actualizar()

    def ventana_eliminar_bases_datos(self):
        """ Ventana para eliminar bases de datos"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar bases de datos")

    def ventana_crear_bases_datos(self):
        """ Ventana para crear bases de datos"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear bases de datos")

    def ventana_crear_respaldos(self):
        """ Ventana para crear respaldos """
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear respaldos ")

    def ventana_crear_tablas(self):
        """ Ventana para crear tablas"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear tablas")

    def ventana_eliminar_tablas(self):
        """ Ventana para eliminar tablas"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar tablas")

    def ventana_mostrar_tablas(self):
        """ Ventana para mostrar tablas"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar tablas")

    def ventana_mostrar_columnas(self):
        """ Ventana para mostrar columnas"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar columnas")

    def ventana_insertar_registros(self):
        """ Ventana para insertar registros"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para insertar registros")

    def ventana_eliminar_registros(self):
        """ Ventana para eliminar registros"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar registros")

    def ventana_vaciar_tablas(self):
        """ Ventana para vaciar tablas"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para vaciar tablas")

    def ventana_actualizar_tablas(self):
        """ Ventana para actualizar tablas"""
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para actualizar tablas")
    
objeto_funciones = FuncionesPrograma()

class VentanaOpciones:
    """ Ventana con las diferentes opciones para manejar la BBDD"""
    # Lista de texto de los botones
    botones = {
        'Consulta SQL':objeto_funciones.ventana_consultas,
        'Mostrar Bases de Datos':objeto_funciones.ventana_mostrar_bases_datos,
        'Eliminar Bases de Datos':objeto_funciones.ventana_eliminar_bases_datos,
        'Crear Bases de Datos':objeto_funciones.ventana_crear_bases_datos,
        'Crear Respaldos':objeto_funciones.ventana_crear_respaldos,
        'Crear Tablas':objeto_funciones.ventana_crear_tablas,
        'Eliminar Tablas':objeto_funciones.ventana_eliminar_tablas,
        'Mostrar Tablas':objeto_funciones.ventana_mostrar_tablas,
        'Mostrar Columnas':objeto_funciones.ventana_mostrar_columnas,
        'Insertar Registros':objeto_funciones.ventana_insertar_registros,
        'Eliminar Registros':objeto_funciones.ventana_eliminar_registros,
        'Vaciar Tablas':objeto_funciones.ventana_vaciar_tablas,
        'Actualizar Registros':objeto_funciones.ventana_actualizar_tablas
        }
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Opciones para trabajar con bases de datos.")

        # Contador para la posición de los botones
        contador = 0
        # Nº de elementos por fila
        elementos_fila = 3

        # Crea los botones y establece su texto
        for texto_boton in self.botones:
            button = ctk.CTkButton(
                master=self.root,
                text=texto_boton,
                height=25,
                width=200,
                command=self.botones[texto_boton]
            )
            button.grid(row=contador//elementos_fila, column=contador%elementos_fila, padx= 5, pady=5)

            # Incrementa el contador
            contador +=1
        self.root.mainloop()
                        
            