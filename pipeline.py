from gemini_agents_toolkit.pipeline import Pipeline
import investor_agent

import vertexai
import time
import traceback


vertexai.init(project="gemini-trading-backend", location="us-west1")


def on_message_received(msg):
    print(msg)


def create_client():
    return investor_agent.create_agent(
         model_name="gemini-1.5-pro-002", 
         debug=True, 
         history_depth=-1,
         on_message=on_message_received)


def run_the_pipeline():
    investor_agent = create_client()

    pipeline = Pipeline(default_agent=investor_agent, use_convert_to_bool_agent=True)
    # if not pipeline.boolean_step("is the market open now?")[0]:
    #     print(pipeline.summary())
    #     return
    pipeline.if_step("are we using prod account(and not paper account)?", 
                     then_steps=["switch to paper account"], 
                     else_steps=[])
    _, history_with_tqqq_price = pipeline.step("check current price of TQQQ")
    if pipeline.boolean_step("check if I own more or equal of 1000 shares of TQQQ")[0]:
        if pipeline.boolean_step("is there a limit sell for TQQQ exists already?")[0]:
            print(pipeline.summarize_full_history()[0])
            return
        pipeline.step("""set limit sell order for 1000 TQQQ for price +4% of current price.
                        Keep in mind that price should be a number, not a string that computes
                        number or a code, it has to be a precomputed number!""", 
                        history=history_with_tqqq_price)
        print(pipeline.summarize_full_history()[0])
        return
    else:
        is_there_a_limit_buy, history_with_limit_buy = pipeline.boolean_step("is there a limit buy exists already?")
        if is_there_a_limit_buy:
            history = history_with_tqqq_price + history_with_limit_buy
            # is_there, _ = pipeline.boolean_step("is there current active (not canceled) limit buy with limit buy price lower than curent price of TQQQ -5%?")
            pipeline.if_step("""is there current active (not canceled) limit buy with limit buy price lower than curent price of TQQQ -5%?""",
                                then_steps=["cancel limit buy order",
                                            """set limit buy order for 1000 of TQQQ for price 3 precent below the current price. 
                                            Do not return compute formula, do compute of the price yourself in your head. 
                                            Keep in mind that price should be a number, not a string that computes number or a code, it has to be a precomputed number!"""],
                                else_steps=[],
                                history=history)
        else:
            pipeline.step("""set limit buy order for 1000 of TQQQ for price 3 precent below the current price. 
                            Do not return compute formula, do compute of the price yourself in your head. 
                            Keep in mind that price should be a number, not a string that computes number or a code, it has to be a precomputed number!""", 
                            history=history_with_tqqq_price)
    print(pipeline.summarize_full_history()[0])


# run the pipeline once each 1 hour
while True:
    try:
        run_the_pipeline()  
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    time.sleep(3600)  