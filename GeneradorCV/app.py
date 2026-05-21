import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from fpdf import FPDF
import os

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("📄 Generador de CV con IA")
st.write("Rellena tus datos y la IA generará un CV profesional")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre completo:")
    email = st.text_input("Email:")
    telefono = st.text_input("Teléfono:")
    ubicacion = st.text_input("Ubicación:")

with col2:
    puesto = st.text_input("Puesto al que aspiras:")
    experiencia = st.text_area("Experiencia laboral:")
    educacion = st.text_area("Educación:")

habilidades = st.text_area("Habilidades técnicas:")
sobre_mi = st.text_area("Cuéntame sobre ti (opcional):")

if st.button("🤖 Generar CV con IA"):
    if nombre and puesto:
        with st.spinner("La IA está generando tu CV..."):
            respuesta = cliente.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un experto en recursos humanos y redacción de CVs profesionales.
                        Genera un CV completo y profesional en español basado en los datos del usuario.
                        Usa este formato exacto:
                        
                        NOMBRE: 
                        CONTACTO:
                        SOBRE MÍ:
                        EXPERIENCIA:
                        EDUCACIÓN:
                        HABILIDADES:
                        """
                    },
                    {
                        "role": "user",
                        "content": f"""Genera un CV profesional para:
                        Nombre: {nombre}
                        Email: {email}
                        Teléfono: {telefono}
                        Ubicación: {ubicacion}
                        Puesto deseado: {puesto}
                        Experiencia: {experiencia}
                        Educación: {educacion}
                        Habilidades: {habilidades}
                        Sobre mí: {sobre_mi}"""
                    }
                ]
            )
            
            cv_generado = respuesta.choices[0].message.content
            st.session_state.cv = cv_generado
# Generar PDF
if "cv" in st.session_state:
    st.markdown("---")
    st.subheader("✅ Tu CV generado")
    st.write(st.session_state.cv)

if st.button("📥 Descargar CV en PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(20, 20, 20)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Helvetica", size=11)
        
        import textwrap
        for linea in st.session_state.cv.split("\n"):
            if linea.strip() == "":
                pdf.ln(4)
            elif linea.strip().isupper() or linea.strip().endswith(":"):
                pdf.set_font("Helvetica", style="B", size=12)
                for trozo in textwrap.wrap(linea, width=85):
                    texto = trozo.encode('latin-1', 'replace').decode('latin-1')
                    pdf.cell(0, 7, texto, ln=True)
                pdf.set_font("Helvetica", size=11)
            else:
                for trozo in textwrap.wrap(linea, width=90):
                    texto = trozo.encode('latin-1', 'replace').decode('latin-1')
                    pdf.cell(0, 6, texto, ln=True)
        
        pdf_bytes = pdf.output()
        st.download_button(
            label="⬇️ Haz clic aquí para descargar",
            data=bytes(pdf_bytes),
            file_name=f"CV_{nombre}.pdf",
            mime="application/pdf"
        )