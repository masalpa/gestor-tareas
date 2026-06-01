import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import pdfplumber
import requests
from bs4 import BeautifulSoup

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🔍 Analizador de Ofertas de Trabajo con IA")
st.write("Pega una oferta de trabajo y te digo si encajas")

if "cv_texto" not in st.session_state:
    st.session_state.cv_texto = ""

if "analisis" not in st.session_state:
    st.session_state.analisis = ""

if "oferta_texto" not in st.session_state:
    st.session_state.oferta_texto = ""

st.subheader("📎 Sube tu CV (opcional)")
cv_archivo = st.file_uploader("Sube tu CV en PDF:", type=["pdf"])

if cv_archivo:
    with pdfplumber.open(cv_archivo) as pdf:
        cv_texto = ""
        for pagina in pdf.pages:
            cv_texto += pagina.extract_text() or ""
    st.session_state.cv_texto = cv_texto
    st.success("✅ CV cargado correctamente")
    st.write(cv_texto[:500])
else:
    cv_texto = st.session_state.cv_texto

st.markdown("---")

st.subheader("📋 Tu perfil")
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Tu nombre:")
    experiencia_años = st.slider("Años de experiencia:", 0, 20, 0)
    educacion = st.text_input("Educación:")

with col2:
    habilidades = st.text_area("Tus habilidades técnicas:")
    experiencia = st.text_area("Tu experiencia laboral:")

st.markdown("---")

st.subheader("📄 Oferta de trabajo")
url_oferta = st.text_input("Pega el enlace de la oferta (Infojobs, LinkedIn...):")
oferta = st.text_area("O pega el texto de la oferta aquí:", height=200)

if url_oferta and st.button("🔗 Cargar oferta desde URL"):
    with st.spinner("Cargando oferta..."):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url_oferta, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            oferta_cargada = soup.get_text(separator="\n", strip=True)[:3000]
            st.session_state.oferta_texto = oferta_cargada
            st.success("✅ Oferta cargada correctamente")
            st.write(oferta_cargada[:300])
        except:
            st.error("No se pudo cargar la oferta, pégala manualmente")

oferta_final = oferta or st.session_state.oferta_texto

if st.button("🤖 Analizar con IA"):
    if oferta_final and (habilidades or st.session_state.cv_texto):
        with st.spinner("Analizando la oferta..."):
            respuesta = cliente.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un experto en recursos humanos y selección de personal.
                        Analiza si el candidato encaja con la oferta de trabajo y responde SIEMPRE en este formato:

                        PUNTUACIÓN: (del 1 al 10 cuánto encaja el candidato)
                        
                        HABILIDADES QUE TIENES:
                        - habilidad 1
                        - habilidad 2
                        
                        HABILIDADES QUE TE FALTAN:
                        - habilidad 1
                        - habilidad 2
                        
                        CONSEJOS PARA MEJORAR TU CANDIDATURA:
                        - consejo 1
                        - consejo 2
                        
                        CONCLUSIÓN: (un párrafo final con tu valoración)"""
                    },
                    {
                        "role": "user",
                        "content": f"""Analiza si este candidato encaja con esta oferta:
                        
                        PERFIL DEL CANDIDATO:
                        Nombre: {nombre}
                        Años de experiencia: {experiencia_años}
                        Educación: {educacion}
                        Habilidades: {habilidades}
                        Experiencia: {experiencia}
                        CV completo: {st.session_state.cv_texto}
                        
                        OFERTA DE TRABAJO:
                        {oferta_final}"""
                    }
                ]
            )
            
            st.session_state.analisis = respuesta.choices[0].message.content

if st.session_state.analisis:
    st.markdown("---")
    st.subheader("📊 Resultado del análisis")
    st.write(st.session_state.analisis)