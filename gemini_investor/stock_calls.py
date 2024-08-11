from gemini_investor.alpaca_utils import submit_limit_buy_order, submit_limit_sell_order, submit_sell_market_order, submit_buy_market_order
from alpaca.trading.requests import TimeInForce


def buy_stock_by_market_price(symbol: str, qty: float, take_profit_price: float, stop_loss_price: float):
    """Buy a stock at market price, retuns the order id. Alpaca allows you to buy shares in parts, not necessarily in whole parts. For example, you can buy/sell 0.5 or 1.8 shares.
    This also sets a take profit and stop loss order. This is enforced, so you can NOT buy stocks without setting a take profit and stop loss order (exit strategy).
    
    Args:
        symbol: The stock symbol to buy.
        qty: The quantity of stock to buy. Mush be a positive integer.
        take_profit_price: The price at which the take profit order will be executed.
        stop_loss_price: The price at which the stop loss order will be executed.
    """
    return submit_buy_market_order(symbol, qty,
        time_in_force=TimeInForce.GTC,
        take_profit_price=take_profit_price,
        stop_loss_price=stop_loss_price)


def sell_stock_by_market_price(symbol: str, qty: float):
    """Sell a stock at market price, retuns the order id. Alpaca allows you to sell shares in parts, not necessarily in whole parts. For example, you can buy/sell 0.5 or 1.8 shares.
    
    Args:
        symbol: The stock symbol to sell.
        qty: The quantity of stock to sell. Mush be a positive integer.
    """
    return submit_sell_market_order(symbol, qty)


def submit_stocks_limit_buy_order(
        symbol: str,
        qty: float,
        limit_price: float,
        take_profit_price: float,
        stop_loss_price: float):
    """Buy a stock at a specific price, retuns the order id. Alpaca allows you to buy shares in parts, not necessarily in whole parts. For example, you can buy/sell 0.5 or 1.8 shares.

    Args:
        symbol: The stock symbol to buy.
        qty: The quantity of stock to buy. Mush be a positive integer.
        limit_price: The price at which the limit order will be executed.
        take_profit_price: The price at which the take profit order will be executed.
        stop_loss_price: The price at which the stop loss order will be executed.
    """
    return submit_limit_buy_order(symbol=symbol, qty=qty, limit_price=limit_price, take_profit_price=take_profit_price, stop_loss_price=stop_loss_price)


def submit_stocks_limit_sell_order(
        symbol: str,
        qty: float,
        limit_price: float):
    """Sell a stock at a specific price, retuns the order id. Alpaca allows you to sell shares in parts, not necessarily in whole parts. For example, you can buy/sell 0.5 or 1.8 shares.

    Args:
        symbol: The stock symbol to sell.
        qty: The quantity of stock to sell. Mush be a positive integer.
        limit_price: The price at which the limit order will be executed.
    """
    return submit_limit_sell_order(symbol=symbol, qty=qty, 
        limit_price=limit_price)
