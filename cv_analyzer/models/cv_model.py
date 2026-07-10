from pydantic import BaseModel, Field

class Modelo_cv(BaseModel):
    nombre_candidato: str = Field(description="Nombre completo del candidato extraído del CV.")
    experiencia_años: int = Field(description="Años totales de experiencia laboral relevante.")
    habilidades_clave: list[str] = Field(description="Lista de las habilidades más relevantes del candidato para el puesto.")
    education:str = Field(description="Nivel educativo más alto y especialización principal.")
    experiencia_relevante: str = Field(description="Resumen conciso de la experiencia más relevante para el puesto específico.")
    fortalezas: list[str] = Field(description="Principales fortalezas del cadidato.")
    areas_mejora: list[str] = Field(description="Áreas donde el candidato podría desarrollarse.")
    porcentaje_ajuste: int = Field(description="Porcentaje de ajuste al puesto (0-100), basado en la experiencia, habilidades y formación.", ge=0, le=100)
  