from datetime import datetime
from typing import Dict

import httpx
from pydantic import BaseModel


class ExchangeRateResponse(BaseModel):
    """
    This model represents the response returned to the user, containing the exchange rate(s) for the requested currency pair(s) along with a timestamp marking the data retrieval time.
    """

    base_currency: str
    rates: Dict[str, float]
    timestamp: datetime


async def fetch_rates_from_api(base_currency: str, target_currency: str) -> Dict:
    """
    Fetches the exchange rates for the specified base and target currencies from the Forex Open Exchange Rates API.

    Args:
        base_currency (str): The base currency code.
        target_currency (str): The target currency or currencies codes (comma-separated for multiple currencies).

    Returns:
        Dict: A dictionary containing the exchange rates and the timestamp.
    """
    url = f"https://open.exchangerate-api.com/v6/latest?base={base_currency}&symbols={target_currency}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
    rates = {
        key: value
        for key, value in data["rates"].items()
        if key in target_currency.split(",")
    }
    timestamp = datetime.fromtimestamp(data["timestamp"])
    return {"rates": rates, "timestamp": timestamp}


async def get_exchange_rate(
    base_currency: str, target_currency: str
) -> ExchangeRateResponse:
    """
    Retrieves the latest exchange rate data for specified base and target currencies.

    Args:
        base_currency (str): The base currency code for which the exchange rate is being requested.
        target_currency (str): The target currency or currencies codes to convert the base currency into. Can be a single code or a comma-separated list of codes for multiple currencies.

    Returns:
        ExchangeRateResponse: This model represents the response returned to the user, containing the exchange rate(s) for the requested currency pair(s) along with a timestamp marking the data retrieval time.
    """
    rates_data = await fetch_rates_from_api(base_currency, target_currency)
    return ExchangeRateResponse(
        base_currency=base_currency,
        rates=rates_data["rates"],
        timestamp=rates_data["timestamp"],
    )
