from gemini_agents_toolkit.pipeline import Pipeline
from gemini_agents_toolkit.history_utils import print_history
from gemini_agents_toolkit.agent_utils import start_debug_chat
import investor_agent

import vertexai
import time
import traceback


vertexai.init(project="gemini-trading-backend", location="us-west1")


def on_message(message):
    print(message)


def create_client():
    return investor_agent.create_agent(model_name="gemini-1.5-pro-002", debug=False, on_message=on_message)


def run_the_pipeline():
    investor_agent = create_client()

    pipeline = Pipeline(default_agent=investor_agent, use_convert_to_bool_agent=True, debug=False)
    # if not pipeline.boolean_step("is the market open now?")[0]:
    #     print(pipeline.summary())
    #     return
    pipeline.if_step("Is the current account a production account (not a paper account)?", 
                     then_steps=["Switch to paper account"], 
                     else_steps=[])
    tqqq_price, _ = pipeline.int_step("Get the current TQQQ price")
    limit_sell_price = tqqq_price * 1.05
    stop_loss_price = tqqq_price * 0.01
    buy_price = tqqq_price * 0.97
        # Check if we currently own at least 100 shares of TQQQ
    own_more_than_100, _ = pipeline.boolean_step("Do I currently own 100 or more shares of TQQQ?")
    if own_more_than_100:
        # Check if a limit sell order for TQQQ already exists
        if pipeline.boolean_step("Does a limit sell order for TQQQ already exist?")[0]:
            print(pipeline.summarize_full_history()[0])
        else:
            pipeline.step(f"Place a limit sell order for 100 shares of TQQQ at {limit_sell_price}")

    # Check if there's an active (non-canceled) limit buy order for TQQQ
    is_there_a_limit_buy, history_with_buy_order = pipeline.boolean_step(
        "Is there an active (non-canceled, not pending cancel) limit buy order for TQQQ?"
    )
    if is_there_a_limit_buy:
        if own_more_than_100:
            pipeline.step("Cancel the active limit buy order for TQQQ", history=history_with_buy_order)
        else:
            _, history_with_buy_orders = pipeline.step("Retrieve the latest active limit buy orders for TQQQ", 
                                                       history=history_with_buy_order)
            limit_buy_price, _ = pipeline.float_step(
                "Get the limit buy price of the latest active limit buy order for TQQQ", 
                history=history_with_buy_orders
            )
            pipeline.if_step(
                f"Is the limit buy price strictly lower than {limit_buy_price * 0.95}?",
                then_steps=[
                    "Cancel the active limit buy order for TQQQ",
                    f"Place a limit buy order for 100 shares of TQQQ at {buy_price}"
                ],
                else_steps=[],
                history=history_with_buy_orders
            )
    elif not own_more_than_100:
        pipeline.step(f"Place a limit buy order for 100 shares of TQQQ at {buy_price}")

    pipeline.summarize_full_history()[0]


# run the pipeline once each 1 hour
while True:
    try:
        run_the_pipeline()  
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    time.sleep(36000)  