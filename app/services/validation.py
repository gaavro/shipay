from pydantic import BaseModel

class ValidationRequest(BaseModel):
    cnpj: str
    cep: str

class ValidationResponse(BaseModel):
    status: str
    message: str