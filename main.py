import vertexai
import inspect
from vertexai.generative_models import (
    GenerativeModel,
)
from gemini_toolbox import declarations
from gemini_toolbox import client
import gemini_investor

all_functions = [
    func
    for name, func in inspect.getmembers(gemini_investor, inspect.isfunction)
]

all_functions_tools = declarations.generate_tool_from_functions(all_functions)

vertexai.init(project="gemini-trading-backend", location="us-west1")

model = GenerativeModel(model_name="gemini-1.5-pro", tools=[all_functions_tools])

client = client.GeminiChatClient(all_functions, model, debug=True)

print(client.send_message("can you sell my one SPY call, strike 549, for 8/23/24 by limit price 100$"))
