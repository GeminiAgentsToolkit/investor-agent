from gemini_investor.alpaca_utils import TradingClientSingleton, submit_buy_market_order, create_option_ticker, submit_limit_buy_order, submit_market_order
from alpaca.trading.requests import OrderSide, TimeInForce


def buy_option_by_market_price(
        underlying_symbol: str,
        expiration_date: str,
        option_type: str,
        strike_price: float,
        qty: int):
    """Buy an option at market price, retuns the order id.

    Args:
        underlying_symbol: The underlying symbol of the option.
        expiration_date: The expiration date of the option.
        option_type: The type of the option. Should be 'C' (Call) or 'P' (Put).
        strike_price: The strike price of the option.
        qty: The quantity of the option to buy. Mush be a positive integer. You MUST provide it, even if qty is 1.
    """
    strike_price = float(strike_price)
    qty = int(qty)
    option_ticker = create_option_ticker(
        underlying_symbol=underlying_symbol,
        expiration_date=expiration_date,
        option_type=option_type,
        strike_price=strike_price,
    )
    return submit_market_order(option_ticker, qty, time_in_force=TimeInForce.DAY, side=OrderSide.BUY)
