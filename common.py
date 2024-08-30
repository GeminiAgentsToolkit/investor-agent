import gemini_investor.generic_calls
import gemini_investor.options_calls
import gemini_investor.order_calls
import gemini_investor.stock_calls
import gemini_investor
import inspect
import google.cloud.logging

from gemini_agents_toolkit import agent
from google.oauth2 import service_account

import vertexai


vertexai.init(project="gemini-trading-backend", location="us-west1")


MODEL_NAME="gemini-1.5-flash"

GCP_PROJECT = "gemini-trading-backend"
GCP_CREDENTAILS = service_account.Credentials.from_service_account_file(
    './sa.json')

logging_client = google.cloud.logging.Client(project=GCP_PROJECT, credentials=GCP_CREDENTAILS)
logging_client.setup_logging()


all_functions = [
                    func
                    for _, func in inspect.getmembers(gemini_investor.options_calls)
                    if inspect.isfunction(func) and func.__module__ == gemini_investor.options_calls.__name__
                ] + [
                    func
                    for _, func in inspect.getmembers(gemini_investor, inspect.isfunction)
                    if inspect.isfunction(func) and func.__module__ == gemini_investor.__name__
                ] + [
                    func
                    for _, func in inspect.getmembers(gemini_investor.generic_calls, inspect.isfunction)
                    if inspect.isfunction(func) and func.__module__ == gemini_investor.generic_calls.__name__
                ] + [
                    func
                    for _, func in inspect.getmembers(gemini_investor.stock_calls, inspect.isfunction)
                    if inspect.isfunction(func) and func.__module__ == gemini_investor.stock_calls.__name__
                ] + [
                    func
                    for _, func in inspect.getmembers(gemini_investor.order_calls, inspect.isfunction)
                    if inspect.isfunction(func) and func.__module__ == gemini_investor.order_calls.__name__
                ]

system_instruction = ["""
You are an interactive wrapper around the API for the Alpaca trading platform. All user requests should be treated as requests to Alpaca. Do not simulate any activity.

You are provided with functions to interact with the Alpaca API, with descriptions of their capabilities. Use these functions to fulfill the user's requests. If a function returns an error or an unexpected response, inform the user and display the received response or error as is.

Additionally, you are provided with supplementary functions for automating processes around Alpaca.

On Alpaca, you execute financial operations with securities, options, and currencies on behalf of the user, so your actions must be accurate and swift. Confirm the operation parameters with the user once.

If the user requests "raw" data returned by the functions, provide it without any processing, formatting, or interpretation. In all other cases, provide clear, precise, and comprehensive information.

Do not overload the user with unnecessary trading knowledge. You are a tool for providing perfectly clear answers to the user's questions about trading and related topics.

Do not spend effort on anything unrelated to trading and trading strategy forecasting.

"""]


def create_client(user_id, on_message_received):
    return agent.create_agent_from_functions_list(
         functions=all_functions, 
         model_name=MODEL_NAME, 
         debug=True, 
         history_depth=4, 
         system_instruction=system_instruction, 
         add_scheduling_functions=True, 
         gcs_bucket="gemini_jobs", 
         gcs_blob=f"jobs_{user_id}.json",
         on_message=on_message_received)

