import mysql.connector
import os
import subprocess
import datetime

### Conexion a BD
acceso_bd = {"host":"localhost", 
             "user":"root",
             "password":"root",
             "database":"american_riders"
             }

### Rutas 

# Raiz carpeta principal
carpeta_principal = os.path.dirname(__file__)

# Carpeta respaldo
carpeta_respaldo = os.path.join(carpeta_principal,"respaldo")

class BaseDatos:
            
    def __init__(self, **kwargs):
        """ Conecta a MySQL a través de un dict con los datos de acceso """
        self.conector = mysql.connector.connect(**kwargs)
        self.cursor = self.conector.cursor()
        self.host = kwargs["host"]
        self.user = kwargs["user"]
        self.contrasenha = kwargs["password"]
        self.conexion_cerrada = False
        print("Abierta conexión a la base de datos")

    ### Decorador para el reporte de BBDD en el servidor
    def reporte_bd(funcion_parametro):
        """ Decorador para el reporte de BBDD en el servidor"""
        def interno(self, base_datos):
            funcion_parametro(self,base_datos)
            BaseDatos.mostrar_bd(self)
        return interno

    ### Decorador para el cierre de las conexiones
    def conexion(funcion_parametro):
        def interno(self, *args, **kwargs):
            try:
                if self.conexion_cerrada:
                    self.conector = mysql.connector.connect(
                        host = self.host,
                        user = self.user,
                        password = self.contrasenha
                    )
                    self.cursor = self.conector.cursor()
                    self.conexion_cerrada = False
                    print("Abierta conexión con el servidor")
                # Se llama a funcion externa
                funcion_parametro(self, *args, **kwargs)
            except Exception as e:
                # Se informa de error en la llamada
                print("Ocurrió un error: {e}")
                raise e # propaga la excepcion
            finally:
                if self.conexion_cerrada:
                    pass
                else:
                    # Cerramos cursor y conexion
                    self.cursor.close()
                    self.conector.close()
                    self.conexion_cerrada = True
                    print("Se ha cerrado la conexión a la base de datos")
            return self.resultado
        return interno
    
    # Decorador para comprobar si existe una base de datos
    def comprueba_bd(funcion_parametro):
        def interno(self, nombre_bd, *args):
            # Verifica si la BD existe en el servidor
            sql = f"SHOw DATABASES LIKE '{nombre_bd}' "
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()
            # Si la BD no existe, muestra un mensaje de error
            if not resultado:
                print(f"La base de datos {nombre_bd} no existe.")
                return
            # Ejecuta al funcion y devuelve el resultado
            return funcion_parametro(self, nombre_bd, *args)
        return interno

    @conexion
    def consulta(self,sql):
        """ Ejecuta una consulta SQL sobre la conexion"""
        self.cursor.execute(sql)
        self.resultado = self.cursor.fetchall()
 
    @conexion
    def mostrar_bd(self):
        """ Muestra las BBDD del Servidor """
        self.cursor.execute("SHOW DATABASES")    
        self.resultado = self.cursor.fetchall()
        
    @conexion
    @reporte_bd
    @comprueba_bd
    def eliminar_bd(self, base_datos):
        """ Elimina la BBDD indicada como argumento """
        try:
            self.cursor.execute(f"DROP DATABASE {base_datos}")
            print(f"Se eliminó la base de datos '{base_datos}' correctamente.")
        except:
            print(f"Base de datos '{base_datos}' no encontrada.")

    @conexion
    @reporte_bd
    def crear_base_datos(self, base_datos):
        """ Crea la BBDD si no existe"""
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {base_datos} ")
            print(f"Se ha creado la BBDD '{base_datos}' o ya estaba creada.")
        except:
            print(f"Ha ocurrido un error al crear la BBDD '{base_datos}'")
        
    @conexion
    @comprueba_bd
    def copia_bd(self, base_datos):
        """ Realiza la copia de la base de datos indicada
            "C:/Program Files/MySQL/MySQL Workbench 8.0" --> Ruta a la instalacion de mysqldump
        """       
        # Obtiene fecha y horas actuales
        fecha_hora =  datetime.datetime.now().strftime("%A-%m-%d %H-%M-%S")

        # Realiza copia de seguridad SQL 
        with open(f'{carpeta_respaldo}/{base_datos}_{fecha_hora}.sql','w') as out:
            subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysqldump --user=root --password={self.contrasenha} --databases {base_datos}', shell=True, stdout=out)
        print("Se creo copia de seguridad de la base de datos")
    
    @conexion
    @comprueba_bd
    def crear_tabla(self, nombre_bd, nombre_tabla, columnas):
        """ Crear tabla en BD indicada"""

        try:
            # String para guardar el string con las columnas y tipos de datos
            columnas_string = ""

            # Se itera la lista que se pasa por argumento (cada diccionario)
            for columna in columnas:
                # Formamos el string con nombre, tipo y longitud
                columnas_string += f"{columna['name']} {columna['type']} ({columna['lenght']})"
                # Se es clave primaria, auto_increment o no admite valores nulos , lo añade al string
                if columna['primary_key']:
                    columnas_string += " PRIMARY KEY"
                if columna['auto_increment']:
                    columnas_string += " AUTO_INCREMENT"
                if columna['not_null']:
                    columnas_string += " NOT NULL"
                # Salto de linea despues de cada diccionario (columna)
                columnas_string += ",\n"
            # Elimina al final del string el salto de linea y la coma
            columnas_string = columnas_string[:-2]
            # Le indica que base de datos utilizar
            self.cursor.execute(f"USE {nombre_bd}")
            # Se crea la tabla juntando la instruccion SQL  con el string de columnas
            sql = f"CREATE TABLE {nombre_tabla} ({columnas_string});"
            # Se ejecuta la instruccion SLQ 
            self.cursor.execute(sql)
            # Se hace efectiva
            self.conector.commit()

            print(f"Se ha creado la tabla {nombre_tabla} en {nombre_bd}")

        except:
            print(f"No se pudo crear la tabla {nombre_tabla} en {nombre_bd}")
    
    @conexion
    @comprueba_bd
    def eliminar_tabla(self, nombre_bd, nombre_tabla):
        """ Elimina la tabla de la BD indicada """
        try:
            # Le indica que base de datos utilizar
            self.cursor.execute(f"USE {nombre_bd}")
            
            # Se ejecuta la instruccion SLQ 
            self.cursor.execute(f"DROP TABLE {nombre_tabla}")

            print(f"Se ha eliminado la tabla {nombre_tabla} de {nombre_bd}")
        except:
            print(f"No se ha podido eliminar la tabla {nombre_tabla} de {nombre_bd}")
 
    @conexion
    @comprueba_bd
    def mostrar_tablas(self, nombre_bd):
        """ Muestra las tablas de la BD indicada """
        try:
            # Le indica que base de datos utilizar
            self.cursor.execute(f"USE {nombre_bd};")
            self.cursor.execute(f"SHOW TABLES;")

            # Comprobar si hay al menos 1 resultado
            resultado = self.cursor.fetchall()

            if resultado == []:
                print(f"No hay tablas en la base de datos {nombre_bd}")
                return

            for tabla in resultado:
                print(f"- {tabla[0]}")
        except:
            print(f"No se han podido consultar las tablas de {nombre_bd}")
    
    @conexion
    @comprueba_bd
    def mostrar_columnas(self, nombre_bd, nombre_tabla):
        """ Muestra las tablas de la BD indicada """
        try:
            # Le indica que base de datos utilizar
            self.cursor.execute(f"USE {nombre_bd};")

            self.cursor.execute(f"SHOW COLUMNS FROM {nombre_tabla};")
            
            for columna in self.cursor.fetchall():
                not_null = "No admite valores nulos" if columna[2] == 'NO' else ""
                primary_key = "Es clave primaria" if columna[3] == 'PRI' else ""
                foreign_key = "Es clave externa" if columna[3] == 'MUL' else ""
                auto_incremental = "Autoincremental" if columna[5] == 'auto_increment' else ""
                print(f"{columna[0]} ({columna[1]}) {not_null} {primary_key} {foreign_key} {auto_incremental}")
        except:
            print(f"No se han podido consultar las columnas de {nombre_bd}.{nombre_tabla}")

    @conexion
    @comprueba_bd
    def insertar_registro(self, nombre_bd, nombre_tabla, registro):
        """ Inserta registros  en una tabla """
        self.cursor.execute(f"USE {nombre_bd}")

        # Si la lista está vacia
        if not registro:
            print("La lista de registro está vacía")
            return
        
        # Obtener las columnas y los valores de cada diccionario
        columnas = []
        valores = []
        for registro in registro:
            columnas.extend(registro.keys())
            valores.extend(registro.values())

        # Convertir las columnas y los valores a strings
        columnas_string = ''
        for columna in columnas:
            columnas_string += f"{columna}, "
        columnas_string += columnas_string[:-2] # Quitar la ultima coma y espacio

        valores_string = ''
        for valor in valores:
            valores_string += f"'{valor}', "
        valores_string += valores_string[:-2] # Quitar la ultima coma y espacio

        # Crear la instruccion de insercion
        sql = f"INSERT INTO {nombre_tabla} ({columnas_string}) VALUES ({valores_string})"
        self.cursor.execute(sql)
        self.conector.commit()
        print("Registro añadido a la tabla.")
    
    @conexion
    @comprueba_bd
    def eliminar_registro(self, nombre_bd, nombre_tabla, condiciones):
        """ Eliminar registros en una tabla """
        try:
            # Se selecciona la BD
            self.cursor.execute(f"USE {nombre_bd}")
            # Se crea la instruccion de eliminar
            sql = f"DELETE FROM {nombre_tabla} WHERE {condiciones}"
            # Se ejecuta y confirma
            self.cursor.execute(sql)
            self.conector.commit()
            print("Registros eliminados.")
        except:
            print("Error al intentar eliminar registros en la tabla.")
    
    @conexion
    @comprueba_bd
    def vaciar_tabla(self, nombre_bd, nombre_tabla):
        """ Vacia una tabla """
        try:
            # Se selecciona la BD
            self.cursor.execute(f"USE {nombre_bd}")
            # Se crea la instruccion de eliminar
            sql = f"TRUNCATE TABLE {nombre_tabla}"
            # Se ejecuta y confirma
            self.cursor.execute(sql)
            self.conector.commit()
            print("Se han eliminado todos los registros de la tabla.")
        except:
            print("Error al intentar eliminar todos los registros de la tabla.")

    @conexion
    @comprueba_bd
    def actualizar_registro(self, nombre_bd, nombre_tabla, columnas, condiciones):
        """ Actualiza el registro de una tabla """
        try:
            # Se selecciona la BD
            self.cursor.execute(f"USE {nombre_bd}")
            # Se crea la instruccion de actualizacion
            sql = f"UPDATE {nombre_tabla} SET {columnas} WHERE {condiciones}"
            # Se ejecuta y confirma
            self.cursor.execute(sql)
            self.conector.commit()
            print("Se actualizo el registro correctamente.")
        except:
            print("Error al intentar actualizar el registro.")