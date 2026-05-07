import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🤖 Asistente de Código con IA")
st.write("Pregúntame cualquier duda de programación")

st.sidebar.title("⚙️ Opciones")
lenguaje = st.sidebar.selectbox(
    "Lenguaje de programación:",
    ["Python", "Java", "JavaScript", "C++", "General"]
)

pregunta = st.text_input("Tu pregunta:")

if st.button("Preguntar"):
    if pregunta:
        with st.spinner("Pensando..."):
            respuesta = cliente.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Eres un experto en {lenguaje}. Responde en español con ejemplos de código."},
                    {"role": "user", "content": pregunta}
                ]
            )
            st.write(respuesta.choices[0].message.content)
    else:
        st.warning("Escribe una pregunta primero")