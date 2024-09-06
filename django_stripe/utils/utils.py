# Standard Library
import decimal
from datetime import datetime


def convert_epoch(epoch):
    """
    Convert epoch to datetime
    """
    return str(datetime.utcfromtimestamp(epoch))


def convert_amount_for_db(amount, currency="usd"):
    # @@@ not sure if this is right;
    # find out what we should do when API returns null for currency
    if currency is None:
        currency = "usd"
    return (
        (amount / decimal.Decimal("100"))
        if currency.lower() not in ZERO_DECIMAL_CURRENCIES
        else decimal.Decimal(amount)
    )


CURRENCY_SYMBOLS = {
    "aud": "\u0024",
    "cad": "\u0024",
    "chf": "\u0043\u0048\u0046",
    "cny": "\u00a5",
    "eur": "\u20ac",
    "gbp": "\u00a3",
    "jpy": "\u00a5",
    "myr": "\u0052\u004d",
    "sgd": "\u0024",
    "usd": "\u0024",
}

# currencies those amount=1 means 100 cents
# https://support.stripe.com/questions/which-zero-decimal-currencies-does-stripe-support
ZERO_DECIMAL_CURRENCIES = [
    "bif",
    "clp",
    "djf",
    "gnf",
    "jpy",
    "kmf",
    "krw",
    "mga",
    "pyg",
    "rwf",
    "vuv",
    "xaf",
    "xof",
    "xpf",
]
