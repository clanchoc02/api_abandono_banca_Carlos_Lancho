from pydantic import BaseModel, Field

# 1. Esquema de los datos de entrada del cliente bancario
class ClienteInput(BaseModel):
    id_cliente: str = Field(min_length=2, max_length=20, description="Identificador único del cliente")
    edad: float = Field(ge=18, le=120, description="Edad del cliente en años")
    ingresos_anuales: float = Field(ge=0, le=1000000, description="Ingresos anuales declarados")
    saldo_cuenta: float = Field(ge=0, le=1000000, description="Saldo actual en la cuenta principal")
    num_productos: int = Field(ge=1, le=10, description="Número de productos contratados con el banco")
    tiene_tarjeta: int = Field(ge=0, le=1, description="Indica si posee tarjeta (1 o 0)")
    antiguedad_meses: int = Field(ge=0, le=600, description="Antigüedad como cliente expresada en meses")
    tipo_cuenta: str = Field(min_length=2, max_length=30, description="Tipo de cuenta bancaria")
    canal_preferido: str = Field(min_length=2, max_length=30, description="Canal de comunicación o acceso favorito")
    nivel_estudios: str = Field(min_length=2, max_length=30, description="Nivel educativo del cliente")
    nivel_satisfaccion: str = Field(min_length=2, max_length=30, description="Grado de satisfacción percibido")

# 2. Esquema de la respuesta de salida del modelo (Predicción)
class PrediccionOutput(BaseModel):
    id_cliente: str = Field(description="Identificador único del cliente analizado")
    abandono: int = Field(description="Clase predicha: 0 (permanece) o 1 (abandona)")
    probabilidad_abandono: float = Field(ge=0.0, le=1.0, description="Probabilidad estimada de fuga")
    nivel_riesgo: str = Field(description="Calificación cualitativa del riesgo (Bajo, Medio, Alto)")
    accion_recomendada: str = Field(description="Directriz comercial a seguir por el gestor")