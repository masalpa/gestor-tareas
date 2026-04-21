from groq import Groq
from datetime import datetime

cliente = Groq(api_key="TU_API_KEY_AQUI")

historial = [
    {
        "role": "system",
        "content": """Eres un asistente experto en programación. 
        Cuando alguien te pregunta sobre código siempre:
        1. Explicas el concepto en 2-3 líneas
        2. Das un ejemplo de código claro
        3. Explicas el ejemplo línea por línea
        Respondes siempre en español y de forma sencilla."""
    }
]

conversacion_guardada = []

print("🤖 Asistente de Código")
print("Pregúntame cualquier duda de programación")
print("Escribe 'salir' para terminar\n")

while True:
    pregunta = input("Tú: ")
    
    if pregunta.lower() == "salir":
        # Guardar conversación en archivo
        nombre_archivo = f"conversacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            for linea in conversacion_guardada:
                f.write(linea + "\n\n")
        print(f"✅ Conversación guardada en {nombre_archivo}")
        print("¡Hasta luego!")
        break
    
    historial.append({"role": "user", "content": pregunta})
    
    respuesta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=historial
    )
    
    mensaje_ia = respuesta.choices[0].message.content
    historial.append({"role": "assistant", "content": mensaje_ia})
    
    conversacion_guardada.append(f"Tú: {pregunta}")
    conversacion_guardada.append(f"IA: {mensaje_ia}")
    
    print("\n🤖:", mensaje_ia, "\n")