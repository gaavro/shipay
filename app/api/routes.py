from clients.cep_client import CEPClient
from clients.cnpj_client import CNPJClient
from clients.http_client import BaseHttpClient
from schemas.validation import ValidationService
from fastapi import APIRouter, HTTPException
from services.validation import ValidationRequest, ValidationResponse
from core.exceptions import AddressMismatchException

router = APIRouter()

http_client = BaseHttpClient()
validation_service = ValidationService(
    cnpj_client=CNPJClient(http_client),
    cep_client=CEPClient(http_client),
)

@router.post("/validate", response_model=ValidationResponse)
async def validate(data: ValidationRequest):
    try:
        await validation_service.validate_cnpj_cep(data.cnpj, data.cep)
        return ValidationResponse(
            status="success",
            message="Endereços correspondem"
        )
    except AddressMismatchException:
        raise HTTPException(status_code=404, detail="Endereços não correspondem")