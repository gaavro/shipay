import asyncio
from clients.cnpj_client import CNPJClient
from clients.cep_client import CEPClient
from core.utils import addresses_match
from core.exceptions import AddressMismatchException

class ValidationService:
    def __init__(self, cnpj_client: CNPJClient, cep_client: CEPClient):
        self._cnpj_client = cnpj_client
        self._cep_client = cep_client

    async def validate_cnpj_cep(self, cnpj: str, cep: str) -> None:
        cnpj_data, cep_data = await asyncio.gather(
            self._cnpj_client.get_cnpj(cnpj),
            self._cep_client.get_cep(cep)
        )

        if not addresses_match(cnpj_data, cep_data):
            raise AddressMismatchException()
