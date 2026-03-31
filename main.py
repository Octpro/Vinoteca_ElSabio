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
lugar_envasado     (str)   : Dónde se embotelló (sin guion medio).
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

			conexion.execute("INSERT INTO Bodegas (nombre, direccion, localidad, telefono) VALUES (?, ?, ?, ?)", (nom, dir, loc, tel))
			conexion.commit()
			print("\nBodega agregada exitosamente.\n")            

		elif opcion == '2':

			fetch_bodegas = conexion.execute("SELECT * FROM Bodegas").fetchall()
			
			while True:
				print("\n--- Lista de Bodegas ---")
				print("Listar por localidad (L), por nombre (N), todas(T)?")

				criterio = input("Seleccione un criterio de ordenamiento (L/N/T/0 Salir): ").upper()

				if criterio== 'L':
					busqueda = input("Ingrese la localidad: ")
					fetch_bodegas = conexion.execute("SELECT * FROM Bodegas WHERE localidad = ?", (busqueda,)).fetchall()
					titulo = f"\n--- Bodegas en la localidad seleccionada: {busqueda} ---"
						
				elif criterio == 'N':
					busqueda = input("Ingrese el nombre de la bodega: ")
					fetch_bodegas = conexion.execute("SELECT * FROM Bodegas WHERE nombre = ?", (busqueda,)).fetchall()
					titulo = f"\n--- Bodegas con el nombre seleccionado: {busqueda} ---"

				elif criterio == 'T':
					fetch_bodegas = conexion.execute("SELECT * FROM Bodegas").fetchall()
					titulo = f"\n--- Listado de todas las bodegas {len(fetch_bodegas)} --- "
			
				elif criterio == '0':
					break

				if criterio in ["L", "N", "T"]:
					if fetch_bodegas:
						print(titulo)

						for i, bodega in enumerate(fetch_bodegas):                      
							if criterio == 'L':
								print(f"Nombre: {bodega[1]}\nDirección: {bodega[2]}\nTeléfono: {bodega[4]}")
							elif criterio == 'N':
								print(f"Localidad: {bodega[3]}\nDirección: {bodega[2]}\nTeléfono: {bodega[4]}")
							elif criterio == 'T':
								print(f"Nombre: {bodega[1]}\nDirección: {bodega[2]}\nLocalidad: {bodega[3]}\nTeléfono: {bodega[4]}")    
							
							if i < len(fetch_bodegas) - 1:
								input("Presione Enter para continuar...")
								print("\n--- Siguiente Bodega ---")
							else:
								input("Presione Enter para finalizar la vista...") 
					else:
						print("No se encontraron resultados para su búsqueda.")

		elif opcion == '3':
			
			nombre = input("Ingrese el nombre de la bodega que desea modificar: ")

			bodega = conexion.execute("SELECT * FROM Bodegas WHERE nombre = ?", (nombre,)).fetchone()

			if bodega:
				print(f"Nombre: {bodega[1]}, Dirección: {bodega[2]}, Localidad: {bodega[3]}, Teléfono: {bodega[4]}")
				print("\nIngrese los nuevos detalles de la bodega (deje en blanco para mantener el valor actual):")
				nom = input(f"Nombre [{bodega[1]}]: ") or bodega[1]
				dir = input(f"Dirección [{bodega[2]}]: ") or bodega[2]
				loc = input(f"Localidad [{bodega[3]}]: ") or bodega[3]
				tel = input(f"Teléfono [{bodega[4]}]: ") or bodega[4]

				conexion.execute("UPDATE Bodegas SET nombre = ?, direccion = ?, localidad = ?, telefono = ? WHERE nombre = ?", (nom, dir, loc, tel, nombre))
				print("Bodega modificada exitosamente.")
			else:
				print("No se encontró una bodega con ese nombre.")

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
			print("\nIngresa los detalles del nuevo proveedor:")
			razon_social= input("Ingrese la razon social: ")
			cuit= input("Ingrese el CUIT del proveedor: ")
			email = input("Ingrese el email del proveedor: ")
			tel = input("Ingrese el teléfono del proveedor: ")
			dir = input("Ingrese la dirección del proveedor: ")
			nom_contacto = input("Ingrese el nombre del contacto del proveedor: ")
			
			conexion.execute("INSERT INTO Proveedores(razon_social, cuit, email, telefono, direccion, contacto_nombre) VALUES (?,?,?,?,?,?)", (razon_social, cuit, email, tel, dir, nom_contacto))
			conexion.commit()
			print("\nProveedor agregado exitosamente.\n")

		elif opcion == '2':
				print("\n--- Lista de proveedores ---")
				print("Listado por Razon social")

				buscar_razon_social = input("Ingrese la razon social del proveedor: ")
				fetch_proveedor = conexion.execute("SELECT * FROM PROVEEDORES WHERE razon_social = ?", (buscar_razon_social,)).fetchone()

				if fetch_proveedor:                
					print(f"CUIT: {fetch_proveedor[2]}\nEmail: {fetch_proveedor[3]}\nTelefono: {fetch_proveedor[4]}\nDireccion: {fetch_proveedor[5]}\nnombre contacto: {fetch_proveedor[6]}")
					break
				else:
					print("No se encontró un proveedor con esa razon social.")

		elif opcion =='3':
			buscar_razon_social = input("Ingrese la razon social del proveedor: ")
			proveedor = conexion.execute("SELECT * FROM PROVEEDORES WHERE razon_social = ?", (buscar_razon_social,)).fetchone()
			if proveedor:
					print(f"Nombre: {proveedor[1]}, Dirección: {proveedor[2]}, Localidad: {proveedor[3]}, Teléfono: {proveedor[4]}")
					print("\nIngrese los nuevos detalles del proveedor (deje en blanco para mantener el valor actual):")
					Telefono = input(f"Telefono [{proveedor[3]}]: ") or proveedor[3]
					Email = input(f"Email [{proveedor[4]}]: ") or proveedor[4]
					Direccion = input(f"Direccion [{proveedor[5]}]: ") or proveedor[5]
					Contacto_nombre = input(f"Contaco_nombre [{proveedor[6]}]: ") or proveedor[6]
					
					conexion.execute("UPDATE PROVEEDORES SET Telefono = ?, Email = ?, Direccion = ?, Contacto_nombre = ? WHERE razon_social = ?", (Telefono, Email, Direccion, Contacto_nombre, proveedor[1]))
					print("proveedor modificado exitosamente.")
			else:
					print("No se encontró un proveedor con esa razon social.")

			break

		elif opcion == '0':
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

		fetch_bodega = conexion.execute("SELECT ID_BODEGA, NOMBRE FROM BODEGAS")
		fetch_prove = conexion.execute('SELECT ID_PROVEEDOR, RAZON_SOCIAL FROM PROVEEDORES')

		mapa_bodega = {nombre: id_bodega for id_bodega, nombre in fetch_bodega}		
		mapa_prove = {razon_social: id_prov for id_prov, razon_social in fetch_prove}

		if opcion == '1':

			print(f"\nLas bodegas disponibles son: {mapa_bodega} ")
			print(f"Los proveedores disponibles son: {mapa_prove} ")

			print("\n--- Ingresa los detalles del vino nuevo --- ")

			id_bodega = input("Ingrese el nombre de la bodega: ")
			id_prove = input("Ingrese la razon social del proveedor: ")
			nombre = input("Ingrese el nombre del vino: ")
			cepa = input("Ingrese la cepa del vino: ")
			anejo = int(input("Ingrese el año de elaboración: "))
			reserva = int(input("Ingresa si fue reserva (1:Si, 0:No): "))
			procedencia = input("Ingrese la region de origen: ")
			lugar_envasado = input("Ingrese donde se embotello: ")
			precio = float(input("Ingrese el precio actual del producto: $"))
			stock = int(input("Ingrese la cantidad de botellas disponibles: "))

			fk_bode = mapa_bodega[id_bodega]
			fk_prove = mapa_prove[id_prove]

			conexion.execute("INSERT INTO Vinos (id_bodega, id_proveedor, cepa, anejo, reserva, procedencia, lugar_envasado, precio, stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (fk_bode, fk_prove, cepa, anejo, reserva, procedencia, lugar_envasado ,precio, stock))
			conexion.commit()
			print("\nVino agregado exitosamente.\n")

		elif opcion == '2':
			
			while True:
				print("\n--- Lista de Vinos ---")
				print("Listar por cepa (C), procedencia (P), precio(T), (0)Salir?")

				criterio = input("Seleccione un criterio de listado (C/P/T): ").upper()

				if criterio == 'C':
					busqueda = input("Ingrese la cepa: ")
					fetch_vinos = conexion.execute("SELECT * FROM VINOS WHERE cepa = ?", (busqueda,)).fetchall()
					titulo = f"\n--- Vinos por cepa seleccionada: {busqueda}"

				elif criterio == 'P':
					busqueda = input("Ingrese la procedencia: ")
					fetch_vinos = conexion.execute("SELECT * FROM VINOS WHERE procedencia = ?", (procedencia,)).fetchall()
					titulo = f"\n--- Vinos de {busqueda} que estan en la bodega"
					
				elif criterio == 'T':
					print("\n--- Ingrese el rango de precios ---")
					busqueda1 = float(input("Ingrese precio minimo: $"))
					busqueda2 = float(input("Ingrese precio maximo: $"))
					
					fetch_vinos = conexion.execute("SELECT * FROM VINOS WHERE precio BETWEEN ? and ?", (busqueda1,busqueda2,)).fetchall()
				
				elif criterio == '0':
					break
				
				if criterio in ['C', 'P', 'T']:
					if fetch_vinos:
						print(titulo)

						for i, vino in enumerate(fetch_vinos):
							texto_reserva = "Sí" if vino[5] == 1 else "No"

							if criterio == 'C':
								print(f"Cepa: {vino[3]}\nAño: {vino[4]} Reserva: {texto_reserva}\nProcedencia: {vino[6]}\nPrecio: {vino[9]}\nStock: {vino[10]}")
							elif criterio == 'P':
								print(f"Cepa: {vino[3]}\nAño: {vino[4]}\nReserva: {texto_reserva}\nProcedencia: {vino[6]}\nPrecio: {vino[9]}\nStock: {vino[10]}")
							elif criterio == 'T':
								if fetch_vinos:
									print(f"\n--- Vinos encontrados entre ${busqueda1} y ${busqueda2} ---")
									print(f"Procedencia: {vino[6]} | Cepa: {vino[3]} | Precio: ${vino[9]}")
								else:
									print(f"\nNo se encontraron vinos en el rango de ${busqueda1} a ${busqueda2}.")

							if i < len(fetch_vinos) - 1:
								input("Presione Enter para continuar...")
								print("\n--- Siguiente Vino ---")
							else:
								input("Presione Enter para finalizar la vista...")
								break
					else:
						print("No se encontraron resultados para su búsqueda.")

		elif opcion == '3':

			#Buscar por nombre y cepa para cambiar el vino
			
			buscar_id = input("Ingrese el ID de la bodega que desea modificar: ")

			bodega = conexion.execute("SELECT * FROM Bodegas WHERE id_bodega = ?", (buscar_id,)).fetchone()

			if bodega:
				print(f"Nombre: {bodega[1]}, Dirección: {bodega[2]}, Localidad: {bodega[3]}, Teléfono: {bodega[4]}")
				print("\nIngrese los nuevos detalles de la bodega (deje en blanco para mantener el valor actual):")
				nom = input(f"Nombre [{bodega[1]}]: ") or bodega[1]
				dir = input(f"Dirección [{bodega[2]}]: ") or bodega[2]
				loc = input(f"Localidad [{bodega[3]}]: ") or bodega[3]
				tel = input(f"Teléfono [{bodega[4]}]: ") or bodega[4]
				
				conexion.execute("UPDATE Bodegas SET nombre = ?, direccion = ?, localidad = ?, telefono = ? WHERE id_bodega = ?", (nom, dir, loc, tel, buscar_id))
				print("Bodega modificada exitosamente.")
			else:
				print("No se encontró una bodega con ese ID.")

		elif opcion == '0':
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
			gestionar_bodegas(conexion)
		elif opcion == '2':
			gestionar_proveedores(conexion)
		elif opcion == '3':
			gestionar_vinos(conexion)
		elif opcion == '4':
			gestionar_clientes(conexion)
		elif opcion == '5':
			realizar_venta(conexion)
		elif opcion == '0':
			print("Saliendo del programa.")
			break
		else:
			print("Opción no válida, por favor intente nuevamente.")
			
if __name__ == "__main__":
	main()