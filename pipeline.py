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
    pipeline.if_step("are we using prod account(and not paper account)?", 
                     then_steps=["switch to paper account"], 
                     else_steps=[])
    tqqq_price, _ = pipeline.int_step("check current price of TQQQ")
    limit_sell_price = tqqq_price * 1.05
    stop_loss_price = tqqq_price * 0.01
    buy_price = tqqq_price * 0.97
    if pipeline.boolean_step("check if I own more or equal of 100 shares of TQQQ")[0]:
        if pipeline.boolean_step("is there a limit sell for TQQQ exists already?")[0]:
            print(pipeline.summarize_full_history()[0])
        else:
            pipeline.step(f"""set limit sell order for 100 TQQQ for price {limit_sell_price}""")
    is_there_a_limit_buy, history_with_buy_order = pipeline.boolean_step("is there a non canceled (and non panding canceled) 'limit buy' for TQQQ exists already?")
    rsi, _ = pipeline.int_step("calcualte RSI for TQQQ")
    if rsi < 30:
        if is_there_a_limit_buy:
            pipeline.step("cancel buy order for TQQQ", history=history_with_buy_order)
        pipeline.step(f"buy 100 TQQQ shares with market price, set limit sell price to {limit_sell_price} and stop loss to {stop_loss_price}")
    else:
        if is_there_a_limit_buy:
            _, history_with_buy_orders = pipeline.step("get all active limit buy orders")
            limit_buy_price, _ = pipeline.float_step("what is the 'limit buy price' of a latest non canceled 'limit buy' order we have for TQQQ", 
                                                        history=history_with_buy_orders)
            pipeline.if_step(f"is the price of 'limit buy' is strictly lower than {limit_buy_price * 0.95}?",
                                then_steps=["cancel limit buy order",
                                            f"set limit buy order for 100 of TQQQ for {buy_price}."],
                                else_steps=[],
                                history=history_with_buy_orders)
        else:
            pipeline.step(f"set limit buy order for 100 of TQQQ for price {buy_price}.")
    pipeline.summarize_full_history()[0]


# run the pipeline once each 1 hour
while True:
    try:
        run_the_pipeline()  
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    time.sleep(36000)  