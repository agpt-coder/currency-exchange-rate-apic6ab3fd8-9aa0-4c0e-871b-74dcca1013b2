import io
import logging
from contextlib import asynccontextmanager

import prisma
import project.get_exchange_rate_service
import project.update_cache_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, StreamingResponse
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Currency Exchange Rate API",
    lifespan=lifespan,
    description="""To create an endpoint that handles real-time exchange rate data effectively, the application will utilize Python as the programming language, with FastAPI for the API framework due to its performance and ease of asynchronous programming, which is beneficial for real-time data processing. The database of choice will be PostgreSQL, managed through Prisma as the ORM for efficient and straightforward database operations.

The endpoint will be designed to accept both a base currency and one or multiple target currencies as parameters. Utilizing the preferred real-time exchange rate data source, the 'Forex Open Exchange Rates' API, the application will retrieve the latest exchange rates efficiently. Implementing best practices for secure external API calls, such as using HTTPS for encrypted data transmission, managing sensitive information like API keys securely, and validating the SSL certificates, will ensure data integrity and security.

The endpoint will calculate the exchange rate between the specified base and target currencies by fetching the latest rates from the Forex API. To accommodate the requirement for multiple target currencies, the logic will include processing multiple rates in a single request when possible, leveraging the Forex API’s ability to handle multiple currencies. The results will include the calculated exchange rates along with a timestamp of the data retrieval, ensuring users have access to the timeliness of the information.

Care will be taken to implement caching strategies to minimize direct API calls, thus optimizing performance and managing API rate limits effectively. Fallback mechanisms will also be in place to handle potential API failures, ensuring continuous functionality of the endpoint.

In summary, the endpoint will provide a robust, secure, and efficient way to retrieve and calculate real-time exchange rates for given base and target currencies, incorporating user feedback and technical best practices for a high-quality user experience.""",
)


@app.patch(
    "/cache/update", response_model=project.update_cache_service.UpdateCacheResponse
)
async def api_patch_update_cache(
    base_currency: str, target_currency: str, rate: float, ttl: Optional[int]
) -> project.update_cache_service.UpdateCacheResponse | Response:
    """
    Updates the cache with the latest data from the Forex API or as per the TTL configuration.
    """
    try:
        res = await project.update_cache_service.update_cache(
            base_currency, target_currency, rate, ttl
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/exchange-rate/{base_currency}/{target_currency}",
    response_model=project.get_exchange_rate_service.ExchangeRateResponse,
)
async def api_get_get_exchange_rate(
    base_currency: str, target_currency: str
) -> project.get_exchange_rate_service.ExchangeRateResponse | Response:
    """
    Retrieves the latest exchange rate data for specified base and target currencies.
    """
    try:
        res = await project.get_exchange_rate_service.get_exchange_rate(
            base_currency, target_currency
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
