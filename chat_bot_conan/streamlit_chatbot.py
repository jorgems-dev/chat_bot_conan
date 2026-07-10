import os
from dotenv import load_dotenv
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate

import streamlit as st

load_dotenv()

def obtener_hora():
   return datetime.now().strftime("%H:%M")


# Configuración de la página 
st.set_page_config(page_title="ChatBot Conan", page_icon="👾")
st.markdown("<h1 style='text-align: center; font-size: 32px;'>ChatBot Conan 👾</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 24px'> *ChatBot en desarrollo*</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 24px'> ¿Con qué te puedo ayudar hoy?</p>", unsafe_allow_html=True)

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5, google_api_key=os.getenv("GEMINI_API_KEY"))


with st.sidebar:
   st.header("Configuración")
   temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
   model_name = st.selectbox("Modelo", ["gemini-2.5-flash"])

   personalidad = st.selectbox(
      "Personalidad del Asistente",
      [
         "Útil y amigable",
         "Profesional y formal",
         "Casual y relajado",
         "Experto técnico",
         "Creativo y divertido"
      ]
   )

   chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature, google_api_key=os.getenv("GEMINI_API_KEY"))

   system_messages = {
        "Útil y amigable": "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
        "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
        "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
        "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
        "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."   
   }
   chat_prompt = ChatPromptTemplate.from_messages([
      ("system", system_messages[personalidad]),
      ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
   ])

   cadena = chat_prompt | chat_model


# Inicializa el historial de mensajes del chat
if "mensajes" not in st.session_state:
   st.session_state.mensajes = []

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
