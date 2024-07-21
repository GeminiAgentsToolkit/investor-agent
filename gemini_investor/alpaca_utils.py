from alpaca.trading.client import TradingClient
import os
from dotenv import load_dotenv


# For lazy instantiation
class TradingClientSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            load_dotenv()  # You can set a path to the .env file
            api_key_id = os.getenv('ALPACA_API_KEY_ID')
            secret_key = os.getenv('ALPACA_SECRET_KEY')
            cls._instance = TradingClient(api_key_id, secret_key, paper=False)
        return cls._instance
    

def create_option_ticker(
    underlying_symbol: str,
    expiration_date: str,
    option_type: str,
    strike_price: float,
):
    """
    Creates an option ticker in the format AAPL231201C00195000
    Validates the input arguments for format and logic.
    """
    # --- Validate Underlying Symbol ---
    if not underlying_symbol.isalpha() or len(underlying_symbol) > 5:
        raise ValueError("Invalid underlying symbol: should be 1-5 alphabetic characters")

    # --- Validate Expiration Date ---
    try:
        expiration_datetime = datetime.strptime(expiration_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid expiration date format: should be YYYY-MM-DD")
    if expiration_datetime < datetime.now():
        raise ValueError("Expiration date cannot be in the past")

    # --- Validate Option Type ---
    if option_type.upper() not in ("C", "P"):
        raise ValueError("Invalid option type: should be 'C' (Call) or 'P' (Put)")

    # --- Validate Strike Price ---
    if strike_price <= 0 or not isinstance(strike_price, (int, float)):
        raise ValueError("Invalid strike price: should be a positive number")

    # --- Format Expiration Date ---
    expiration_str = expiration_datetime.strftime("%y%m%d")

    # --- Format Strike Price ---
    strike_str = f"{int(strike_price * 1000):08}" 

    # --- Create Ticker ---
    ticker = f"{underlying_symbol}{expiration_str}{option_type.upper()}{strike_str}"

    return ticker
