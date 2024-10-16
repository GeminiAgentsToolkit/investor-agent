from tabulate import tabulate
from investor_agent.utils import TradingClientSingleton

def get_portfolio_value():
    """
    Returns the current total market value of the portfolio.
    This is the sum of the value of all positions in the portfolio.
    """
    positions = TradingClientSingleton.get_instance().get_all_positions()
    positions = [pos for pos in positions if pos.qty != 0]

    total_market_value = 0.0
    for pos in positions:
        total_market_value += float(pos.market_value)

    return total_market_value

def get_portfolio():
    """Returns a formatted table representing the portfolio of the account."""

    positions = TradingClientSingleton.get_instance().get_all_positions()
    positions = [pos for pos in positions if pos.qty != 0]

    # Prepare data for the table
    data = []
    total_cost_basis = 0.0

    for pos in positions:
        market_value = float(pos.market_value)
        cost_basis = float(pos.cost_basis)
        pl_percentage = (market_value - cost_basis) / cost_basis * 100 if cost_basis != 0 else 0.0

        data.append({
            "Tkr": pos.symbol,
            "Q": pos.qty,
            "cuP": f"{float(pos.current_price):.2f}",
            "mVal": f"{market_value:.2f}",
            "%": f"{pl_percentage:.2f}%"
        })

        total_cost_basis += cost_basis

    # If there are no positions, return a simple message
    if not data:
        return "No open positions in your portfolio."

    # Calculate Total P/L (%)
    total_market_value = get_portfolio_value()
    total_pl_percentage = (total_market_value - total_cost_basis) / total_cost_basis * 100 if total_cost_basis != 0 else 0.0

    # Adding row with "Total"
    data.append({
        "Tkr": "Total",
        "Q": "",
        "cuP": "",
        "mVal": f"{total_market_value:.2f}",
        "%": f"{total_pl_percentage:.2f}%"
    })

    # Form a table using tabulate
    table = tabulate(
        data,
        headers="keys",
        tablefmt="plain",
        floatfmt=".2f",
        colalign=("left", "right", "right", "right", "right")
    )

    # Wrap the table for Telegram
    return f"{table}"
