"""
Unit tests for ExchangeRateTracker.
Uses unittest.mock to avoid making real API calls during testing.
"""

import pytest
from unittest.mock import patch, Mock
from exchange_tracker import ExchangeRateTracker, ExchangeRateError


@pytest.fixture
def tracker():
    return ExchangeRateTracker()


@pytest.fixture
def mock_rates_response():
    return {
        "base": "USD",
        "rates": {
            "EUR": 0.92,
            "GBP": 0.79,
            "TRY": 32.5
        }
    }


class TestGetRates:
    @patch("exchange_tracker.requests.get")
    def test_get_rates_success(self, mock_get, tracker, mock_rates_response):
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_rates_response)
        rates = tracker.get_rates("USD")
        assert rates["EUR"] == 0.92
        assert mock_get.call_count == 1

    @patch("exchange_tracker.requests.get")
    def test_get_rates_uses_cache(self, mock_get, tracker, mock_rates_response):
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_rates_response)
        tracker.get_rates("USD")
        tracker.get_rates("USD")
        assert mock_get.call_count == 1  # Second call should hit cache

    @patch("exchange_tracker.requests.get")
    def test_get_rates_raises_on_connection_error(self, mock_get, tracker):
        mock_get.side_effect = Exception("Connection failed")
        with pytest.raises(ExchangeRateError):
            tracker.get_rates("USD")


class TestConvert:
    @patch("exchange_tracker.requests.get")
    def test_convert_success(self, mock_get, tracker, mock_rates_response):
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_rates_response)
        result = tracker.convert(100, "USD", "EUR")
        assert result == 92.0

    @patch("exchange_tracker.requests.get")
    def test_convert_invalid_currency_raises(self, mock_get, tracker, mock_rates_response):
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_rates_response)
        with pytest.raises(ExchangeRateError):
            tracker.convert(100, "USD", "XXX")

    def test_convert_negative_amount_raises(self, tracker):
        with pytest.raises(ValueError):
            tracker.convert(-50, "USD", "EUR")


class TestConvertBatch:
    @patch("exchange_tracker.requests.get")
    def test_convert_batch_success(self, mock_get, tracker, mock_rates_response):
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_rates_response)
        results = tracker.convert_batch(100, "USD", ["EUR", "GBP"])
        assert results == {"EUR": 92.0, "GBP": 79.0}
