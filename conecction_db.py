import sqlite3


def connect_db():
    conexion = sqlite3.connect("bd1.db")
    try:
        conexion.execute(
            """create table clientes (
                                id integer primary key autoincrement,
                                nombre_completo text,
                                edad real,
                                fecha_de_ingreso text,
                                direccion text
                            )"""
        )
        conexion.execute(
            """
            create table series (
                id integer primary key autoincrement,
                cliente text,
                inicio timestamp,
                cantidad real,
                fin timestamp
            )
            """
        )
    except sqlite3.OperationalError:
        print("La tabla clientes ya existe")
    conexion.close()


def insert_cliente(nombre, edad, fecha, direccion):
    connect_db()
    conexion = sqlite3.connect("bd1.db")
    conexion.execute(
        "insert into clientes(nombre_completo, edad, fecha_de_ingreso, direccion) values (?, ?, ?, ?)",
        (nombre, edad, fecha, direccion),
    )
    conexion.commit()
    conexion.close()


def insert_serie(cliente, inicio, cantidad, fin):
    connect_db()
    conexion = sqlite3.connect("bd1.db")
    conexion.execute(
        "insert into series(cliente, inicio, cantidad, fin) values (?, ?, ?, ?)",
        (cliente, inicio, cantidad, fin),
    )
    conexion.commit()
    conexion.close()


def list_customer():
    list_user = []
    connect_db()
    conexion = sqlite3.connect("bd1.db")
    cursor = conexion.execute("select * from clientes")
    for fila in cursor:
        list_user.append(fila[1])
    conexion.close()
    return list_user
