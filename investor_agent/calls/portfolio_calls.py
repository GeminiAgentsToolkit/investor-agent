from tabulate import tabulate
from investor_agent.utils import TradingClientSingleton

def get_portfolio():
    """Returns a formatted table representing the portfolio of the account."""

    positions = TradingClientSingleton.get_instance().get_all_positions()

    # Prepare data for the table
    data = []
    total_market_value = 0.0
    total_cost_basis = 0.0  # Додаємо змінну для загальної початкової вартості

    for pos in positions:
        if pos.qty != 0:
            market_value = float(pos.market_value)
            cost_basis = float(pos.cost_basis)  # Початкова вартість позиції
            pl_percentage = (market_value - cost_basis) / cost_basis * 100 if cost_basis != 0 else 0.0

            data.append({
                "Tkr": pos.symbol,
                "Q": pos.qty,
                "cuP": f"{float(pos.current_price):.2f}",
                "mVal": f"{market_value:.2f}",
                "%": f"{pl_percentage:.2f}%"
            })

            total_market_value += market_value
            total_cost_basis += cost_basis

    # If there are no positions, return a simple message
    if not data:
        return "No open positions in your portfolio."

    # Calculate Total P/L (%)
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

    # Wrap the table in code block for Telegram
    return f"```\n{table}\n```"
