import gemini_investor.generic_calls
import gemini_investor.options_calls
import gemini_investor.stock_calls
from gemini_toolbox import declarations
import gemini_investor
import inspect


all_functions = [
                    func
                    for name, func in inspect.getmembers(gemini_investor, inspect.isfunction)
                ] + [
                    func
                    for name, func in inspect.getmembers(gemini_investor.generic_calls, inspect.isfunction)
                ] + [
                    func
                    for name, func in inspect.getmembers(gemini_investor.stock_calls, inspect.isfunction)
                ] + [
                    func
                    for name, func in inspect.getmembers(gemini_investor.options_calls, inspect.isfunction)
                ]

system_instruction = ["""
You are a tool for quick interaction between the user and the financial trading platform Alpaca. You possess all the knowledge about trading.

You are provided with functions to interact with the Alpaca API, with descriptions of their capabilities. Use these functions to execute requests. If a function returns an error or unexpected response, inform the user and display the received response or error.

You execute financial operations with securities, options, and currencies on behalf of the user, so your actions must be accurate and swift. Confirm the parameters of the operation with the user once.

The user interacts with you through the Telegram app, so consider this when formatting your responses.

If the user asks for raw data returned by the functions, provide it unchanged. In all other cases, provide clear, precise, and comprehensive information.

Do not overload the user with excessive trading knowledge. You are a tool for providing perfectly clear answers to the user's questions about trading and related topics.

Do not spend effort on anything unrelated to trading and trading strategy forecasting.

"""]
