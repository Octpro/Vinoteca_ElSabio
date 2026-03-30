"""
=============================================================================
DICCIONARIO DE VARIABLES - SISTEMA DE STOCK Y CATEGORIZACIÓN DE VINOS
=============================================================================
Nota para el equipo: Usar esta nomenclatura exacta para mantener consistencia 
entre los módulos de base de datos y la interfaz.

--- BODEGAS ---
id_bodega          (int)   : PK - Identificador único de la bodega.
nombre             (str)   : Nombre de la bodega.
direccion          (str)   : Dirección física.
localidad          (str)   : Ciudad / Localidad.
telefono           (str)   : Teléfono de contacto.

--- PROVEEDORES ---
id_proveedor       (int)   : PK - Identificador único del distribuidor.
razon_social       (str)   : Nombre de la empresa proveedora.
cuit               (str)   : CUIT (con guiones).
telefono           (str)   : Teléfono del proveedor.
email              (str)   : Correo electrónico de ventas/contacto.
direccion          (str)   : Dirección del depósito/oficina.
contacto_nombre    (str)   : Nombre del vendedor o representante.

--- VINOS ---
id_vino            (int)   : PK - Identificador único del vino.
id_bodega          (int)   : FK - Relación con la tabla Bodegas.
id_proveedor       (int)   : FK - Relación con la tabla Proveedores.
cepa               (str)   : Tipo de uva (Malbec, Cabernet, etc.).
anejo              (int)   : Año de cosecha (sin 'ñ').
reserva            (int)   : 1 para Sí, 0 para No (Booleano en SQLite).
procedencia        (str)   : Región de origen.
destino            (str)   : Mercado objetivo.
lugar_envasado     (str)   : Dónde se embotelló (sin guion medio).
vinedo_procedencia (str)   : Finca específica (sin 'ñ' ni guion medio).
precio             (float) : Precio actual del producto.
stock              (int)   : Cantidad de botellas disponibles.

--- CLIENTES ---
id_cliente         (int)   : PK - Identificador único del cliente.
nombre             (str)   : Nombre del cliente.
apellido           (str)   : Apellido del cliente.
dni                (str)   : Documento (str por si lleva puntos).
fecha_nac          (str)   : Fecha de nacimiento (Formato YYYY-MM-DD).
email              (str)   : Correo electrónico.
preferencia        (str)   : Tipo de vino favorito / notas del cliente.
telefono           (str)   : Teléfono de contacto.
direccion          (str)   : Dirección de envío o facturación.

--- ORDENES (TICKETS DE VENTA) ---
id_orden           (int)   : PK - Número de ticket/factura.
id_cliente         (int)   : FK - Cliente que realizó la compra.
fecha_venta        (str)   : Fecha y hora de la operación.
total              (float) : Monto total de la orden.

--- DETALLE ORDENES (RENGLONES DEL TICKET) ---
id_detalle         (int)   : PK - Identificador único del renglón.
id_orden           (int)   : FK - A qué orden pertenece este detalle.
id_vino            (int)   : FK - Qué vino se está vendiendo.
cantidad           (int)   : Cuántas botellas de este vino se llevan.
precio_unitario    (float) : Precio histórico al momento de la venta.
=============================================================================
"""
from sqlite3 import *
from datetime import datetime

def conectar_db():
    """Establece conexión con la base de datos SQLite y devuelve el objeto conexión."""
    try:
        conexion = connect('bodega.db')
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
def crear_tablas(conexion):
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
                                cepa TEXT,
                                anejo INTEGER,
                                reserva INTEGER,
                                procedencia TEXT,
                                destino TEXT,
                                lugar_envasado TEXT,
                                vinedo_procedencia TEXT,
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
    except Error as e:
        print(f"Error al crear las tablas: {e}")

