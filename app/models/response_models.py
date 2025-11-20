from pydantic import BaseModel
from datetime import datetime, date


class Event(BaseModel):
    titulo: str
    data_inicio: date
    data_fim: date
    local: str


class Certificate(BaseModel):
    hash_confirmacao: str
    data_emissao: datetime
    evento: Event


class CertificateResponse(BaseModel):
    success: bool = True
    certificados: list[Certificate]
