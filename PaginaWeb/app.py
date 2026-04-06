from flask import Flask, render_template, request
import sqlite3
from collections import defaultdict

app = Flask(__name__)

def get_db_connection():
    """Crea y retorna una conexión a la base de datos"""
    try:
        conn = sqlite3.connect('bodega.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error conexión: {e}")
        return None

@app.route('/')
def index():
    """Página principal con resumen"""
    conn = get_db_connection()
    if not conn:
        return "Error de conexión a base de datos", 500
    
    cursor = conn.cursor()
    
    # Obtener estadísticas
    cursor.execute("SELECT SUM(stock) FROM Vinos")
    total_stock = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM Ordenes")
    total_ordenes = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM Clientes")
    total_clientes = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM Proveedores")
    total_proveedores = cursor.fetchone()[0] or 0
    
    # Obtener 6 vinos destacados (primeros 6)
    cursor.execute("SELECT * FROM Vinos LIMIT 6")
    vinos_destacados = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html',
                         total_stock=total_stock,
                         total_ordenes=total_ordenes,
                         total_clientes=total_clientes,
                         total_proveedores=total_proveedores,
                         vinos_destacados=vinos_destacados)

@app.route('/vinos')
def vinos():
    """Página de catálogo de vinos"""
    conn = get_db_connection()
    if not conn:
        return "Error de conexión a base de datos", 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vinos")
    vinos = cursor.fetchall()
    
    conn.close()
    
    return render_template('vinos.html', vinos=vinos)

@app.route('/bodegas')
def bodegas():
    """Página de bodegas"""
    conn = get_db_connection()
    if not conn:
        return "Error de conexión a base de datos", 500
    
    cursor = conn.cursor()
    
    # Obtener todas las bodegas
    cursor.execute("SELECT * FROM Bodegas")
    bodegas = cursor.fetchall()
    
    # Contar vinos por bodega
    cursor.execute("SELECT id_bodega, COUNT(*) as count FROM Vinos GROUP BY id_bodega")
    vinos_count_data = cursor.fetchall()
    vinos_count = {row[0]: row[1] for row in vinos_count_data}
    
    conn.close()
    
    return render_template('bodegas.html', bodegas=bodegas, vinos_count=vinos_count)

@app.route('/clientes')
def clientes():
    """Página de clientes"""
    conn = get_db_connection()
    if not conn:
        return "Error de conexión a base de datos", 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes LIMIT 20")
    clientes = cursor.fetchall()
    
    conn.close()
    
    return render_template('clientes.html', clientes=clientes)

@app.route('/proveedores')
def proveedores():
    """Página de proveedores"""
    conn = get_db_connection()
    if not conn:
        return "Error de conexión a base de datos", 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()
    
    conn.close()
    
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/ordenes')
def ordenes():
    """Página de órdenes"""
    conn = get_db_connection()
    if not conn:
        return "Error de conexión a base de datos", 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ordenes LIMIT 20")
    ordenes = cursor.fetchall()
    
    conn.close()
    
    return render_template('ordenes.html', ordenes=ordenes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
