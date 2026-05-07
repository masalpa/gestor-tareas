import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🤖 Asistente de Código con IA")

# Sidebar
st.sidebar.title("⚙️ Opciones")

lenguaje = st.sidebar.selectbox(
    "Lenguaje de programación:",
    ["Python", "Java", "JavaScript", "C++", "General"]
)

idioma = st.sidebar.selectbox(
    "Idioma de respuesta:",
    ["Español", "Inglés", "Francés", "Alemán"]
)

if st.sidebar.button("🗑️ Limpiar conversación"):
    st.session_state.historial = []
    st.session_state.tokens = 0

if "historial" not in st.session_state:
    st.session_state.historial = []

if "tokens" not in st.session_state:
    st.session_state.tokens = 0

# Contador de tokens
st.sidebar.markdown("---")
st.sidebar.metric("Tokens usados", st.session_state.tokens)

# Subir archivo
archivo = st.file_uploader("Sube un archivo de código para analizarlo", type=["py", "js", "java", "cpp", "txt"])

if archivo:
    codigo = archivo.read().decode("utf-8")
    st.code(codigo)
    if st.button("Analizar código"):
        with st.spinner("Analizando..."):
            respuesta = cliente.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Eres un experto en programación. Responde en {idioma}. Analiza el código, explica qué hace y sugiere mejoras."},
                    {"role": "user", "content": f"Analiza este código:\n{codigo}"}
                ]
            )
            st.session_state.tokens += respuesta.usage.total_tokens
            st.write(respuesta.choices[0].message.content)

# Historial
for mensaje in st.session_state.historial:
    if mensaje["role"] == "user":
        st.chat_message("user").write(mensaje["content"])
    else:
        st.chat_message("assistant").write(mensaje["content"])

# Input
pregunta = st.chat_input("Escribe tu pregunta...")

if pregunta:
    st.session_state.historial.append({"role": "user", "content": pregunta})
    st.chat_message("user").write(pregunta)

    with st.spinner("Pensando..."):
        mensajes = [
            {"role": "system", "content": f"Eres un experto en {lenguaje}. Responde en {idioma} con ejemplos de código."}
        ] + st.session_state.historial

        respuesta = cliente.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mensajes
        )

        mensaje_ia = respuesta.choices[0].message.content
        st.session_state.tokens += respuesta.usage.total_tokens
        st.session_state.historial.append({"role": "assistant", "content": mensaje_ia})
        st.chat_message("assistant").write(mensaje_ia)