def gestionar_bodegas(conexion):
    while True:
        print("\n--- Gestión de Bodegas ---")
        print("1. Agregar Bodega")
        print("2. Listar Bodegas")
        print("3. Modificar Bodega")
        print("0. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("\nIngresa los detalles de la nueva bodega:")
            nom = input("Ingrese el nombre de la bodega: ")
            dir = input("Ingrese la dirección de la bodega: ")
            loc = input("Ingrese la localidad de la bodega: ")
            tel = input("Ingrese el teléfono de la bodega: ")

            conectar_db().execute("INSERT INTO Bodegas (nombre, direccion, localidad, telefono) VALUES (?, ?, ?, ?)", (nom, dir, loc, tel))
            print("Bodega agregada exitosamente.")

        elif opcion == '2':

            fetch_bodegas = conectar_db().execute("SELECT * FROM Bodegas").fetchall()
            
            while True:
                print("\n--- Lista de Bodegas ---")
                print("Listar por localidad (L), por nombre (N), todas(T)?")

                criterio = input("Seleccione un criterio de ordenamiento (L/N/T): ").upper()

                if criterio == 'L':

                    fetch_bodegas = conectar_db().execute("SELECT * FROM Bodegas WHERE localidad = ?", (input("Ingrese la localidad: "),)).fetchall()
                    print(f"\n--- Bodegas en la localidad seleccionada: {fetch_bodegas[0][3] if fetch_bodegas else 'No se encontraron bodegas en esa localidad'}---")
                    print(f"Nombre: {bodega[1]}, Dirección: {bodega[2]} Teléfono: {bodega[4]}")
                    break

                elif criterio == 'N':
                    
                    fetch_bodegas = conectar_db().execute("SELECT * FROM Bodegas WHERE nombre = ?", (input("Ingrese el nombre de la bodega: "),)).fetchall()
                    print(f"\n--- Bodegas con el nombre seleccionado: {fetch_bodegas[0][1] if fetch_bodegas else 'No se encontraron bodegas con ese nombre'}---")
                    print(f"Localidad: {bodega[3]}, Dirección: {bodega[2]} Teléfono: {bodega[4]}")
                    break

                elif criterio == 'T':

                    for bodega in fetch_bodegas:
                        print(f"ID: {bodega[0]}, Nombre: {bodega[1]}, Dirección: {bodega[2]}, Localidad: {bodega[3]}, Teléfono: {bodega[4]}")
                
                        if bodega != fetch_bodegas[-1]:
                            input("Presione Enter para continuar...")
                            print("\n--- Siguiente Bodega ---")


        elif opcion == '3':
            
            buscar_id = input("Ingrese el ID de la bodega que desea modificar: ")

            bodega = conectar_db().execute("SELECT * FROM Bodegas WHERE id_bodega = ?", (buscar_id,)).fetchone()

            if bodega:
                print(f"ID: {bodega[0]}, Nombre: {bodega[1]}, Dirección: {bodega[2]}, Localidad: {bodega[3]}, Teléfono: {bodega[4]}")
                print("\nIngrese los nuevos detalles de la bodega (deje en blanco para mantener el valor actual):")
                nom = input(f"Nombre [{bodega[1]}]: ") or bodega[1]
                dir = input(f"Dirección [{bodega[2]}]: ") or bodega[2]
                loc = input(f"Localidad [{bodega[3]}]: ") or bodega[3]
                tel = input(f"Teléfono [{bodega[4]}]: ") or bodega[4]

                conectar_db().execute("UPDATE Bodegas SET nombre = ?, direccion = ?, localidad = ?, telefono = ? WHERE id_bodega = ?", (nom, dir, loc, tel, buscar_id))
                print("Bodega modificada exitosamente.")
            else:
                print("No se encontró una bodega con ese ID.")

        elif opcion == '0':
            break
        else:
            print("Opción no válida, por favor intente nuevamente.")

def gestionar_proveedores(conexion):
    while True:
        print("\n--- Gestión de Proveedores ---")
        print("1. Agregar Proveedor")
        print("2. Listar Proveedores")
        print("3. Modificar Proveedor")
        print("0. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("Funcionalidad de agregar proveedor (pendiente de implementación).")
            # Aquí se implementaría la función para agregar un proveedor
        elif opcion == '2':
            print("Funcionalidad de listar proveedores (pendiente de implementación).")
            # Aquí se implementaría la función para listar los proveedores
        elif opcion == '3':
            break
        else:
            print("Opción no válida, por favor intente nuevamente.")

def gestionar_vinos(conexion):
    while True:
        print("\n--- Gestión de Vinos ---")
        print("1. Agregar Vino")
        print("2. Listar Vinos")
        print("3. Modificar Vino")
        print("0. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("Funcionalidad de agregar vino (pendiente de implementación).")
            # Aquí se implementaría la función para agregar un vino
        elif opcion == '2':
            print("Funcionalidad de listar vinos (pendiente de implementación).")
            # Aquí se implementaría la función para listar los vinos
        elif opcion == '3':
            break
        else:
            print("Opción no válida, por favor intente nuevamente.")

def gestionar_clientes(conexion):
    while True:
        print("\n--- Gestión de Clientes ---")
        print("1. Agregar Cliente")
        print("2. Listar Clientes")
        print("3. Modificar Cliente")
        print("0. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("Funcionalidad de agregar cliente (pendiente de implementación).")
            # Aquí se implementaría la función para agregar un cliente
        elif opcion == '2':
            print("Funcionalidad de listar clientes (pendiente de implementación).")
            # Aquí se implementaría la función para listar los clientes
        elif opcion == '3':
            break
        else:
            print("Opción no válida, por favor intente nuevamente.")

def realizar_venta(conexion):
    while True:
        print("\n--- Realizar Venta ---")
        print("1. Iniciar Nueva Venta")
        print("0. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("Funcionalidad de iniciar nueva venta (pendiente de implementación).")
            # Aquí se implementaría la función para iniciar una nueva venta
        elif opcion == '2':
            break
        else:
            print("Opción no válida, por favor intente nuevamente.")


def main():
    conexion = conectar_db()
    if conexion:
        crear_tablas(conexion)
        print("Base de datos y tablas creadas exitosamente.")
        conexion.close()
    else:
        print("No se pudo establecer conexión con la base de datos.")
    
    while True:
        print("\n--- Menú Principal ---")
        print("1. Gestionar Bodegas")
        print("2. Gestionar Proveedores")
        print("3. Gestionar Vinos")
        print("4. Gestionar Clientes")
        print("5. Realizar Venta")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("Funcionalidad de gestión de bodegas (pendiente de implementación).")
            gestionar_bodegas(conexion)
        elif opcion == '2':
            print("Funcionalidad de gestión de proveedores (pendiente de implementación).")
            gestionar_proveedores(conexion)
        elif opcion == '3':
            print("Funcionalidad de gestión de vinos (pendiente de implementación).")
            gestionar_vinos(conexion)
        elif opcion == '4':
            print("Funcionalidad de gestión de clientes (pendiente de implementación).")
            gestionar_clientes(conexion)
        elif opcion == '5':
            print("Funcionalidad de realización de ventas (pendiente de implementación).")
            realizar_venta(conexion)
        elif opcion == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor intente nuevamente.")

if __name__ == "__main__":
    main()