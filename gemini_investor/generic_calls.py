from gemini_investor.alpaca_utils import TradingClientSingleton
from datetime import datetime, timedelta
import time

import psutil
import socket


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
    This value calculated on the server and we return the raw value here.
    """
    return f"{TradingClientSingleton.get_instance().get_account().equity}$"


def get_current_date():
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def get_system_info():
    """Returns a string with the system information.
    This includes the container ID, the current date, and the uptime of the container
    """
    # Get the container ID from the hostname
    container_id = socket.gethostname()
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime_string = str(timedelta(seconds = uptime_seconds))

    return f"""Container ID: {container_id}
current date: {get_current_date()}
Uptime: {uptime_string}"""
