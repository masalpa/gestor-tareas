import streamlit as st
from database import crear_tabla, agregar_tarea, obtener_tareas, completar_tarea, eliminar_tarea
from ia import analizar_tarea, sugerir_orden
from datetime import date
import plotly.graph_objects as go
from database import obtener_estadisticas

# Inicializar base de datos
crear_tabla()

st.title("📋 Gestor de Tareas con IA")

# Sidebar - Añadir tarea
st.sidebar.title("➕ Nueva Tarea")

titulo = st.sidebar.text_input("Título de la tarea:")
descripcion = st.sidebar.text_area("Descripción:")
fecha = st.sidebar.date_input("Fecha límite:", min_value=date.today())

if st.sidebar.button("Añadir y analizar con IA"):
    if titulo:
        with st.spinner("La IA está analizando tu tarea..."):
            analisis = analizar_tarea(titulo, descripcion)
            
            lineas = analisis.split("\n")
            prioridad = "Media"
            tiempo = "Sin estimar"
            
            for linea in lineas:
                if "PRIORIDAD:" in linea:
                    prioridad = linea.replace("PRIORIDAD:", "").strip()
                if "TIEMPO:" in linea:
                    tiempo = linea.replace("TIEMPO:", "").strip()
            
            agregar_tarea(titulo, descripcion, prioridad, tiempo, str(fecha))
            
            st.sidebar.success("✅ Tarea añadida")
            st.sidebar.info(analisis)
    else:
        st.sidebar.warning("Escribe un título para la tarea")

# Tareas pendientes
tareas = obtener_tareas()

if len(tareas) == 0:
    st.info("No tienes tareas pendientes. ¡Añade una desde el panel izquierdo!")
else:
    # Botón sugerir orden
    if st.button("🤖 Sugerir orden óptimo con IA"):
        with st.spinner("La IA está pensando..."):
            sugerencia = sugerir_orden(tareas)
            st.success(sugerencia)

    st.markdown("---")
    st.subheader(f"Tareas pendientes ({len(tareas)})")

    for tarea in tareas:
        id, titulo, descripcion, prioridad, tiempo, completada, fecha = tarea
        
        color = "🔴" if prioridad == "Alta" else "🟡" if prioridad == "Media" else "🟢"
        
        with st.expander(f"{color} {titulo} — {prioridad} · {tiempo} · {fecha}"):
            st.write(descripcion)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Completar", key=f"completar_{id}"):
                    completar_tarea(id)
                    st.rerun()
            with col2:
                if st.button("🗑️ Eliminar", key=f"eliminar_{id}"):
                    eliminar_tarea(id)
                    st.rerun()
# Estadísticas
st.markdown("---")
st.subheader("📊 Estadísticas")

stats = obtener_estadisticas()

col1, col2, col3 = st.columns(3)
col1.metric("Total tareas", stats["total"])
col2.metric("Completadas", stats["completadas"])
col3.metric("Pendientes", stats["pendientes"])

# Gráfica de prioridades
fig = go.Figure(data=[
    go.Bar(
        x=["Alta", "Media", "Baja"],
        y=[stats["alta"], stats["media"], stats["baja"]],
        marker_color=["red", "orange", "green"]
    )
])
fig.update_layout(title="Tareas por prioridad", xaxis_title="Prioridad", yaxis_title="Cantidad")
st.plotly_chart(fig)