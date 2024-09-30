import yfinance as yf
import pandas as pd

"""
RSI:
Buy: RSI < 30
Sell: RSI > 70
MACD:
Buy: MACD crosses above the signal line.
Sell: MACD crosses below the signal line.
Stochastic Oscillator:
Buy: %K < 20 (oversold).
Sell: %K > 80 (overbought).
ATR (Average True Range):
ATR doesn’t provide direct buy/sell signals but indicates volatility. A high ATR suggests high volatility.
"""


# RSI Calculation
def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI) for the given stock data.

    Args:
        data (pd.DataFrame): Stock data containing 'Close' prices.
        period (int, optional): Lookback period for RSI calculation. Defaults to 14.

    Returns:
        pd.Series: RSI values for the given stock data.
    """
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# MACD Calculation
def calculate_macd(data: pd.DataFrame, short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> tuple[pd.Series, pd.Series]:
    """
    Calculate the Moving Average Convergence Divergence (MACD) and the signal line.

    Args:
        data (pd.DataFrame): Stock data containing 'Close' prices.
        short_window (int, optional): Short-term EMA period. Defaults to 12.
        long_window (int, optional): Long-term EMA period. Defaults to 26.
        signal_window (int, optional): Signal line EMA period. Defaults to 9.

    Returns:
        tuple[pd.Series, pd.Series]: Tuple containing MACD values and signal line values.
    """
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()

    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_window, adjust=False).mean()

    return macd, signal_line

# Stochastic Oscillator Calculation
def calculate_stochastic(data: pd.DataFrame, period: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> tuple[pd.Series, pd.Series]:
    """
    Calculate the Stochastic Oscillator values (%K and %D).

    Args:
        data (pd.DataFrame): Stock data containing 'High', 'Low', and 'Close' prices.
        period (int, optional): Lookback period for %K calculation. Defaults to 14.
        smooth_k (int, optional): Smoothing period for %K. Defaults to 3.
        smooth_d (int, optional): Smoothing period for %D. Defaults to 3.

    Returns:
        tuple[pd.Series, pd.Series]: Tuple containing %K and %D values.
    """
    low_min = data['Low'].rolling(window=period).min()
    high_max = data['High'].rolling(window=period).max()

    stochastic_k = 100 * (data['Close'] - low_min) / (high_max - low_min)
    stochastic_d = stochastic_k.rolling(window=smooth_d).mean()

    return stochastic_k, stochastic_d

# ATR Calculation
def calculate_atr(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate the Average True Range (ATR), a volatility indicator.

    Args:
        data (pd.DataFrame): Stock data containing 'High', 'Low', and 'Close' prices.
        period (int, optional): Lookback period for ATR calculation. Defaults to 14.

    Returns:
        pd.Series: ATR values for the given stock data.
    """
    high_low = data['High'] - data['Low']
    high_close = (data['High'] - data['Close'].shift()).abs()
    low_close = (data['Low'] - data['Close'].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()

    return atr

# Stock Data Fetching
def get_stock_data(ticker: str, period: str = '3mo', interval: str = '1d') -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        period (str, optional): Time period to fetch data for (e.g., '1mo', '3mo'). Defaults to '3mo'.
        interval (str, optional): Data interval (e.g., '1d', '1h'). Defaults to '1d'.

    Returns:
        pd.DataFrame: Historical stock data.
    """
    stock_data = yf.download(ticker, period=period, interval=interval)
    return stock_data

# Signal Check for RSI
def check_rsi_signal(rsi: pd.Series) -> str:
    """
    Check the RSI buy/sell signal based on RSI values.

    Args:
        rsi (pd.Series): RSI values.

    Returns:
        str: Buy, sell, or no signal based on RSI.
    """
    if rsi.iloc[-1] > 70:
        return "RSI Signal: Sell (Overbought)"
    elif rsi.iloc[-1] < 30:
        return "RSI Signal: Buy (Oversold)"
    else:
        return "RSI Signal: No clear signal"

# Signal Check for MACD
def check_macd_signal(macd: pd.Series, signal_line: pd.Series) -> str:
    """
    Check the MACD buy/sell signal based on MACD and signal line values.

    Args:
        macd (pd.Series): MACD values.
        signal_line (pd.Series): Signal line values.

    Returns:
        str: Buy, sell, or no signal based on MACD.
    """
    if macd.iloc[-1] > signal_line.iloc[-1] and macd.iloc[-2] < signal_line.iloc[-2]:
        return "MACD Signal: Buy"
    elif macd.iloc[-1] < signal_line.iloc[-1] and macd.iloc[-2] > signal_line.iloc[-2]:
        return "MACD Signal: Sell"
    else:
        return "MACD Signal: No clear signal"

# Signal Check for Stochastic Oscillator
def check_stochastic_signal(stochastic_k: pd.Series, stochastic_d: pd.Series) -> str:
    """
    Check the Stochastic Oscillator buy/sell signal based on %K and %D values.

    Args:
        stochastic_k (pd.Series): %K values.
        stochastic_d (pd.Series): %D values.

    Returns:
        str: Buy, sell, or no signal based on the Stochastic Oscillator.
    """
    if stochastic_k.iloc[-1] > 80:
        return "Stochastic Oscillator: Sell (Overbought)"
    elif stochastic_k.iloc[-1] < 20:
        return "Stochastic Oscillator: Buy (Oversold)"
    else:
        return "Stochastic Oscillator: No clear signal"

# Signal Check for ATR
def check_atr_signal(atr: pd.Series) -> str:
    """
    Check the ATR value to indicate volatility.

    Args:
        atr (pd.Series): ATR values.

    Returns:
        str: A message about the ATR value indicating volatility.
    """
    return f"ATR (Average True Range) Value: {atr.iloc[-1]:.2f} (High ATR implies high volatility)"

# Main function
def analyze_stock(ticker: str) -> None:
    """
    Analyze stock data for a given ticker and print buy/sell signals based on RSI, MACD, Stochastic Oscillator, and ATR.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
        None
    """
    data = get_stock_data(ticker)

    # Calculate indicators
    rsi = calculate_rsi(data)
    macd, signal_line = calculate_macd(data)
    stochastic_k, stochastic_d = calculate_stochastic(data)
    atr = calculate_atr(data)

    # Get individual signals
    rsi_signal = check_rsi_signal(rsi)
    macd_signal = check_macd_signal(macd, signal_line)
    stochastic_signal = check_stochastic_signal(stochastic_k, stochastic_d)
    atr_signal = check_atr_signal(atr)

    # Print signals
    print(f"Stock: {ticker}")
    print(rsi_signal)
    print(macd_signal)
    print(stochastic_signal)
    print(atr_signal)

# Example usage
analyze_stock("MSFT")  # You can replace 'MSFT' with any stock ticker
