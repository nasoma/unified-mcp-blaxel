from decimal import Decimal

import pytest

from config import settings
from services import payment


@pytest.fixture(autouse=True)
def fixed_rates(monkeypatch):
    monkeypatch.setattr(settings, "EXCHANGE_RATE", Decimal("129.0"))
    monkeypatch.setattr(settings, "UPWORK_FEE", Decimal("0.99"))
    monkeypatch.setattr(settings, "UPWORK_RATE", Decimal("0.884"))


def test_parse_payment_amounts():
    assert payment.parse_payment_amounts("10, 20.5,") == [Decimal("10"), Decimal("20.5")]


@pytest.mark.parametrize("raw", ["", "   ", ",", "abc", "-5"])
def test_parse_payment_amounts_rejects_invalid(raw):
    with pytest.raises(ValueError):
        payment.parse_payment_amounts(raw)


def test_convert_to_kes_single():
    # (100 - 0.99) * 0.884 * 129 = 11290.70
    assert payment.convert_to_kes("100") == "Payment: $100.00\nKES equivalent: 11290.70 KShs"


def test_convert_to_kes_multiple():
    result = payment.convert_to_kes("50, 50")
    assert result.startswith("Payments: $50.00 + $50.00 = $100.00 total")
    assert result.endswith("11290.70 KShs")


def test_convert_to_kes_invalid_input():
    assert payment.convert_to_kes("abc") == "Error: Invalid payment amount: 'abc'"


@pytest.mark.parametrize("text", ["9000", "9,000", "I need 9,000"])
def test_extract_number_from_text(text):
    assert payment.extract_number_from_text(text) == Decimal("9000")


def test_calculate_gross_needed_round_trips_with_convert():
    result = payment.calculate_gross_needed("11290.70")
    assert "Gross USD payment needed: $100.00" in result


def test_calculate_gross_needed_rejects_zero_and_missing_numbers():
    assert payment.calculate_gross_needed("0") == "Error: Target KES amount must be positive"
    assert payment.calculate_gross_needed("nothing here") == "Error: No valid number found in input"
