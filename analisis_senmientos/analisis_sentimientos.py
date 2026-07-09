import json, os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.5
)

class Analisis(BaseModel):
    sentimiento : str = Field(description="positivo, negativo o neutro")
    resumen: str = Field(description="Resume en una oración")
    razon: str = Field(description="Justificación breve")

structured_llm = chat_model.with_structured_output(Analisis)

def preprocess_text(text):
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

prmpt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Eres un experto en análisis de textos.

        Devuelve:

        - Resumen (una oración)
        - Sentimiento (positivo, negativo, neutro)
        - Razón
        """
    ),
    (
        "human",
        "{texto}"
    ),
    
])

prompt_chain = (
    prmpt | 
    structured_llm
)

chain = preprocessor | RunnableLambda(lambda texto: {"texto": texto}) | prompt_chain 

textos_prueba = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]

for texto in textos_prueba:
    resultado = chain.invoke(texto)

    print("=" * 50 )
    print("Texto: ", texto)
    print("Resumen: ", resultado.resumen)
    print("Sentimiento: ", resultado.sentimiento)
    print("Razón: ", resultado.razon)