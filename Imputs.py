import sqlite3
import random
from datetime import datetime, timedelta

# Conexión a la base de datos (cambiá el nombre si es distinto)
conexion = sqlite3.connect('bodega.db')
cursor = conexion.cursor()

# --- 1. DATOS FIJOS PARA BODEGAS (5 registros) ---
bodegas_data = [
    ("Bodega Catena Zapata", "Cobos s/n", "Luján de Cuyo", "261-4131100"),
    ("Bodega Salentein", "Ruta 89 s/n", "Valle de Uco", "2622-429500"),
    ("Bodega Norton", "Ruta 15 km 23", "Perdriel", "261-4909790"),
    ("Bodega Luigi Bosca", "San Martín 2044", "Luján de Cuyo", "261-4131100"),
    ("Bodega El Esteco", "Ruta Nacional 68", "Cafayate", "3868-421220")
]
for b in bodegas_data:
    cursor.execute("INSERT INTO Bodegas (nombre, direccion, localidad, telefono) VALUES (?, ?, ?, ?)", b)

# --- 2. DATOS FIJOS PARA PROVEEDORES (5 registros) ---
proveedores_data = [
    ("Distribuidora Cuyo S.A.", "30-71234567-9", "011-45678912", "ventas@cuyo.com", "Av. San Martín 1500", "Carlos Gómez"),
    ("Vinos del Interior SRL", "30-65432198-1", "351-4112233", "contacto@vinosinterior.com", "Ruta 9 Km 15", "Mariana López"),
    ("Logística Andina", "33-55554444-9", "261-4998877", "pedidos@andina.com", "Parque Industrial 2", "Roberto Sánchez"),
    ("Bebidas Premium", "30-11223344-5", "011-48887777", "info@premium.com", "Av. Callao 120", "Lucía Fernández"),
    ("El Bodeguero Mayorista", "30-99887766-2", "341-4556677", "ventas@bodeguero.com", "Bv. Oroño 300", "Diego Martínez")
]
for p in proveedores_data:
    cursor.execute("INSERT INTO Proveedores (razon_social, cuit, telefono, email, direccion, contacto_nombre) VALUES (?, ?, ?, ?, ?, ?)", p)

# --- 3. GENERAR 100 VINOS ---
cepas = ['Malbec', 'Cabernet Sauvignon', 'Merlot', 'Syrah', 'Chardonnay', 'Torrontés', 'Sauvignon Blanc', 'Pinot Noir', 'Bonarda']
nombres_base = ['Finca', 'Reserva', 'Gran Estirpe', 'Piedra Negra', 'Luna', 'Sol de los Andes', 'Cumbres', 'Valle Hermoso', 'El Secreto', 'Altos']
regiones = ['Mendoza', 'San Juan', 'Salta', 'La Rioja', 'Patagonia']

for _ in range(100):
    id_bodega = random.randint(1, 5)
    id_proveedor = random.randint(1, 5)
    nombre = f"{random.choice(nombres_base)} {random.choice(['Tinto', 'Blanco', 'Especial', 'Clásico', 'Roble'])}"
    cepa = random.choice(cepas)
    anejo = random.randint(2015, 2023)
    reserva = random.choice([0, 1])
    procedencia = random.choice(regiones)
    lugar_envasado = "Origen" if random.random() > 0.3 else "Planta Central"
    precio = round(random.uniform(3000.0, 25000.0), 2)
    stock = random.randint(0, 150)
    
    cursor.execute('''INSERT INTO Vinos (id_bodega, id_proveedor, nombre, cepa, anejo, reserva, procedencia, lugar_envasado, precio, stock) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (id_bodega, id_proveedor, nombre, cepa, anejo, reserva, procedencia, lugar_envasado, precio, stock))

cursor.execute('''INSERT INTO Clientes (nombre, apellido, dni, fecha_nac, email, preferencia, telefono, direccion) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
               ("Consumidor", "Final", "0", "1900-01-01", "N/A", "N/A", "N/A", "Mostrador"))

# --- 4. GENERAR 100 CLIENTES ---
nombres_cli = ['Juan', 'Maria', 'Pedro', 'Ana', 'Luis', 'Laura', 'Carlos', 'Sofia', 'Diego', 'Martina', 'Franco', 'Florencia']
apellidos_cli = ['Garcia', 'Lopez', 'Perez', 'Gonzalez', 'Rodriguez', 'Fernandez', 'Martinez', 'Gomez', 'Diaz', 'Alvarez', 'Romero']

for _ in range(99):
    nombre = random.choice(nombres_cli)
    apellido = random.choice(apellidos_cli)
    dni = str(random.randint(20000000, 45000000))
    # Generar fecha de nacimiento aleatoria (entre 1950 y 2004)
    año_nac = random.randint(1950, 2004)
    mes_nac = str(random.randint(1, 12)).zfill(2)
    dia_nac = str(random.randint(1, 28)).zfill(2)
    fecha_nac = f"{año_nac}-{mes_nac}-{dia_nac}"
    email = f"{nombre.lower()}.{apellido.lower()}{random.randint(1,99)}@gmail.com"
    preferencia = random.choice(cepas)
    telefono = f"3541-{random.randint(111111, 999999)}"
    direccion = f"Calle Falsa {random.randint(100, 999)}"
    
    cursor.execute('''INSERT INTO Clientes (nombre, apellido, dni, fecha_nac, email, preferencia, telefono, direccion) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (nombre, apellido, dni, fecha_nac, email, preferencia, telefono, direccion))

# --- 5. GENERAR 100 ÓRDENES Y SUS DETALLES ---
for i in range(1, 101): # i será el id_orden
    id_cliente = random.randint(1, 100)
    
    # Generar fecha de venta aleatoria en los últimos 365 días
    dias_restar = random.randint(0, 365)
    fecha_obj = datetime.now() - timedelta(days=dias_restar)
    fecha_venta = fecha_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    # Creamos la orden con un total inicial de 0
    cursor.execute('''INSERT INTO Ordenes (id_cliente, fecha_venta, total) VALUES (?, ?, ?)''', 
                   (id_cliente, fecha_venta, 0.0))
    
    # Cantidad de productos (renglones) distintos en este ticket (entre 1 y 3)
    cant_renglones = random.randint(1, 3)
    total_orden = 0.0
    
    for _ in range(cant_renglones):
        id_vino = random.randint(1, 100)
        cantidad = random.randint(1, 6) # Compra entre 1 y 6 botellas
        
        # Buscamos el precio actual del vino para simular el precio histórico
        cursor.execute("SELECT precio FROM Vinos WHERE id_vino = ?", (id_vino,))
        precio_unitario = cursor.fetchone()[0]
        
        subtotal = precio_unitario * cantidad
        total_orden += subtotal
        
        cursor.execute('''INSERT INTO DetalleOrdenes (id_orden, id_vino, cantidad, precio_unitario) 
                          VALUES (?, ?, ?, ?)''', 
                       (i, id_vino, cantidad, precio_unitario))
        
        # Descontamos el stock
        cursor.execute("UPDATE Vinos SET stock = stock - ? WHERE id_vino = ?", (cantidad, id_vino))
        
    # Actualizamos el total de la orden
    cursor.execute("UPDATE Ordenes SET total = ? WHERE id_orden = ?", (round(total_orden, 2), i))

# Guardamos los cambios y cerramos
conexion.commit()
conexion.close()

print("¡Datos ficticios insertados con éxito!")