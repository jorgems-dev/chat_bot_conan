import os
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def obtener_hora():
   return datetime.now().strftime("%H:%M")


# Configuración de la página 
st.set_page_config(page_title="ChatBot Conan", page_icon="👾")
st.markdown("<h1 style='text-align: center; font-size: 32px;'>ChatBot Conan 👾</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 24px'> *ChatBot en desarrollo*</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 24px'> ¿Con qué te puedo ayudar hoy?</p>", unsafe_allow_html=True)

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)


with st.sidebar:
   st.header("Configuración")
   temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
   model_name = st.selectbox("Modelo", ["gemini-2.5-flash"])

   chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)


# Inicializa el historial de mensajes del chat
if "mensajes" not in st.session_state:
   st.session_state.mensajes = []

prompt_template = PromptTemplate(
   input_variables=["mensaje", "historial"],
   template="""Eres un asistente útil y amigable llamado ChatBot Conan.
   Historial de conversación:
   {historial}
   
   Responde de forma clara y concisa a la siguiente pregunta: {mensaje}"""
)

cadena = prompt_template | chat_model

# Mostrar mensajes precios en la interfaz
for item in st.session_state.mensajes:
   msg = item["mensajes"]
   hora = item["hora"]
   # No muestra mensaje del sistema
   if isinstance(msg, SystemMessage):
      continue
    
   role = "assistant" if isinstance(msg, AIMessage) else "user"

   with st.chat_message(role):
      st.markdown(msg.content)
      st.caption(hora)
   
if st.button("Nueva convesación"):
   st.session_state.mensajes = []
   st.rerun()

# Entrada de texto del usuario
pregunta = st.chat_input("Escribe tu mensaje: ")

if pregunta:
   # Mostrar mensaje del usuario en la interfaz
   with st.chat_message("user"):
      st.markdown(pregunta)
      st.caption(obtener_hora())

   try:
      with st.chat_message("assistant"):
         response_placeholder = st.empty()
         full_response = ""

         for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
               full_response += chunk.content
               response_placeholder.markdown(full_response + " ")

         response_placeholder.markdown(full_response)
      
      st.session_state.mensajes.append({
         "mensajes" : HumanMessage(content=pregunta),
         "hora" : obtener_hora()
         })
      st.session_state.mensajes.append({
         "mensajes": AIMessage(content=full_response),
         "hora": obtener_hora()
         })
   except Exception as e:
      st.error(f"Error al generar respuesta: {str(e)}")
      st.info("Verifica que tu API KEY de Google esté configurada correctamente")
