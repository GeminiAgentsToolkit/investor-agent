from gemini_investor.alpaca_utils import TradingClientSingleton, submit_market_order, submit_limit_order
from alpaca.trading.requests import OrderSide


def buy_stock_by_market_price(symbol: str, qty: float):
    """Buy a stock at market price, retuns the order id. Alpaca allows you to buy shares in parts, not necessarily in whole parts. For example, you can buy/sell 0.5 or 1.8 shares.
    
    Args:
        symbol: The stock symbol to buy.
        qty: The quantity of stock to buy. Mush be a positive integer.
    """
    return submit_market_order(symbol, qty, side=OrderSide.BUY)


def sell_stock_by_market_price(symbol: str, qty: float):
    """Sell a stock at market price, retuns the order id. Alpaca allows you to sell shares in parts, not necessarily in whole parts. For example, you can buy/sell 0.5 or 1.8 shares.
    
    Args:
        symbol: The stock symbol to sell.
        qty: The quantity of stock to sell. Mush be a positive integer.
    """
    return submit_market_order(symbol, qty, side=OrderSide.SELL)


def set_stock_exit_strategy(
        symbol: str,
        qty: float,
        limit_price: float,
        stop_loss_price: float):
    """Set a limit order and a stop loss order to sell a stock.

    Args:
        symbol: The stock symbol to sell.
        qty: The quantity of stock to sell. Mush be a positive float.
        limit_price: The price at which the limit order will be executed.
        stop_loss_price: The price at which the stop loss order will be executed.
    """
    return submit_limit_order(symbol=symbol, qty=qty, limit_price=limit_price, stop_loss_price=stop_loss_price, side=OrderSide.SELL)


def submit_stocks_limit_buy_order(
        symbol: str,
        qty: float,
        limit_price: float):
    """Buy a stock at a specific price, retuns the order id. Alpaca allows you to buy shares in parts, not necessarily in whole parts. For example, you can buy/sell 0.5 or 1.8 shares.

    Args:
        symbol: The stock symbol to buy.
        qty: The quantity of stock to buy. Mush be a positive integer.
        limit_price: The price at which the limit order will be executed.
    """
    return submit_limit_order(symbol=symbol, qty=qty, limit_price=limit_price, side=OrderSide.BUY)
