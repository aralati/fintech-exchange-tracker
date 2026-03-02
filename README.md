# fintech-exchange-tracker
A Python-based real-time currency exchange rate tracker and conversion module designed for Fintech applications.
requests==2.31.0
python-dotenv==1.0.0
import requests
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExchangeRateTracker:
    """
    Real-time currency exchange rate tracker for Fintech applications.
    """
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"

    def get_rates(self, base_currency: str = "USD") -> Optional[Dict]:
        """Fetches current exchange rates for the given base currency."""
        try:
            logging.info(f"Fetching current rates for {base_currency}...")
            response = requests.get(f"{self.base_url}{base_currency}")
            response.raise_for_status()
            data = response.json()
            return data.get("rates")
        except requests.exceptions.RequestException as e:
            logging.error(f"API Connection Error: {e}")
            return None

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Converts an amount from one currency to another."""
        rates = self.get_rates(from_currency)
        if rates and to_currency in rates:
            converted_amount = amount * rates[to_currency]
            logging.info(f"Success: {amount} {from_currency} = {converted_amount:.2f} {to_currency}")
            return converted_amount
        else:
            logging.warning("Invalid currency or rate not found.")
            return 0.0

if __name__ == "__main__":
    tracker = ExchangeRateTracker()
    tracker.convert_currency(2500.0, "USD", "EUR")


