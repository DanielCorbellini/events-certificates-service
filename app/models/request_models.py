from pydantic import BaseModel


class UserRequest(BaseModel):
    id_usuario: int
