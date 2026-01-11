import unicodedata
from difflib import SequenceMatcher

SIMILARITY_THRESHOLD = 0.8


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text.lower().strip())
    return "".join(c for c in text if c.isalnum() or c.isspace())


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def addresses_match(cnpj: dict, cep: dict) -> bool:
    uf_cnpj = normalize_text(cnpj.get("uf"))
    uf_cep = normalize_text(cep.get("uf") or cep.get("state"))

    city_cnpj = normalize_text(cnpj.get("municipio"))
    city_cep = normalize_text(cep.get("localidade") or cep.get("city"))

    street_cnpj = normalize_text(cnpj.get("logradouro"))
    street_cep = normalize_text(cep.get("logradouro") or cep.get("street"))

    return (
        uf_cnpj == uf_cep and
        similarity(city_cnpj, city_cep) >= SIMILARITY_THRESHOLD and
        similarity(street_cnpj, street_cep) >= SIMILARITY_THRESHOLD
    )
