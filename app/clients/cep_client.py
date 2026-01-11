from clients.http_client import BaseHttpClient
from core.exceptions import ExternalServiceException

class CEPClient:
    PRIMARY_URL = "https://brasilapi.com.br/api/cep/v2"
    SECONDARY_URL = "https://viacep.com.br/ws"

    def __init__(self, http_client: BaseHttpClient):
        self._http = http_client

    async def get_cep(self, cep: str) -> dict:
        resp = await self._http.get_with_retry(f"{self.PRIMARY_URL}/{cep}")
        if resp.status_code == 200:
            return resp.json()

        resp = await self._http.get_with_retry(f"{self.SECONDARY_URL}/{cep}/json/")
        if resp.status_code != 200:
            raise ExternalServiceException("Erro ao consultar CEP")

        return resp.json()
