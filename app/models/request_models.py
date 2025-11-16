from pydantic import BaseModel


class CertificateRequest(BaseModel):
    id_usuario: int
    nome: str
    id_evento: int
    titulo: str
    data_inicio: str
    data_fim: str
