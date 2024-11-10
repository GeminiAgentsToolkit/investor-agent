from investor_agent.utils import TradingClientSingleton
from investor_agent.utils import parse_date
from alpaca.trading.requests import GetOrdersRequest, QueryOrderStatus, OrderSide
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


def get_10_latest_open_buy_orders_for_ticker(ticker: str):
    """Returns list of open buy orders for a specific ticker.

    Args:
        ticker: The stock symbol to filter the orders.
    """
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.OPEN,
        limit=10,
        symbols=[ticker] if ticker else None,
        side=OrderSide.BUY,
        nested=True  # show nested multi-leg orders
    )
    orders = TradingClientSingleton.get_instance().get_orders(filter=get_orders_data)
    return "\n".join([str(order) for order in orders])


def get_10_latest_open_sell_orders_for_ticker(ticker: str):
    """Returns a string with the open sell orders for a specific ticker.

    Args:
        ticker: The stock symbol to filter the orders.
    """
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.OPEN,
        limit=10,
        symbols=[ticker] if ticker else None,
        side=OrderSide.SELL,
        nested=True  # show nested multi-leg orders
    )
    orders = TradingClientSingleton.get_instance().get_orders(filter=get_orders_data)
    return "\n".join([str(order) for order in orders])


def get_closed_orders_in_between_dates(date_from: str, date_to: str, limit: int = 30, ticker: str = None):
    """Returns a string with the closed orders for the account in between the given dates.

    Args:
        date_from (str): The start date in YYYY-MM-DD format.
        date_to (str): The end date in YYYY-MM-DD format.
        limit (int): The maximum number of orders to return.
        ticker (str): The stock symbol to filter the orders.
    """
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        after=parse_date(date_from).timestamp(),
        until=parse_date(date_to).timestamp(),
        limit=limit,
        symbols=[ticker] if ticker else None,
        nested=True  # show nested multi-leg orders
    )
    orders = TradingClientSingleton.get_instance().get_orders(filter=get_orders_data)
    return "\n".join([str(order) for order in orders])


def get_last_n_closed_orders(limit: int = 10, ticker: str =None):
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

