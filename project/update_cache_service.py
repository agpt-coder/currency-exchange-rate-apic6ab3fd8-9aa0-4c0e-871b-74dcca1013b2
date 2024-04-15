from datetime import datetime, timedelta
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateCacheResponse(BaseModel):
    """
    Confirms the successful update of the cache. Includes a status message and, optionally, the timestamp of the update for verification.
    """

    status: str
    updated_at: Optional[datetime] = None


async def update_cache(
    base_currency: str, target_currency: str, rate: float, ttl: Optional[int] = None
) -> UpdateCacheResponse:
    """
    Updates the cache with the latest data from the Forex API or as per the TTL configuration.

    Args:
    base_currency (str): The base currency code for the exchange rate.
    target_currency (str): The target currency code for which the exchange rate is applicable.
    rate (float): The latest exchange rate between the base and target currency.
    ttl (Optional[int]): The time-to-live (TTL) for the cached rate. This is an optional field that dictates how long this cached entry remains valid, in seconds.

    Returns:
    UpdateCacheResponse: Confirms the successful update of the cache. Includes a status message and, optionally, the timestamp of the update for verification.
    """
    now = datetime.now()
    valid_until = now + timedelta(seconds=ttl) if ttl else now + timedelta(hours=1)
    existing_entry = await prisma.models.CachedRate.prisma().find_unique(
        where={
            "baseCurrency_targetCurrency": {
                "baseCurrency": base_currency,
                "targetCurrency": target_currency,
            }
        }
    )
    if existing_entry:
        await prisma.models.CachedRate.prisma().update(
            where={"id": existing_entry.id},
            data={"rate": rate, "validUntil": valid_until},
        )
    else:
        await prisma.models.CachedRate.prisma().create(
            data={
                "baseCurrency": base_currency,
                "targetCurrency": target_currency,
                "rate": rate,
                "validUntil": valid_until,
            }
        )
    return UpdateCacheResponse(status="Cache updated successfully.", updated_at=now)
