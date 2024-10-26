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
    _, history_with_tqqq_price = pipeline.step("check current price of TQQQ")
    if pipeline.boolean_step("check if I own more or equal of 100 shares of TQQQ")[0]:
        if pipeline.boolean_step("is there a limit sell for TQQQ exists already?")[0]:
            print(pipeline.summarize_full_history()[0])
        else:
            pipeline.step("""set limit sell order for 100 TQQQ for price +4% of current price.
                            Keep in mind that price should be a number, not a string that computes
                            number or a code, it has to be a precomputed number!""", 

                            history=history_with_tqqq_price)
    else:
        is_there_a_limit_buy, _ = pipeline.boolean_step("is there a non canceled (and non panding canceled) 'limit buy' exists already?")
        if is_there_a_limit_buy:
            _, history_with_buy_orders = pipeline.step("get all active limit buy orders")
            limit_buy_price, _ = pipeline.float_step("what is the 'limit buy price' of a latest non canceled 'limit buy' order we have for TQQQ", 
                                                        history=history_with_buy_orders)
            pipeline.if_step(f"is the price of 'limit buy' is strictly lower than {limit_buy_price * 0.95}?",
                                then_steps=["cancel limit buy order",
                                            """set limit buy order for 100 of TQQQ for price 3 precent below the current price. 
                                            Do not return compute formula, do compute of the price yourself in your head. 
                                            Keep in mind that price should be a number, not a string that computes number or a code, it has to be a precomputed number!"""],
                                else_steps=[],
                                history=history_with_tqqq_price)
        else:
            pipeline.step("set limit buy order for 100 of TQQQ for price 3 precent below the current price.", 
                            history=history_with_tqqq_price)
    pipeline.summarize_full_history()[0]


# run the pipeline once each 1 hour
while True:
    try:
        run_the_pipeline()  
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    time.sleep(36000)  