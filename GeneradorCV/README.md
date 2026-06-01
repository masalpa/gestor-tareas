# Generador de CV con IA

App web que genera CVs profesionales usando inteligencia artificial. El usuario rellena sus datos y la IA crea un CV personalizado descargable en PDF.

## 🌐 App en vivo
[Ver la app aquí](https://gestor-tareas-lusapxvmtcxgihmtwwfoxa.streamlit.app)

## Tecnologías usadas
- Python
- Streamlit
- Groq API (LLaMA 3.3)
- FPDF2

## Funcionalidades
- Formulario con datos personales, experiencia y habilidades
- La IA genera un CV profesional adaptado al puesto deseado
- Descarga del CV en PDF con diseño profesional

## Cómo usarlo
1. Clona el repositorio
2. Instala las dependencias: `pip install streamlit groq python-dotenv fpdf2`
3. Crea un archivo `.env` con tu API key: `GROQ_API_KEY=tu_key`
4. Ejecuta: `python -m streamlit run app.py`

## Autor
Masalpa — desarrollador de IA