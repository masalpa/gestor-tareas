import sqlite3

def conectar():
    conn = sqlite3.connect("tareas.db")
    return conn

def crear_tabla():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            prioridad TEXT,
            tiempo_estimado TEXT,
            completada INTEGER DEFAULT 0,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

def agregar_tarea(titulo, descripcion, prioridad, tiempo_estimado, fecha):
    conn = conectar()
    conn.execute("""
        INSERT INTO tareas (titulo, descripcion, prioridad, tiempo_estimado, fecha)
        VALUES (?, ?, ?, ?, ?)
    """, (titulo, descripcion, prioridad, tiempo_estimado, fecha))
    conn.commit()
    conn.close()

def obtener_tareas():
    conn = conectar()
    cursor = conn.execute("SELECT * FROM tareas WHERE completada = 0 ORDER BY fecha")
    tareas = cursor.fetchall()
    conn.close()
    return tareas

def completar_tarea(id):
    conn = conectar()
    conn.execute("UPDATE tareas SET completada = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def eliminar_tarea(id):
    conn = conectar()
    conn.execute("DELETE FROM tareas WHERE id = ?", (id,))
    conn.commit()
    conn.close()