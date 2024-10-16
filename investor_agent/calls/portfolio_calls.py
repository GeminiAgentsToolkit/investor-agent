from investor_agent.utils import TradingClientSingleton

def get_portfolio_value(positions=None):
    """
    Returns the current total market value of the portfolio.
    This is the sum of the value of all positions in the portfolio.
    Do not pass anything here as an argument!
    """
    if positions is None:
        positions = TradingClientSingleton.get_instance().get_all_positions()
    return sum(float(pos.market_value) for pos in positions if pos.qty != 0)

def get_portfolio():
    """
    Returns a table representing the portfolio of the account.
    It should be printed in Telegram as is, without adding any formatting characters!
    """
    positions = TradingClientSingleton.get_instance().get_all_positions()
    positions = [pos for pos in positions if pos.qty != 0]

    # If there are no positions, return a simple message
    if not positions:
        return "No open positions in your portfolio."

    # Prepare data for the table
    header = f"{'Tkr':<20} {'Q':>3} {'cuP':>6} {'mVal':>8} {'%':>7}"
    rows = [
        f"{pos.symbol:<20} {pos.qty:>3} {float(pos.current_price):>6.2f} {float(pos.market_value):>8.2f} {(float(pos.market_value) - float(pos.cost_basis)) / float(pos.cost_basis) * 100 if float(pos.cost_basis) != 0 else 0.0:>7.2f}%"
        for pos in positions
    ]

    # Calculate Total P/L (%)
    total_cost_basis = sum(float(pos.cost_basis) for pos in positions)
    total_market_value = get_portfolio_value(positions)  # Reuse the function to get total market value
    total_pl_percentage = (total_market_value - total_cost_basis) / total_cost_basis * 100 if total_cost_basis != 0 else 0.0

    # Adding row with "Total"
    rows.append(f"{'Total':<20} {'':>3} {'':>6} {total_market_value:>8.2f} {total_pl_percentage:>7.2f}%")

    # Join header and rows into a single string with newlines
    table = "\n".join([header] + rows)

    return table
