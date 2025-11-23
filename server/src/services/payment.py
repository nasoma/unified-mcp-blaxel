from decimal import Decimal, InvalidOperation
from typing import List
import re
from config import settings

def parse_payment_amounts(input_str: str) -> List[Decimal]:
    """Parse comma-separated payment amounts with validation."""
    if not input_str or not input_str.strip():
        raise ValueError("Payment amount cannot be empty")

    amounts = []
    for item in input_str.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            amount = Decimal(item)
            if amount < 0:
                raise ValueError(f"Payment amount cannot be negative: {amount}")
            amounts.append(amount)
        except InvalidOperation:
            raise ValueError(f"Invalid payment amount: '{item}'")

    if not amounts:
        raise ValueError("No valid payment amounts found")
    return amounts

def convert_to_kes(input_str: str) -> str:
    """
    Convert Upwork payment amounts from USD to Kenyan Shillings.
    """
    try:
        amounts = parse_payment_amounts(input_str)
        total_usd = sum(amounts)
        after_fee = max(total_usd - settings.UPWORK_FEE, Decimal("0"))
        after_rate = after_fee * settings.UPWORK_RATE
        kes_amount = after_rate * settings.EXCHANGE_RATE

        if len(amounts) > 1:
            amounts_str = " + ".join(f"${float(amt):.2f}" for amt in amounts)
            result = f"Payments: {amounts_str} = ${float(total_usd):.2f} total\n"
        else:
            result = f"Payment: ${float(total_usd):.2f}\n"

        result += f"KES equivalent: {float(kes_amount):.2f} KShs"
        return result

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def extract_number_from_text(text: str) -> Decimal:
    """Extract number from text, handling commas and mixed text/numbers."""
    text = text.lower().strip()
    number_pattern = r"[\d,]+(?:\.\d+)?"
    matches = re.findall(number_pattern, text)

    if not matches:
        raise ValueError("No valid number found in input")

    number_str = max(matches, key=lambda x: len(x.replace(",", "")))
    clean_number = number_str.replace(",", "")
    return Decimal(clean_number)

def calculate_gross_needed(target_kes: str) -> str:
    """
    Calculate gross USD payment needed to receive target KES amount.
    """
    try:
        target = extract_number_from_text(target_kes)
        if target <= 0:
            return "Error: Target KES amount must be positive"

        usd_after_rate = target / settings.EXCHANGE_RATE
        usd_after_fee = usd_after_rate / settings.UPWORK_RATE
        gross_usd_needed = usd_after_fee + settings.UPWORK_FEE

        result = f"To receive {float(target):,.2f} KES:\n"
        result += f"Gross USD payment needed: ${float(gross_usd_needed):.2f}\n"
        result += f"After Upwork processing: {float(target):,.2f} KES"
        return result

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
