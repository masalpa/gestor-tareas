# Gestor de Tareas con IA

App web para gestionar tareas con inteligencia artificial. La IA analiza cada tarea, le asigna prioridad, estima el tiempo y sugiere el orden óptimo para completarlas.

## Tecnologías usadas
- Python
- Streamlit
- Groq API (LLaMA 3.3)
- SQLite

## Funcionalidades
- Añadir tareas con título, descripción y fecha límite
- La IA analiza automáticamente la prioridad y tiempo estimado
- Sugerencia de orden óptimo con IA
- Marcar tareas como completadas
- Eliminar tareas

## Cómo usarlo
1. Clona el repositorio
2. Instala las dependencias: `pip install streamlit groq python-dotenv`
3. Crea un archivo `.env` con tu API key: `GROQ_API_KEY=tu_key`
4. Ejecuta: `python -m streamlit run app.py`

## Autor
Masalpa — desarrollador de IA