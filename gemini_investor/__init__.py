from gemini_investor.alpaca_utils import TradingClientSingleton
from alpaca.trading.requests import MarketOrderRequest, OrderSide, TimeInForce, OrderType, LimitOrderRequest, OrderClass, GetOrdersRequest, QueryOrderStatus, StopLossRequest
from gemini_investor.options_calls import get_option_contract
from dateutil import parser


def get_portfolio():
    """Returns a string with the portfolio of the account.
    """
    positions = TradingClientSingleton.get_instance().get_all_positions()
    return "\n".join([f"{pos.symbol}: {pos.qty}" for pos in positions if pos.qty != 0])

