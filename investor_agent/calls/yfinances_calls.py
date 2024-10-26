import yfinance as yf


def get_stock_price(stock_ticker: str):
    """Returns the current price of the given stock ticker.
    
    Args:
        stock_ticker: The stock ticker to get the price.
    """
    stock = yf.Ticker(stock_ticker)
    price = None
    if 'currentPrice' in stock.info:
        price = stock.info['currentPrice']
    else:
        price = stock.info['ask']
    return price
