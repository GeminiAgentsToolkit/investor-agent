from gemini_investor.alpaca_utils import TradingClientSingleton
from alpaca.trading.requests import MarketOrderRequest, OrderSide, TimeInForce, OrderType, LimitOrderRequest, OrderClass, GetOrdersRequest, QueryOrderStatus
from gemini_investor.alpaca_utils import create_option_ticker, get_option_contract


def check_if_trading_is_blocked():
    """Check if trading is blocked for the account"""
    return f"{TradingClientSingleton.get_instance().get_account().trading_blocked}"


def get_account_buying_power():
    """Returns a string with the number of dollars as the purchasing power of the accountant.
    Current available cash buying power. If multiplier = 2 then buying_power = max(equity-initial_margin(0) * 2).
    If multiplier = 1 then buying_power = cash."""
    return f"{TradingClientSingleton.get_instance().get_account().buying_power}$"


def get_non_marginable_buying_power():
    """Returns a string with the number of dollars as the non marginable buying power for the account."""
    return f"{TradingClientSingleton.get_instance().get_account().non_marginable_buying_power}$"


def get_account_equity_value():
    """Returns a string with the numbers of dollars that tell us the account equity.
    This value is cash + long_market_value + short_market_value.
    This value isn’t calculated in the SDK it is computed on the server and we return the raw value here.
    """
    return f"{TradingClientSingleton.get_instance().get_account().equity}$"


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
    market_order_data = MarketOrderRequest(
        symbol=option_ticker,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
        type=OrderType.MARKET,
    )
    market_order = TradingClientSingleton.get_instance().submit_order(
        order_data=market_order_data
    )
    return market_order.client_order_id


def get_order_by_id(order_id: str):
    """Returns a string with the order details for the given order id.
    
    Args:
        order_id: The id of the order to get.
    """
    order = TradingClientSingleton.get_instance().get_order_by_id(order_id=order_id)
    return str(order)


def cancel_order_by_id(order_id: str):
    """Remove/cancels an order by its id.
    
    Args:
        order_id: The id of the order to remove.
    """
    TradingClientSingleton.get_instance().cancel_order_by_id(order_id=order_id)


def buy_stock_by_market_price(symbol: str, qty: int):
    """Buy a stock at market price, retuns the order id.
    
    Args:
        symbol: The stock symbol to buy.
        qty: The quantity of stock to buy. Mush be a positive integer.
    """
    market_order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
    )
    market_order = TradingClientSingleton.get_instance().submit_order(
        order_data=market_order_data
    )
    return market_order.client_order_id


def sell_stock_by_market_price(symbol: str, qty: int):
    """Sell a stock at market price, retuns the order id.
    
    Args:
        symbol: The stock symbol to sell.
        qty: The quantity of stock to sell. Mush be a positive integer.
    """
    market_order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
    )
    market_order = TradingClientSingleton.get_instance().submit_order(
        order_data=market_order_data
    )
    return market_order.client_order_id


def get_portfolio():
    """Returns a string with the portfolio of the account.
    """
    positions = TradingClientSingleton.get_instance().get_all_positions()
    return "\n".join([f"{pos.symbol}: {pos.qty}" for pos in positions if pos.qty != 0])


def buy_option_by_limit_price(underlying_symbol, expiration_date, option_type, strike_price, qty, limit_price):
    """
    Buys an option contract at a specified limit price.

    Args:
        underlying_symbol (str): The underlying stock symbol (e.g., AAPL).
        expiration_date (str): Expiration date in YYYY-MM-DD format.
        option_type (str): "C" for call, "P" for put.
        strike_price (float): Strike price.
        qty (int): Quantity of the option contract to buy.
        limit_price (float): The limit price at which to buy the option contract.
    """
    option_contract = get_option_contract(underlying_symbol, option_type, expiration_date, strike_price)
    if not option_contract:
        return "No suitable option contract found."
    
    limit_order_data = LimitOrderRequest(
        symbol=option_contract.symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
        limit_price=limit_price,
        order_class=OrderClass.SIMPLE,  # For basic options orders
    )
    return TradingClientSingleton.get_instance().submit_order(order_data=limit_order_data).client_order_id


def sell_option_by_limit_price(underlying_symbol, expiration_date, option_type, strike_price, qty, limit_price):
    """
    Sells an option contract at a specified limit price.

    Args:
        underlying_symbol (str): The underlying stock symbol (e.g., AAPL).
        expiration_date (str): Expiration date in YYYY-MM-DD format.
        option_type (str): "C" for call, "P" for put.
        strike_price (float): Strike price.
        qty (int): Quantity of the option contract to sell.
        limit_price (float): The limit price at which to sell the option contract.
    """
    option_contract = get_option_contract(underlying_symbol, option_type, expiration_date, strike_price)
    if not option_contract:
        return "can not sell, since no suitable owned option contract found."
    
    # Check if the option contract is in the portfolio (owned)
    positions = TradingClientSingleton.get_instance().get_all_positions()
    owned_option = next((pos for pos in positions if pos.symbol == option_contract.symbol), None)
    if not owned_option or owned_option.qty < qty:
        return f"Not enough {option_contract.symbol} contracts owned to sell."

    limit_order_data = LimitOrderRequest(
        symbol=option_contract.symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
        limit_price=limit_price,
        order_class=OrderClass.SIMPLE,  # For basic options orders
    )
    return TradingClientSingleton.get_instance().submit_order(order_data=limit_order_data).client_order_id


def get_open_orders():
    """Returns a string with the open orders for the account.
    """
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.OPEN,
        limit=100,
        nested=True  # show nested multi-leg orders
    )
    orders = TradingClientSingleton.get_instance().get_orders(filter=get_orders_data)
    return "\n".join([str(order) for order in orders])


def get_closed_orders():
    """Returns a string with the closed orders for the account.
    """
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        limit=100,
        nested=True  # show nested multi-leg orders
    )
    orders = TradingClientSingleton.get_instance().get_orders(filter=get_orders_data)
    return "\n".join([str(order) for order in orders])

