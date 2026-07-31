"""
Fintech Exchange Tracker
------------------------
A lightweight, real-time currency exchange rate tracker and converter,
with built-in caching to reduce redundant API calls and a simple CLI
for quick conversions.
"""

import argparse
import logging
import time
from dataclasses import dataclass
from typing import Dict, List

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ExchangeRateError(Exception):
    """Raised when exchange rate data cannot be retrieved or is invalid."""


@dataclass
class CacheEntry:
    rates: Dict[str, float]
    timestamp: float


class ExchangeRateTracker:
    """
    Real-time currency exchange rate tracker.

    Rates are cached in memory for `cache_ttl` seconds to avoid
    unnecessary repeated calls to the exchange rate API.
    """

    def __init__(self, base_url: str = "https://api.exchangerate-api.com/v4/latest/", cache_ttl: int = 300):
        self.base_url = base_url
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, CacheEntry] = {}

    def get_rates(self, base_currency: str) -> Dict[str, float]:
        """Fetches exchange rates for a base currency, using cache if fresh."""
        base_currency = base_currency.upper()
        cached = self._cache.get(base_currency)

        if cached and (time.time() - cached.timestamp) < self.cache_ttl:
            logger.info(f"Using cached rates for {base_currency}")
            return cached.rates

        logger.info(f"Fetching fresh rates for {base_currency}...")
        try:
            response = requests.get(f"{self.base_url}{base_currency}", timeout=5)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API connection error: {e}")
            raise ExchangeRateError(f"Could not fetch rates for {base_currency}") from e

        rates = data.get("rates")
        if not rates:
            raise ExchangeRateError(f"No rate data returned for {base_currency}")

        self._cache[base_currency] = CacheEntry(rates=rates, timestamp=time.time())
        return rates

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Converts an amount from one currency to another."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        to_currency = to_currency.upper()
        rates = self.get_rates(from_currency)

        if to_currency not in rates:
            raise ExchangeRateError(f"Unsupported target currency: {to_currency}")

        converted = amount * rates[to_currency]
        logger.info(f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency}")
        return round(converted, 2)

    def convert_batch(self, amount: float, from_currency: str, to_currencies: List[str]) -> Dict[str, float]:
        """Converts a single amount into multiple target currencies at once."""
        rates = self.get_rates(from_currency)
        results = {}
        for currency in to_currencies:
            currency = currency.upper()
            if currency in rates:
                results[currency] = round(amount * rates[currency], 2)
            else:
                logger.warning(f"Skipping unsupported currency: {currency}")
        return results


def main():
    parser = argparse.ArgumentParser(description="Convert currency amounts using live exchange rates.")
    parser.add_argument("amount", type=float, help="Amount to convert")
    parser.add_argument("from_currency", type=str, help="Currency code to convert from (e.g. USD)")
    parser.add_argument("to_currency", type=str, help="Currency code to convert to (e.g. EUR)")
    args = parser.parse_args()

    tracker = ExchangeRateTracker()
    try:
        result = tracker.convert(args.amount, args.from_currency, args.to_currency)
        print(f"{args.amount} {args.from_currency.upper()} = {result} {args.to_currency.upper()}")
    except (ExchangeRateError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
