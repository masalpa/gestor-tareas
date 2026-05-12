import streamlit as st
from database import crear_tabla, agregar_tarea, obtener_tareas, completar_tarea, eliminar_tarea, obtener_estadisticas
from ia import analizar_tarea, sugerir_orden
from datetime import date
from database import obtener_tareas_por_dia
import plotly.graph_objects as go

crear_tabla()

st.title("📋 Gestor de Tareas con IA")

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

tareas = obtener_tareas()

filtro = st.selectbox("Filtrar por prioridad:", ["Todas", "Alta", "Media", "Baja"])
if filtro != "Todas":
    tareas = [t for t in tareas if t[3] == filtro]

if len(tareas) == 0:
    st.info("No tienes tareas pendientes. ¡Añade una desde el panel izquierdo!")
else:
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
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Completar", key=f"completar_{id}"):
                    completar_tarea(id)
                    st.rerun()
            with col2:
                if st.button("🗑️ Eliminar", key=f"eliminar_{id}"):
                    eliminar_tarea(id)
                    st.rerun()
            with col3:
                if st.button("✏️ Editar", key=f"editar_{id}"):
                    st.session_state[f"editando_{id}"] = True

            if st.session_state.get(f"editando_{id}"):
                nuevo_titulo = st.text_input("Nuevo título:", value=titulo, key=f"titulo_{id}")
                nueva_desc = st.text_area("Nueva descripción:", value=descripcion, key=f"desc_{id}")
                nueva_fecha = st.date_input("Nueva fecha:", key=f"fecha_{id}")
                if st.button("💾 Guardar", key=f"guardar_{id}"):
                    from database import editar_tarea
                    editar_tarea(id, nuevo_titulo, nueva_desc, str(nueva_fecha))
                    st.session_state[f"editando_{id}"] = False
                    st.rerun()

st.markdown("---")
st.subheader("📊 Estadísticas")
stats = obtener_estadisticas()

col1, col2, col3 = st.columns(3)
col1.metric("Total tareas", stats["total"])
col2.metric("Completadas", stats["completadas"])
col3.metric("Pendientes", stats["pendientes"])

fig = go.Figure(data=[
    go.Bar(
        x=["Alta", "Media", "Baja"],
        y=[stats["alta"], stats["media"], stats["baja"]],
        marker_color=["red", "orange", "green"]
    )
])
fig.update_layout(title="Tareas por prioridad", xaxis_title="Prioridad", yaxis_title="Cantidad")
st.plotly_chart(fig)
# Gráfica por día
datos_dia = obtener_tareas_por_dia()
if len(datos_dia) > 0:
    fechas = [d[0] for d in datos_dia]
    cantidades = [d[1] for d in datos_dia]
    fig2 = go.Figure(data=[
        go.Scatter(
            x=fechas,
            y=cantidades,
            mode="lines+markers",
            line=dict(color="green"),
            marker=dict(size=8)
        )
    ])
    fig2.update_layout(title="Tareas completadas por día", xaxis_title="Fecha", yaxis_title="Tareas completadas")
    st.plotly_chart(fig2)
else:
    st.info("Completa algunas tareas para ver la gráfica por día")