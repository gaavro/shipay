import asyncio
import os
import httpx

RETRIES = int(os.getenv("HTTP_RETRIES", 3))
TIMEOUT = float(os.getenv("HTTP_TIMEOUT", 10))

class BaseHttpClient:
    def __init__(
        self,
        timeout: float = TIMEOUT,
        retries: int = RETRIES,
        backoff: float = 0.2,
    ):
        self._client = httpx.AsyncClient(timeout=timeout)
        self._retries = retries
        self._backoff = backoff

    async def get_with_retry(self, url: str):
        for attempt in range(self._retries):
            try:
                resp = await self._client.get(url)
                if resp.status_code >= 500:
                    raise httpx.HTTPStatusError("Server error", request=resp.request, response=resp)
                return resp
            except (httpx.TimeoutException, httpx.TransportError, httpx.HTTPStatusError):
                if attempt == self._retries - 1:
                    raise
                await asyncio.sleep(self._backoff * (2 ** attempt))


    async def close(self):
        await self._client.aclose()
