from alpaca.trading.client import TradingClient
import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
from zoneinfo import ZoneInfo
from alpaca.trading.requests import GetOptionContractsRequest, AssetStatus, MarketOrderRequest, OrderClass, TimeInForce, LimitOrderRequest, StopLossRequest


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
    

def get_option_contract(underlying_symbol, option_type, expiration_date=None, strike_price=None, min_open_interest=0):
    """
    Fetches an option contract matching the given criteria.

    Args:
        underlying_symbol (str): The underlying stock symbol (e.g., AAPL).
        option_type (str): "C" for call, "P" for put.
        expiration_date (str, optional): Expiration date in YYYY-MM-DD format. If None, fetches the nearest expiration.
        strike_price (float, optional): Strike price. If None, fetches the closest to the current underlying price.
        min_open_interest (int, optional): Minimum open interest for the contract.

    Returns:
        alpaca.data.models.OptionContract or None: The matching option contract or None if not found.
    """
    min_open_interest = int(min_open_interest)

    now = datetime.now(tz=ZoneInfo("America/New_York"))
    if option_type.lower() == 'c':
        option_type = 'call'
    elif option_type.lower() == 'p':
        option_type = 'put'
    req = GetOptionContractsRequest(
        underlying_symbols=[underlying_symbol],
        status=AssetStatus.ACTIVE,
        type=option_type.lower(),  # Use lowercase for Alpaca
        expiration_date_gte=now.date() if not expiration_date else expiration_date,
        limit=100,  # Fetch enough to find a good match
    )
    contracts = TradingClientSingleton.get_instance().get_option_contracts(req).option_contracts

    matching_contracts = [c for c in contracts if c.open_interest and int(c.open_interest) >= min_open_interest]

    if expiration_date:
        matching_contracts = [c for c in matching_contracts if c.expiration_date == expiration_date]

    if strike_price:
        matching_contracts = sorted(matching_contracts, key=lambda c: abs(c.strike_price - strike_price))

    return matching_contracts[0] if matching_contracts else None


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
        expiration_datetime = parser.parse(expiration_date)
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


def submit_market_order(
        symbol: str, 
        qty: float, 
        side: str,
        *,
        time_in_force=TimeInForce.DAY):
    market_order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side,
        time_in_force=time_in_force,
    )
    market_order = TradingClientSingleton.get_instance().submit_order(
        order_data=market_order_data
    )
    return market_order.client_order_id


def submit_limit_order(
        symbol: str,
        qty: float,
        limit_price: float,
        *,
        side: str,
        time_in_force=TimeInForce.GTC,
        stop_loss_price=-1.):
    order_class = OrderClass.SIMPLE
    stop_loss = None
    if stop_loss_price > 0:
        order_class = OrderClass.OCO
        stop_loss = StopLossRequest(stop_price=stop_loss_price)
    limit_order_data = LimitOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side,
        time_in_force=time_in_force,
        limit_price=limit_price,
        stop_loss = stop_loss,
        order_class=order_class,  
    )
    return TradingClientSingleton.get_instance().submit_order(order_data=limit_order_data).client_order_id