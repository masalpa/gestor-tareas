from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analizar_tarea(titulo, descripcion):
    respuesta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Eres un experto en productividad y gestión de tareas.
                Cuando recibas una tarea responde SOLO en este formato exacto:
                
                PRIORIDAD: (Alta, Media o Baja)
                TIEMPO: (estimación en horas o minutos)
                CONSEJO: (un consejo breve para completar la tarea)"""
            },
            {
                "role": "user",
                "content": f"Analiza esta tarea:\nTítulo: {titulo}\nDescripción: {descripcion}"
            }
        ]
    )
    return respuesta.choices[0].message.content

def sugerir_orden(tareas):
    lista = "\n".join([f"- {t[1]}: {t[2]}" for t in tareas])
    respuesta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Eres un experto en productividad. Sugiere el orden óptimo para completar estas tareas y explica por qué en 3 líneas. Responde en español."
            },
            {
                "role": "user",
                "content": f"Estas son mis tareas pendientes:\n{lista}\n¿En qué orden las hago?"
            }
        ]
    )
    return respuesta.choices[0].message.content