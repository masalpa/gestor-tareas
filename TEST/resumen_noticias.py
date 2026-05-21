from groq import Groq
from dotenv import load_dotenv
from newspaper import Article
import os

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extraer_texto(url):
    articulo = Article(url, language='es')
    articulo.download()
    articulo.parse()
    return articulo.text

def resumir_noticia(texto):
    respuesta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Eres un resumidor de noticias experto.
                Cuando recibas una noticia responde siempre así:
                
                TITULAR: (titular en una línea)
                RESUMEN: (resumen en 2 líneas)
                PUNTOS CLAVE:
                - punto 1
                - punto 2
                - punto 3
                - punto 4
                - punto 5"""
            },
            {
                "role": "user",
                "content": f"Resume esta noticia: {texto[:3000]}"
            }
        ]
    )
    return respuesta.choices[0].message.content

url = input("Pega la URL de la noticia: ")

print("\nExtrayendo noticia...\n")
texto = extraer_texto(url)

print("Resumiendo con IA...\n")
print(resumir_noticia(texto))