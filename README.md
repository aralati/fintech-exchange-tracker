# Fintech Exchange Tracker 💱

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Tested with pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A lightweight Python module for real-time currency exchange rate tracking and conversion, built for Fintech use cases. Includes in-memory caching to reduce redundant API calls, a simple CLI for quick conversions, and a full automated test suite.

## ⚙️ Features
- **Real-time rates** — Fetches live exchange rates from a public API
- **In-memory caching** — Avoids redundant API calls within a configurable time window
- **Single & batch conversion** — Convert to one currency or several at once
- **CLI support** — Run conversions directly from the command line
- **Error handling** — Custom exceptions for invalid input and failed API calls
- **Fully tested** — Unit tests using `pytest` and mocked API responses

## 📂 Project Structure
```
fintech-exchange-tracker/
├── exchange_tracker.py
├── requirements.txt
├── tests/
│   └── test_exchange_tracker.py
└── README.md
```


## 🛠️ Quick Start

```bash
git clone https://github.com/aralati/fintech-exchange-tracker.git
cd fintech-exchange-tracker
pip install -r requirements.txt

Run a conversion via CLI:
python exchange_tracker.py 100 USD EUR

Or use it as a module:
from exchange_tracker import ExchangeRateTracker

tracker = ExchangeRateTracker()
result = tracker.convert(100, "USD", "EUR")
print(result)  # e.g. 92.0

# Convert to multiple currencies at once
batch = tracker.convert_batch(100, "USD", ["EUR", "GBP", "TRY"])
print(batch)

🧪 Running Tests

pytest tests/

Tests use mocked API responses, so they run instantly and without network access.

🗺️ Roadmap

	•	Add support for historical exchange rate lookups
	•	Add persistent (disk-based) caching option
	•	Package as a pip-installable module

🧩 Tech Stack

Python Requests Pytest Argparse

📄 License

MIT

👤 Author

Aral Atilla — GitHub
