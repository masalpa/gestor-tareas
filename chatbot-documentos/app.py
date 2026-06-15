import streamlit as st
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import pdfplumber
import os

load_dotenv()

st.title("📚 Chatbot de Documentos con IA")
st.write("Sube uno o varios PDFs y pregúntame lo que quieras sobre ellos")

if "listo" not in st.session_state:
    st.session_state.listo = False

if "historial" not in st.session_state:
    st.session_state.historial = []

pdfs = st.file_uploader("Sube tus documentos PDF:", type=["pdf"], accept_multiple_files=True)

if pdfs and not st.session_state.listo:
    with st.spinner("Procesando documentos..."):
        texto = ""
        for pdf in pdfs:
            with pdfplumber.open(pdf) as doc:
                for pagina in doc.pages:
                    texto += pagina.extract_text() or ""

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        trozos = splitter.create_documents([texto])

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma.from_documents(trozos, embeddings)
        st.session_state.db = db
        st.session_state.listo = True
        st.success(f"✅ {len(pdfs)} documento(s) procesado(s), ahora puedes hacer preguntas")

if st.session_state.listo:
    for mensaje in st.session_state.historial:
        if mensaje["role"] == "user":
            st.chat_message("user").write(mensaje["content"])
        else:
            st.chat_message("assistant").write(mensaje["content"])

    pregunta = st.chat_input("Pregunta algo sobre los documentos...")

    if pregunta:
        st.chat_message("user").write(pregunta)
        st.session_state.historial.append({"role": "user", "content": pregunta})

        with st.spinner("Buscando respuesta..."):
            docs = st.session_state.db.similarity_search(pregunta, k=3)
            contexto = "\n".join([d.page_content for d in docs])

            llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
            
            prompt = ChatPromptTemplate.from_template("""
            Responde la pregunta basándote SOLO en el siguiente contexto del documento.
            Si la respuesta no está en el contexto, di que no tienes esa información.
            
            Contexto: {contexto}
            
            Pregunta: {pregunta}
            """)
            
            chain = prompt | llm | StrOutputParser()
            respuesta = chain.invoke({"contexto": contexto, "pregunta": pregunta})

        st.chat_message("assistant").write(respuesta)
        st.session_state.historial.append({"role": "assistant", "content": respuesta})