import investor_agent
import inspect
import google.cloud.logging

from gemini_agents_toolkit import agent
import investor_agent
from google.oauth2 import service_account

import vertexai


vertexai.init(project="gemini-trading-backend", location="us-west1")


MODEL_NAME="gemini-1.5-flash-002"

GCP_PROJECT = "gemini-trading-backend"
GCP_CREDENTAILS = service_account.Credentials.from_service_account_file(
    './sa.json')

logging_client = google.cloud.logging.Client(project=GCP_PROJECT, credentials=GCP_CREDENTAILS)
logging_client.setup_logging()


def create_client(user_id, on_message_received):
    return investor_agent.create_agent(
         model_name=MODEL_NAME, 
         debug=True, 
         history_depth=10, 
         add_scheduling_functions=True, 
         gcs_bucket="gemini_jobs", 
         gcs_blob=f"jobs_{user_id}.json",
         on_message=on_message_received)
