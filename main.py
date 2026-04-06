"""
=============================================================================
DICCIONARIO DE VARIABLES - SISTEMA DE STOCK Y CATEGORIZACIÓN DE VINOS
=============================================================================
Nota para el equipo: Usar esta nomenclatura exacta para mantener consistencia 
entre los módulos de base de datos y la interfaz.

--- BODEGAS ---
id_bodega          (int)   : PK - Identificador unico de la bodega.
nombre             (str)   : Nombre de la bodega.
direccion          (str)   : Dirección física.
localidad          (str)   : Ciudad / Localidad.
telefono           (str)   : Teléfono de contacto.

--- PROVEEDORES ---
id_proveedor       (int)   : PK - Identificador unico del distribuidor.
razon_social       (str)   : Nombre de la empresa proveedora.
cuit               (str)   : CUIT (con guiones).
telefono           (str)   : Teléfono del proveedor.
email              (str)   : Correo electrónico de ventas/contacto.
direccion          (str)   : Dirección del depósito/oficina.
contacto_nombre    (str)   : Nombre del vendedor o representante.

--- VINOS ---
id_vino            (int)   : PK - Identificador unico del vino.
id_bodega          (int)   : FK - Relación con la tabla Bodegas.
id_proveedor		(int)   : FK - Relación con la tabla Proveedores.
nombre      		(str)
cepa               (str)   : Tipo de uva (Malbec, Cabernet, etc.).
anejo              (int)   : Año de cosecha (sin 'ñ').
reserva            (int)   : 1 para Sí, 0 para No (Booleano en SQLite).
procedencia        (str)   : Región de origen.
lugar_envasado     (str)   : Dónde se embotelló (sin guion medio).
precio             (float) : Precio actual del producto.
stock              (int)   : Cantidad de botellas disponibles.

--- CLIENTES ---
id_cliente         (int)   : PK - Identificador unico del cliente.
nombre             (str)   : Nombre del cliente.
apellido           (str)   : Apellido del cliente.
dni                (str)   : Documento (str por si lleva puntos).
fecha_nac          (str)   : Fecha de nacimiento (Formato YYYY-MM-DD).
email              (str)   : Correo electrónico.
preferencia        (str)   : Tipo de vino favorito / notas del cliente.
telefono           (str)   : Teléfono de contacto.
direccion          (str)   : Dirección de envío o facturación.

--- ORDENES (TICKETS DE VENTA) ---
id_orden           (int)   : PK - Numero de ticket/factura.
id_cliente         (int)   : FK - Cliente que realizó la compra.
fecha_venta        (str)   : Fecha y hora de la operación.
total              (float) : Monto total de la orden.

--- DETALLE ORDENES (RENGLONES DEL TICKET) ---
id_detalle         (int)   : PK - Identificador unico del renglón.
id_orden           (int)   : FK - A qué orden pertenece este detalle.
id_vino            (int)   : FK - Qué vino se está vendiendo.
cantidad           (int)   : Cuántas botellas de este vino se llevan.
precio_unitario    (float) : Precio histórico al momento de la venta.
=============================================================================

"""
from sqlite3 import *
from datetime import datetime
import string

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
		cursor.execute("INSERT INTO Clientes (nombre, apellido, dni, fecha_nac, email, preferencia, telefono, direccion) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ("Consumidor", "Final", "0", "1900-01-01", "N/A", "N/A", "N/A", "Mostrador"))
		cursor.executescript(SQLITE_CREATE_TABLES)
		conexion.commit()
	except Error as e:
		print(f"Error al crear las tablas: {e}")

def initcap(text):
	return string.capwords(text)

def gestionar_bodegas(conexion):
	while True:
		print("\n--- Gestión de Bodegas ---")
		print("1. Agregar Bodega")
		print("2. Listar Bodegas")
		print("3. Modificar Bodega")
		print("0. Volver al Menu Principal")
		
		opcion = input("Seleccione una opción: ")
		
		if opcion == '1':
			print("\nIngresa los detalles de la nueva bodega")
			nom = input("Ingrese el nombre de la bodega: ")
			dir = input("Ingrese la dirección de la bodega: ")
			loc = input("Ingrese la localidad de la bodega: ")
			tel = input("Ingrese el teléfono de la bodega: ")

			conexion.execute("INSERT INTO Bodegas (nombre, direccion, localidad, telefono) VALUES (?, ?, ?, ?)", (nom, dir, loc, tel))
			conexion.commit()
			print("\n-- Bodega agregada exitosamente. --\n")            

		elif opcion == '2':

			fetch_bodegas = conexion.execute("SELECT * FROM Bodegas").fetchall()
			
			while True:
				print("\n--- Listas de Bodegas ---\nListar por localidad (L), por nombre (N), todas(T)?")

				criterio = input("Seleccione un criterio de ordenamiento (L/N/T/0 Salir): ").upper()

				if criterio == 'L':
					busqueda = input("Ingrese la localidad: ").lower()
					fetch_bodegas = conexion.execute("SELECT * FROM Bodegas WHERE LOWER(localidad) = ?", (busqueda,)).fetchall()
					titulo = f"\n--- Bodegas en la localidad seleccionada: {busqueda} ---"
						
				elif criterio == 'N':
					busqueda = input("Ingrese el nombre de la bodega: ").lower()
					fetch_bodegas = conexion.execute("SELECT * FROM Bodegas WHERE LOWER(nombre) = ?", (busqueda,)).fetchall()
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
								input("...")
								print(f"\n--- Siguiente Bodega ---")
							else:
								input("Presione Enter para finalizar la vista...") 
					else:
						print("No se encontraron resultados para su busqueda.")

		elif opcion == '3':
			
			nombre = input("Ingrese el nombre de la bodega que desea modificar: ").lower()

			bodega = conexion.execute("SELECT * FROM Bodegas WHERE LOWER(nombre) = ?", (nombre,)).fetchone()

			if bodega:
				print(f"Nombre: {bodega[1]}, Dirección: {bodega[2]}, Localidad: {bodega[3]}, Teléfono: {bodega[4]}")
				print("\nIngrese los nuevos detalles de la bodega (deje en blanco para mantener el valor actual):")
				nom = input(f"Nombre [{bodega[1]}]: ") or bodega[1]
				dir = input(f"Dirección [{bodega[2]}]: ") or bodega[2]
				loc = input(f"Localidad [{bodega[3]}]: ") or bodega[3]
				tel = input(f"Teléfono [{bodega[4]}]: ") or bodega[4]

				conexion.execute("UPDATE Bodegas SET nombre = ?, direccion = ?, localidad = ?, telefono = ? WHERE LOWER(nombre) = ?", (nom, dir, loc, tel, nombre))
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
		print("0. Volver al Menu Principal")
		
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
			print("\n-- Proveedor agregado exitosamente. --\n")

		elif opcion == '2':
				print("\n--- Lista de proveedores ---")
				print("Listado por Razon social")

				buscar_razon_social = input("Ingrese la razon social del proveedor: ").lower()
				fetch_proveedor = conexion.execute("SELECT * FROM PROVEEDORES WHERE LOWER(razon_social) = ?", (buscar_razon_social,)).fetchone()

				if fetch_proveedor:                
					print(f"CUIT: {fetch_proveedor[2]}\nEmail: {fetch_proveedor[3]}\nTelefono: {fetch_proveedor[4]}\nDireccion: {fetch_proveedor[5]}\nnombre contacto: {fetch_proveedor[6]}")
				else:
					print("No se encontró un proveedor con esa razon social.")

		elif opcion =='3':
			buscar_razon_social = input("Ingrese la razon social del proveedor: ").lower()
			proveedor = conexion.execute("SELECT * FROM PROVEEDORES WHERE LOWER(razon_social) = ?", (buscar_razon_social,)).fetchone()
			if proveedor:
					print(f"Nombre: {proveedor[1]}, Dirección: {proveedor[2]}, Localidad: {proveedor[3]}, Teléfono: {proveedor[4]}")
					print("\nIngrese los nuevos detalles del proveedor (deje en blanco para mantener el valor actual):")
					Telefono = input(f"Telefono [{proveedor[3]}]: ") or proveedor[3]
					Email = input(f"Email [{proveedor[4]}]: ") or proveedor[4]
					Direccion = input(f"Direccion [{proveedor[5]}]: ") or proveedor[5]
					Contacto_nombre = input(f"Contaco_nombre [{proveedor[6]}]: ") or proveedor[6]
					
					conexion.execute("UPDATE PROVEEDORES SET Telefono = ?, Email = ?, Direccion = ?, Contacto_nombre = ? WHERE LOWER(razon_social) = ?", (Telefono, Email, Direccion, Contacto_nombre, proveedor[1]))
					print("\n-- Proveedor modificado exitosamente. --\n")
			else:
					print("No se encontró un proveedor con esa razon social.")

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
		print("0. Volver al Menu Principal")
		
		opcion = input("Seleccione una opción: ")

		if opcion == '1':

			fetch_bodega = conexion.execute("SELECT ID_BODEGA, INITCAP(NOMBRE) FROM BODEGAS")
			fetch_prove = conexion.execute('SELECT ID_PROVEEDOR, INITCAP(RAZON_SOCIAL) FROM PROVEEDORES')

			mapa_bodega = {nombre: id_bodega for id_bodega, nombre in fetch_bodega}		
			mapa_prove = {razon_social: id_prov for id_prov, razon_social in fetch_prove}

			print(f"\nLas bodegas disponibles son: {', '.join(mapa_bodega.keys())} ")
			print(f"Los proveedores disponibles son: {', '.join(mapa_prove.keys())} ")

			print("\n--- Ingresa los detalles del vino nuevo --- ")
			id_bodega = input("Ingrese el nombre de la bodega: ").title()
			id_prove = input("Ingrese la razon social del proveedor: ").title()
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

			conexion.execute("INSERT INTO Vinos (id_bodega, id_proveedor, nombre, cepa, anejo, reserva, procedencia, lugar_envasado, precio, stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (fk_bode, fk_prove, nombre, cepa, anejo, reserva, procedencia, lugar_envasado ,precio, stock))
			conexion.commit()
			print("\n-- Vino agregado exitosamente. --\n")

		elif opcion == '2':
			
			while True:
				print("\n--- Lista de Vinos ---")
				print("Listar por cepa (C), procedencia (P), precio(T), (0)Salir?")

				criterio = input("Seleccione un criterio de listado (C/P/T/0): ").upper()

				if criterio == 'C':
					busqueda = input("Ingrese la cepa: ").lower()
					fetch_vinos = conexion.execute("SELECT * FROM VINOS WHERE LOWER(cepa) = ?", (busqueda,)).fetchall()
					titulo = f"\n--- Vinos por cepa seleccionada: '{busqueda}' encontrados {len(fetch_vinos)}"

				elif criterio == 'P':
					busqueda = input("Ingrese la procedencia: ").lower()
					fetch_vinos = conexion.execute("SELECT * FROM VINOS WHERE LOWER(procedencia) = ?", (busqueda,)).fetchall()
					titulo = f"\n--- Vinos de '{busqueda}' que estan en la bodega encontrados: {len(fetch_vinos)}"
					
				elif criterio == 'T':
					print("\ns--- Ingrese el rango de precios ---")
					busqueda1 = float(input("Ingrese precio minimo: $"))
					busqueda2 = float(input("Ingrese precio maximo: $"))
					
					fetch_vinos = conexion.execute("SELECT * FROM VINOS WHERE precio BETWEEN ? and ?", (busqueda1,busqueda2,)).fetchall()
					titulo = f"\n--- Vinos de entre ${busqueda1} y ${busqueda2} encontrados {len(fetch_vinos)}"
				
				elif criterio == '0':
					break
				
				if criterio in ['C', 'P', 'T']:
					if fetch_vinos:
						print(titulo)

						for i, vino in enumerate(fetch_vinos):
							texto_reserva = "Sí" if vino[6] == 1 else "No"

							if criterio == 'C':
								print(f"Nombre: {vino[3]}\nAño: {vino[5]}\nReserva: {texto_reserva}\nProcedencia: {vino[7]}\nLugar de envasado: {vino[8]}\nPrecio: {vino[9]}\nStock: {vino[10]}")
							elif criterio == 'P':
								print(f"Nombre: {vino[3]}\nCepa: {vino[4]}\nAño: {vino[5]}\nReserva: {texto_reserva}\nPrecio: {vino[9]}\nStock: {vino[10]}")
							elif criterio == 'T':
								if fetch_vinos:
									print(f"\nNombre: {vino[3]}\nProcedencia: {vino[7]}\nCepa: {vino[4]}\nPrecio: ${vino[9]}")
								else:
									print(f"\nNo se encontraron vinos en el rango de ${busqueda1} a ${busqueda2}.")

							if i < len(fetch_vinos) - 1:
								input("Presione Enter para continuar...")
								print("\n--- Siguiente Vino ---")
							else:
								input("Presione Enter para finalizar la vista...")
								break
					else:
						print("No se encontraron resultados para su busqueda.")

		elif opcion == '3':
			print("--- Modificación de vinos ---")

			fetch_vin = conexion.execute("SELECT nombre, cepa FROM VINOS")
			map_vin = {nombre: cepa for cepa, nombre in fetch_vin}

			print(f"\nLos vinos disponibles son: {', '.join([f"{clave}, {valor}" for clave, valor in map_vin.items()])}")
						
			buscar_nom = input("Ingrese el nombre: ").lower()
			buscar_ce = input("Ingrese la cepa: ").lower()

			vino = conexion.execute("SELECT * FROM VINOS WHERE LOWER(nombre) = ? AND LOWER(cepa) = ?", (buscar_nom,buscar_ce)).fetchone()

			if vino:
				print(f"\nNombre: {vino[3]}\nCepa: {vino[4]}\nAño: {vino[5]}\nReserva: {'Sí' if vino[6] == 1 else 'No'}")
				print("\nIngrese los nuevos detalles del vino (deje en blanco para mantener el valor actual):")
				nom = input(f"Nombre [{vino[3]}]: ") or vino[3]
				cep = input(f"Cepa [{vino[4]}]: ") or vino[4]
				ano = input(f"Año [{vino[5]}]: ") or vino[5]
				res = input(f"Reserva [{ 'Sí' if vino[6] == 1 else 'No' }]: ") or 'Sí' if vino[6] == 1 else 'No'
				pros = input(f"Procedencia [{vino[7]}]: ") or vino[7]
				lugar = input(f"Lugar de envasado [{vino[8]}]: ") or vino[8]
				precio = input(f"Precio [{vino[9]}]: ") or vino[9]
				stock = input(f"Stock [{vino[10]}]: ") or vino[10]

				conexion.execute("UPDATE VINOS SET nombre = ?, cepa = ?, anejo = ?, reserva = ?, procedencia = ?, lugar_envasado = ?, precio = ?, stock = ? WHERE LOWER(nombre) = ? AND LOWER(cepa) = ?", (nom, cep, ano, res, pros, lugar, precio, stock, buscar_nom, buscar_ce))
				conexion.commit()
				print("\n-- Vino modificado exitosamente. --\n")
			else:
				print("No se encontró un vino con ese nombre y cepa.")

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
		print("0. Volver al Menu Principal")
		
		opcion = input("Seleccione una opción: ")
		
		if opcion == '1':
			print("\nIngresa los detalles del nuevo cliente")
			nom = input("Ingrese el nombre: ")
			ape = input("Ingrese el apellido: ")
			dni = input("Ingrese el DNI: ") 
			fec_nac = input("Ingrese la fecha de nacimiento: ") 
			email = input("Ingrese el email: ")
			pref = input("Ingrese la preferencia de vino: ")
			tel = input("Ingrese el telefono: ")
			direc = input("Ingrese la dirección:  ")

			conexion.execute("INSERT INTO Clientes (nombre, apellido, dni, fecha_nac, email, preferencia, telefono, direccion) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nom, ape, dni, fec_nac, email, pref, tel, direc))
			conexion.commit()
			print("\n-- Cliente agregado exitosamente. --\n")

		elif opcion == '2':
			print("\n--- Listas de Clientes ---\nListar por preferencia (P)")

			criterio = input("Ingrese el criterio de ordenamiento: ").upper()

			if criterio == "P":
				busqueda = input("Ingrese la preferencia: ")
				fetch_clientes = conexion.execute("SELECT * FROM Clientes WHERE preferencia = ?", (busqueda,)).fetchall()
				titulo = f"\n--- Clientes con la preferencia: '{busqueda}' seleccionada son {len(fetch_clientes)}---"
			
			if fetch_clientes:
				print(titulo)

				for i, cli in enumerate(fetch_clientes):
					if criterio == "P":
						print(f"Nombre: {cli[1]}\nApellido: {cli[2]}\nFecha de nacimiento: {cli[4]}\nDirección: {cli[8]}\nTeléfono: {cli[7]}")
					
					if i < len(fetch_clientes) - 1:
						input("Presione Enter para continuar...")
						print("\n--- Siguiente Cliente ---")
					else:
						input("Presione Enter para finalizar la vista...") 
			else:
				print("No se encontraron resultados para su busqueda.")
		
		elif opcion == '3':
			print("--- Modificación de Clientes ---")

			fetch_cli = conexion.execute("SELECT dni FROM Clientes").fetchall()

			print(f"\n--- DNI de Clientes Disponibles ---")
			for i in fetch_cli:
				print(f"- {i[0]}")
						
			buscar_dni = input("\nIngrese el dni: ")

			cli = conexion.execute("SELECT * FROM Clientes WHERE dni = ?", (buscar_dni,)).fetchone()

			if cli:
				print(f"\nNombre: {cli[1]}\nApellido: {cli[2]}\nFecha de nacimiento: {cli[4]}\nEmail: {cli[5]}\nPreferencia: {cli[6]}\nTelefono: {cli[7]}\nDireccion: {cli[8]}")
				print("\nIngrese los nuevos detalles del cliente (deje en blanco para mantener el valor actual):")
				nom = input(f"Nombre [{cli[1]}]: ") or cli[1]
				ape = input(f"Apellido [{cli[2]}]: ") or cli[2]
				dni = input(f"DNI [{cli[3]}]: ") or cli[3]
				fec = input(f"Reserva [{cli[4]}]: ") or cli[4]
				email = input(f"Email [{cli[5]}]: ") or cli[5]
				pref = input(f"Preferencia [{cli[6]}]: ") or cli[6]
				tel = input(f"Telefono [{cli[7]}]: ") or cli[7]
				dire = input(f"Direccion [{cli[8]}]: ") or cli[8]

				conexion.execute("UPDATE Clientes SET nombre = ?, apellido = ?, dni = ?, fecha_nac = ?, email = ?, preferencia = ?, telefono = ?, direccion = ? WHERE dni = ?", (nom, ape, dni, fec, email, pref, tel, dire, buscar_dni))
				conexion.commit()
				print("\n-- Cliente modificado exitosamente. --\n")
			else:
				print("No se encontró un Cliente con ese DNI.")

		elif opcion == '0':
			break
		else:
			print("Opción no válida, por favor intente nuevamente.")

def armar_carrito(conexion):
	carrito = []
	print("\n--- INICIANDO NUEVA VENTA ---")

	while True:
		
		busqueda = input("\nIngrese el nombre del vino a vender (o '0' para finalizar y cobrar): ").lower()
		
		if busqueda == '0':
			break
			
		cursor = conexion.cursor()
		cursor.execute("SELECT id_vino, nombre, precio, stock FROM Vinos WHERE LOWER(nombre) LIKE ? OR LOWER(cepa) LIKE ?", (f"%{busqueda}%", f"%{busqueda}%"))
		resultados = cursor.fetchall()
		
		if not resultados:
			print("No se encontró ningun vino con ese nombre o cepa.")
			continue
			
		print("\nOpciones encontradas:")
		for i, vino in enumerate(resultados):
			print(f"{i + 1}. {vino[1]} | Precio: ${vino[2]} | Stock disponible: {vino[3]}")
			
		try:
			opcion = int(input("\nElija el numero del vino que desea agregar: ")) - 1
			if opcion < 0 or opcion >= len(resultados):
				print("Opción inválida.")
				continue
				
			vino_elegido = resultados[opcion]
			
			cantidad = int(input("Ingrese la cantidad a vender: "))
			
			if cantidad > vino_elegido[3]:
				print(f"¡ATENCIÓN! No hay stock suficiente. Solo quedan {vino_elegido[3]} botellas.")
				continue
			elif cantidad <= 0:
				print("La cantidad debe ser mayor a 0.")
				continue
				
			item = {
				"id_vino": vino_elegido[0],
				"nombre": vino_elegido[1],
				"precio": vino_elegido[2],
				"cantidad": cantidad
			}
			
			carrito.append(item)
			print(f"¡{cantidad}x {vino_elegido[1]} agregado(s) al carrito!")
			
		except ValueError:
			print("Por favor, ingrese numeros válidos.")

	return carrito

def registrar_venta(id_cliente, conexion, carrito):
	fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	total_venta = 0.0
	
	try:
		cursor = conexion.cursor()
		cursor.execute("INSERT INTO Ordenes (id_cliente, fecha_venta, total) VALUES (?, ?, ?)", (id_cliente, fecha_actual, 0.0)) 

		id_nueva_orden = cursor.lastrowid 

		for item in carrito:
			subtotal = item["cantidad"] * item["precio"]
			total_venta += subtotal
			
			cursor.execute("INSERT INTO DetalleOrdenes (id_orden, id_vino, cantidad, precio_unitario) VALUES (?, ?, ?, ?)", (id_nueva_orden, item["id_vino"], item["cantidad"], item["precio"]))
			
			cursor.execute("UPDATE Vinos SET stock = stock - ? WHERE id_vino = ?",(item["cantidad"], item["id_vino"]))
		
		cursor.execute("UPDATE Ordenes SET total = ? WHERE id_orden = ?", 
					(total_venta, id_nueva_orden))
		
		conexion.commit()
		print(f"\n--- ¡Venta Registrada Exitosamente! ---")
		print(f"N° de Ticket: {id_nueva_orden} | Total a cobrar: ${total_venta}")

	except Exception as e:
		conexion.rollback() 
		print(f"Ocurrió un error al procesar la venta: {e}")

def listar_ventas(conexion):
	print("\n=====================================")
	print("        HISTORIAL DE VENTAS")
	print("=====================================")

	cursor = conexion.cursor()
	ventas = cursor.execute("SELECT O.id_orden, O.fecha_venta, C.nombre, C.apellido, O.total FROM Ordenes O JOIN Clientes C ON O.id_cliente = C.id_cliente ORDER BY O.fecha_venta DESC LIMIT 15" ).fetchall()
	
	if not ventas:
		print("Todavía no hay ventas registradas en el sistema.")
		input("\nPresione Enter para volver...")
		return

	for v in ventas:
		cliente = f"{v[2]} {v[3]}" if v[2] != "Consumidor" else "Consumidor Final"
		fecha_corta = v[1][:16] 
		
		print(f"Ticket #{v[0]} | Fecha: {fecha_corta} | Cliente: {cliente} | Total: ${v[4]}")

	print("\n-------------------------------------")
	opcion = input("Ingrese el N° de Ticket para ver el detalle (o presione Enter para volver al menu): ")
	
	if opcion.isdigit():
		ver_detalle_ticket(conexion, opcion)

def ver_detalle_ticket(conexion, id_orden):
	print(f"\n--- DETALLE DEL TICKET #{id_orden} ---")
	
	detalles = conexion.execute("SELECT V.nombre, D.cantidad, D.precio_unitario, (D.cantidad * D.precio_unitario) as subtotal FROM DetalleOrdenes D JOIN Vinos V ON D.id_vino = V.id_vino WHERE D.id_orden = ?", (id_orden,)).fetchall()
	
	if not detalles:
		print("No se encontró el ticket o está vacío.")
	else:
		for d in detalles:
			print(f"> {d[1]}x {d[0]}")
			print(f"  Precio c/u: ${d[2]}  --->  Subtotal: ${d[3]}")
			
	input("\nPresione Enter para continuar...")

def realizar_venta(conexion):
	while True:
		print("\n--- Realizar Venta ---")
		print("1. Iniciar Nueva Venta")
		print("2. Listar ventas")
		print("0. Volver al Menu Principal")
		
		opcion = input("Seleccione una opción: ")
		
		if opcion == '1':

			fetch_cli = conexion.execute("SELECT dni FROM Clientes").fetchall()
			print(f"\n--- DNI de Clientes Disponibles ---")
			for i in fetch_cli:
				print(f"- {i[0]}")

			busqueda = input("Ingrese el DNI del cliente (o presione Enter para Consumidor Final): ")

			if busqueda == "":
				print("Venta a Consumidor Final.")
				cli_id = 1
			
			else:
				resultado = conexion.execute("SELECT id_cliente, nombre, apellido FROM Clientes WHERE dni = ?", (busqueda,)).fetchone()
				
				if resultado:
					cli_id = resultado[0]
					print(f"Cliente encontrado: {resultado[1]} {resultado[2]}")
				else:
					print("No se ha encontrado un cliente con ese DNI.\nIntente nuevamente...")
					continue

			mi_carrito = armar_carrito(conexion)
			if mi_carrito:
				registrar_venta(cli_id, mi_carrito)
		
		elif opcion == '2':
			listar_ventas(conexion)
				
		elif opcion == '0':
			break
		else:
			print("Opción no válida, por favor intente nuevamente.")

def main():
	conexion = conectar_db()
	conexion.create_function("INITCAP", 1, initcap)
	if conexion:
		crear_tablas(conexion)
		print("Base de datos y tablas creadas exitosamente.")
	else:
		print("No se pudo establecer conexión con la base de datos.")
	
	while True:
		print("\n--- Menu Principal ---")
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