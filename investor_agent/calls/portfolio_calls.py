
from tabulate import tabulate
from investor_agent.utils import TradingClientSingleton
from investor_agent.options_calls import get_option_contract


def get_portfolio():
    """Returns a formatted table representing the portfolio of the account."""

    positions = TradingClientSingleton.get_instance().get_all_positions()

    # Filter out positions with zero quantity and prepare data for the table
    data = [
        {
            "Symbol": pos.symbol,
            "Quantity": pos.qty,
            "Cost Basis": pos.cost_basis,
            "Unrealized P/L (%)": f"{round(float(pos.unrealized_plpc), 2) if pos.unrealized_plpc else 0}%",
            "Unrealized P/L Today": pos.unrealized_intraday_pl,
            "Current Price": pos.current_price,
            "Market Value": pos.market_value  # Added for more context
        }
        for pos in positions if pos.qty != 0
    ]

    # If there are no positions, return a simple message
    if not data:
        return "No open positions in your portfolio."
    return tabulate(data, headers="keys", tablefmt="grid")