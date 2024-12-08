from datetime import datetime
from investor_agent.utils import TradingClientSingleton
from alpaca.data.requests import BaseCryptoLatestDataRequest, CryptoBarsRequest, CryptoQuoteRequest, CryptoTradesRequest, CryptoLatestQuoteRequest, CryptoLatestTradeRequest, CryptoSnapshotRequest
# from alpaca.data import CryptoHistoricalDataClient
# from alpaca.data.requests import (
#     CryptoLatestTradeRequest,
#     CryptoLatestQuoteRequest,
#     CryptoSnapshotRequest
# )

def get_crypto_price(symbol='ETH'):
    '''Find the latest price for the crypto currency'''
    latest_trade_request = BaseCryptoLatestDataRequest(symbol_or_symbols=symbol)

    crypto_order = TradingClientSingleton.get_instance().submit_order(
        order_data=latest_trade_request
    )

    return str(crypto_order)
