### Diccionario con las columnas

columnas = [
    {
        'name': 'id',
        'type': 'INT',
        'lenght': 10,
        'primary_key': True,
        'auto_increment': True,
        'not_null': True
    },
    {
        'name': 'nombre',
        'type': 'VARCHAR',
        'lenght': 32,
        'primary_key': False,
        'auto_increment': False,
        'not_null': True
    },
    {
        'name': 'apellidos',
        'type': 'VARCHAR',
        'lenght': 64,
        'primary_key': False,
        'auto_increment': False,
        'not_null': True
    },
    {
        'name': 'telefono',
        'type': 'VARCHAR',
        'lenght': 9,
        'primary_key': False,
        'auto_increment': False,
        'not_null': False
    },
    {
        'name': 'direccion',
        'type': 'VARCHAR',
        'lenght': 128,
        'primary_key': False,
        'auto_increment': False,
        'not_null': False
    }
]

# base_datos.crear_tabla('base_datos_cualquiera', 'nombre_tabla', columnas)