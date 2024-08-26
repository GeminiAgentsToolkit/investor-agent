from alpaca.trading.client import TradingClient
from gemini_investor.common import parse_date
import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
import pytz
from alpaca.trading.requests import GetOptionContractsRequest, AssetStatus, MarketOrderRequest, OrderClass, TimeInForce, LimitOrderRequest, StopLossRequest, TakeProfitRequest, OrderSide


# For lazy instantiation
class TradingClientSingleton:
    _instance_prod = None
    _instance_paper = None
    _paper = False

    @classmethod
    def is_paper(cls):
        return cls._paper
    
    @classmethod
    def switch_to_paper_account(cls):
        cls._paper = True
    
    @classmethod
    def switch_to_prod_account(cls):
        cls._paper = False

    @classmethod
    def get_instance(cls):
        if not cls._paper:
            if cls._instance_prod is not None:
                return cls._instance_prod
            else:
                load_dotenv(".env.prod", override=True)
                api_key_id = os.getenv('ALPACA_API_KEY_ID')
                secret_key = os.getenv('ALPACA_SECRET_KEY')
                cls._instance_prod = TradingClient(api_key_id, secret_key, paper=cls._paper)
                return cls._instance_prod
        else:
            if cls._instance_paper is not None:
                return cls._instance_paper
            else:
                load_dotenv(".env.dev", override=True)
                api_key_id = os.getenv('ALPACA_API_KEY_ID')
                secret_key = os.getenv('ALPACA_SECRET_KEY')
                cls._instance_paper = TradingClient(api_key_id, secret_key, paper=cls._paper)
                return cls._instance_paper


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
        expiration_datetime = parse_date(expiration_date)
    except ValueError:
        raise ValueError("Invalid expiration date format: should be YYYY-MM-DD")

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


def submit_sell_market_order(
        symbol: str, 
        qty: float, 
        *,
        time_in_force=TimeInForce.DAY):
    market_order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=time_in_force
    )
    market_order = TradingClientSingleton.get_instance().submit_order(
        order_data=market_order_data
    )
    return str(market_order.id)


def submit_market_order(
        symbol: str, 
        qty: float,
        *,
        time_in_force=TimeInForce.DAY,
        side: str):
    market_order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side,
        time_in_force=time_in_force
    )
    market_order = TradingClientSingleton.get_instance().submit_order(
        order_data=market_order_data
    )
    return str(market_order.id)


def submit_buy_market_order(
        symbol: str, 
        qty: float,
        *,
        time_in_force=TimeInForce.DAY,
        take_profit_price: float,
        stop_loss_price: float):
    market_order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=time_in_force,
        order_class=OrderClass.BRACKET,
        take_profit=TakeProfitRequest(limit_price=take_profit_price),
        stop_loss=StopLossRequest(stop_price=stop_loss_price)
    )
    market_order = TradingClientSingleton.get_instance().submit_order(
        order_data=market_order_data
    )
    return (market_order.id)


def submit_limit_sell_order(
        symbol: str,
        qty: float,
        limit_price: float,
        *,
        time_in_force=TimeInForce.GTC):
    limit_order_data = LimitOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=time_in_force,
        limit_price=limit_price
    )
    order = TradingClientSingleton.get_instance().submit_order(order_data=limit_order_data)
    return str(order.id)


def submit_limit_buy_order(
        symbol: str,
        qty: float,
        limit_price: float,
        *,
        time_in_force=TimeInForce.GTC,
        take_profit_price: float,
        stop_loss_price: float):
    limit_order_data = LimitOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=time_in_force,
        limit_price=limit_price,
        order_class=OrderClass.BRACKET,
        take_profit=TakeProfitRequest(limit_price=take_profit_price),
        stop_loss=StopLossRequest(stop_price=stop_loss_price)
    )
    return str(TradingClientSingleton.get_instance().submit_order(order_data=limit_order_data).id)


def submit_stop_loss_order(
    symbol: str,
    qty: float,
    stop_price: float,
    *,
    time_in_force=TimeInForce.GTC,
):
    """
    Submits a stop-loss order for an existing position.

    Args:
        symbol (str): The symbol of the asset.
        qty (float): The quantity of the asset.
        stop_price (float): The stop price to trigger the order.
        time_in_force (TimeInForce, optional): The time in force for the order. Defaults to TimeInForce.GTC.

    Returns:
        str: The order ID of the submitted stop-loss order.
    """

    stop_loss_order_data = StopLossRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,  # Stop-loss orders are typically sell orders
        time_in_force=time_in_force,
        stop_price=stop_price,
    )

    order = TradingClientSingleton.get_instance().submit_order(order_data=stop_loss_order_data)
    return str(order.id)
