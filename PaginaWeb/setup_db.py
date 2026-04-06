import sqlite3
from sqlite3 import Error

def conectar_db():
    """Establece conexión con la base de datos SQLite"""
    try:
        conexion = sqlite3.connect('bodega.db')
        return conexion
    except Error as e:
        print(f"Error al conectar: {e}")
        return None

def crear_tablas(conexion):
    """Crea todas las tablas de la base de datos"""
    SQLITE_CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS Bodegas (id_bodega INTEGER PRIMARY KEY AUTOINCREMENT,
								nombre TEXT NOT NULL,
								direccion TEXT,
								localidad TEXT,
								telefono TEXT);

CREATE TABLE IF NOT EXISTS Proveedores (id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
									razon_social TEXT NOT NULL,
									cuit TEXT,
									telefono TEXT,
									email TEXT,
									direccion TEXT,
									contacto_nombre TEXT);

CREATE TABLE IF NOT EXISTS Vinos (id_vino INTEGER PRIMARY KEY AUTOINCREMENT,
							id_bodega INTEGER,
							id_proveedor INTEGER,
							nombre TEXT,
							cepa TEXT,
							anejo INTEGER,
							reserva INTEGER,
							procedencia TEXT,
							lugar_envasado TEXT,
							precio INTEGER,
							stock INTEGER,
							FOREIGN KEY (id_bodega) REFERENCES Bodegas(id_bodega),
							FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor));

CREATE TABLE IF NOT EXISTS Clientes (id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
								nombre TEXT,
								apellido TEXT,
								dni TEXT,
								fecha_nac DATE,
								email TEXT,
								preferencia TEXT,
								telefono TEXT,
								direccion TEXT);

CREATE TABLE IF NOT EXISTS Ordenes (id_orden INTEGER PRIMARY KEY AUTOINCREMENT,
							  id_cliente INTEGER,
							  fecha_venta DATE,
							  total INTEGER,
							  FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente));

CREATE TABLE IF NOT EXISTS DetalleOrdenes (id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
									id_orden INTEGER,
									id_vino INTEGER,
									cantidad INTEGER,
									precio_unitario INTEGER,
									FOREIGN KEY (id_orden) REFERENCES Ordenes(id_orden),
									FOREIGN KEY (id_vino) REFERENCES Vinos(id_vino));
"""
    try:
        cursor = conexion.cursor()
        cursor.executescript(SQLITE_CREATE_TABLES)
        conexion.commit()
        print("Tablas creadas exitosamente")
    except Error as e:
        print(f"Error al crear tablas: {e}")

if __name__ == '__main__':
    conexion = conectar_db()
    if conexion:
        crear_tablas(conexion)
        conexion.close()
        print("Base de datos inicializada")
