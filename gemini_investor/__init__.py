from gemini_investor.alpaca_utils import TradingClientSingleton
from alpaca.trading.requests import MarketOrderRequest, OrderSide, TimeInForce, OrderType, LimitOrderRequest, OrderClass, GetOrdersRequest, QueryOrderStatus, StopLossRequest
from gemini_investor.options_calls import get_option_contract
from dateutil import parser


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


def get_portfolio():
    """Returns a string with the portfolio of the account.
    """
    positions = TradingClientSingleton.get_instance().get_all_positions()
    return "\n".join([f"{pos.symbol}: {pos.qty}" for pos in positions if pos.qty != 0])


def sell_option_by_market_price_with_option_ticker(option_ticker, qty):
    """
    Sells an option contract at market price.

    Args:
        option_ticker (str): The option contract ticker.
        qty (int): Quantity of the option contract to sell.
    """
    market_order_data = MarketOrderRequest(
        symbol=option_ticker,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
    )
    market_order = TradingClientSingleton.get_instance().submit_order(
        order_data=market_order_data
    )
    return str(market_order.id)


def sell_option_by_market_price(underlying_symbol, expiration_date, option_type, strike_price, qty):
    """
    Sells an option contract at market price.

    Args:
        underlying_symbol (str): The underlying stock symbol (e.g., AAPL).
        expiration_date (str): Expiration date in YYYY-MM-DD format.
        option_type (str): "C" for call, "P" for put.
        strike_price (float): Strike price.
        qty (int): Quantity of the option contract to sell.
    """
    option_contract = get_option_contract(underlying_symbol, option_type, expiration_date, strike_price)
    if not option_contract:
        return "can not sell, since no suitable owned option contract found."
    market_order_data = MarketOrderRequest(
        symbol=option_contract.symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
    )
    market_order = TradingClientSingleton.get_instance().submit_order(
        order_data=market_order_data
    )
    return str(market_order.id)


def set_option_exit_strategy_by_option_ticker(option_ticker, qty, limit_price, stop_loss_price):
    """
    Sets an exit strategy for an owned option contract.

    Args:
        option_ticker (str): The option contract ticker.
        qty (int): Quantity of the option contract to sell.
        limit_price (float): The limit price at which to sell the option contract.
        stop_loss_price (float): The stop loss price at which to sell the option contract.
    """
    # Check if the option contract is in the portfolio (owned)
    positions = TradingClientSingleton.get_instance().get_all_positions()
    owned_option = next((pos for pos in positions if pos.symbol == option_ticker), None)
    if not owned_option or owned_option.qty < qty:
        return f"Not enough {option_ticker} contracts owned to sell."

    limit_order_data = LimitOrderRequest(
        symbol=option_ticker,
        qty=int(qty),
        side=OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
        limit_price=float(limit_price),
        stop_loss=StopLossRequest(stop_price = float(stop_loss_price)),
        order_class=OrderClass.SIMPLE,  
    )
    return str(TradingClientSingleton.get_instance().submit_order(order_data=limit_order_data).id)


def set_option_exit_strategy(underlying_symbol, expiration_date, option_type, strike_price, qty, limit_price, stop_loss_price):
    """
    Sets an exit strategy for an owned option contract.

    Args:
        underlying_symbol (str): The underlying stock symbol (e.g., AAPL).
        expiration_date (str): Expiration date in YYYY-MM-DD format.
        option_type (str): "C" for call, "P" for put.
        strike_price (float): Strike price.
        qty (int): Quantity of the option contract to sell.
        limit_price (float): The limit price at which to sell the option contract.
        stop_loss_price (float): The stop loss price at which to sell the option contract.
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
        qty=int(qty),
        side=OrderSide.SELL,
        time_in_force=TimeInForce.GTC,
        limit_price=float(limit_price),
        stop_loss = StopLossRequest(stop_price = float(stop_loss_price)),
        order_class=OrderClass.SIMPLE,  
    )
    return str(TradingClientSingleton.get_instance().submit_order(order_data=limit_order_data).id)


def get_100_latest_open_orders():
    """Returns a string with the open orders for the account.
    """
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.OPEN,
        limit=100,
        nested=True  # show nested multi-leg orders
    )
    orders = TradingClientSingleton.get_instance().get_orders(filter=get_orders_data)
    return "\n".join([str(order) for order in orders])


def get_closed_orders_in_between_dates(date_from, date_to, limit=30, ticker=None):
    """Returns a string with the closed orders for the account in between the given dates.

    Args:
        date_from (str): The start date in YYYY-MM-DD format.
        date_to (str): The end date in YYYY-MM-DD format.
        limit (int): The maximum number of orders to return.
        ticker (str): The stock symbol to filter the orders.
    """
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        after=parser.parse(date_from).timestamp(),
        until=parser.parse(date_to).timestamp(),
        limit=limit,
        symbols=[ticker] if ticker else None,
        nested=True  # show nested multi-leg orders
    )
    orders = TradingClientSingleton.get_instance().get_orders(filter=get_orders_data)
    return "\n".join([str(order) for order in orders])


def get_last_n_closed_orders(limit=10, ticker=None):
    """Returns a string with the closed orders for the account.

    Args:
        limit (int): The maximum number of orders to return.
        ticker (str): The stock symbol or part of option symbol to filter the orders. This is an optional parameter.
    """
    if ticker:
        limit = 100
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        limit=limit,
        symbols=None,
        nested=True  # show nested multi-leg orders
    )
    orders = TradingClientSingleton.get_instance().get_orders(filter=get_orders_data)
    if ticker:
        # check low casae ticker in lowcase symbol
        orders = [order for order in orders if ticker.lower() in order.symbol.lower()]
    return "\n".join([str(order) for order in orders])

