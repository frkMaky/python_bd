import bd.base_datos as sqlbd
import os 
import bd.tablas as tablas
import interfaz.interfaz_grafica as gui

os.system("cls")

# Se llama a la BD e inicia el acceso   
base_datos = sqlbd.BaseDatos(**sqlbd.acceso_bd)

#consula_1 = base_datos.consulta("SHOW DATABASES")
#for bd in consula_1: # Se itera el resultado 
#    print(bd)

# base_datos.mostrar_bd()
# base_datos.eliminar_bd("pruebas")
# base_datos.crear_base_datos("pruebas")
# base_datos.crear_tabla("pruebas","usuarios", tablas.columnas )
# base_datos.eliminar_tabla("pruebas","usuarios")
# base_datos.mostrar_tablas("world")

ventana_loguin = gui.Login()

# ventana_opciones = gui.VentanaOpciones()