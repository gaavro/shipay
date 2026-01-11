from clients.http_client import BaseHttpClient
from core.exceptions import ExternalServiceException

class CNPJClient:
    BASE_URL = "https://brasilapi.com.br/api/cnpj/v1"

    def __init__(self, http_client: BaseHttpClient):
        self._http = http_client

    async def get_cnpj(self, cnpj: str) -> dict:
        resp = await self._http.get_with_retry(f"{self.BASE_URL}/{cnpj}")
        if resp.status_code != 200:
            raise ExternalServiceException("Erro ao consultar CNPJ")
        return resp.json()
