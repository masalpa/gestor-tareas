from groq import Groq

cliente = Groq(api_key="TU_API_KEY_AQUI")

def analizar_texto(texto):
    respuesta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Eres un analizador de texto experto. 
                Cuando recibas un texto responde siempre en este formato exacto:
                
                RESUMEN: (resume el texto en 2 líneas)
                TONO: (di si es positivo, negativo o neutro)
                IDEAS PRINCIPALES:
                - idea 1
                - idea 2
                - idea 3"""
            },
            {
                "role": "user",
                "content": f"Analiza este texto: {texto}"
            }
        ]
    )
    return respuesta.choices[0].message.content

print("📝 Analizador de Texto con IA")
print("Pega tu texto y pulsa Enter dos veces\n")

lineas = []
while True:
    linea = input()
    if linea == "":
        break
    lineas.append(linea)

texto = "\n".join(lineas)
print("\nAnalizando...\n")
print(analizar_texto(texto))