from investor_agent.calls import options_calls, generic_calls, stock_calls, order_calls, portfolio_calls
import inspect


def get_functions_from_subpackage(package):
    """
    Collects functions directly from the specified subpackage within a module.

    Args:
        module: The main module to search within.
        subpackage_name: The name of the subpackage to include.

    Returns:
        A list of functions found in the specified subpackage.
    """

    return [
        func
        for _, func in inspect.getmembers(package)
        if inspect.isfunction(func) and func.__module__ == package.__name__
    ]

ALL_FUNCTIONS = (get_functions_from_subpackage(options_calls) +
                  get_functions_from_subpackage(generic_calls) +
                  get_functions_from_subpackage(stock_calls) +
                  get_functions_from_subpackage(order_calls)+
                  get_functions_from_subpackage(portfolio_calls))