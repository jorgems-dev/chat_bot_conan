import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from models.cv_model import Modelo_cv
from prompts.cv_prompts import crear_sistema_prompts

load_dotenv()

def crear_evaluador_cv():
    modelo_base = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, google_api_key=os.getenv("GEMINI_API_KEY"))

    modelo_estructurado = modelo_base.with_structured_output(Modelo_cv)
    chat_prompt = crear_sistema_prompts()
    cadena_evaluacion = chat_prompt |modelo_estructurado

    return cadena_evaluacion

def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> Modelo_cv:
    try:
        cadena_evaluacion = crear_evaluador_cv()

        resultado = cadena_evaluacion.invoke({"texto_cv": texto_cv, "descripcion_puesto": descripcion_puesto})

        return resultado
    
    except Exception as e:
        return Modelo_cv(
            nombre_candidato="Error en procesamiento.", 
            experiencia_años=0, 
            habilidades_clave=["Error al procesar cv"], 
            education="No se puede determinar.", 
            experiencia_relevante="Error durante el análisis.",
            fortalezas=["Requiere revisión manual del CV."],
            areas_mejora=["Verificar formato y legibilidad del PDF."],
            porcentaje_ajuste=0
        )