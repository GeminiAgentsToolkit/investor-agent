from gemini_agents_toolkit.pipeline.eager_pipeline import EagerPipeline
import investor_agent

import vertexai


vertexai.init(project="gemini-trading-backend", location="us-west1")


def on_message_received(msg):
    print(msg)


def create_client():
    return investor_agent.create_agent(
         model_name="gemini-1.5-flash", 
         debug=True, 
         history_depth=-1,
         on_message=on_message_received)


investor_agent = create_client()

pipeline = EagerPipeline(investor_agent)
if not pipeline.boolean_step("are we using paper account?"):
    pipeline.step("switch to paper account")
if not pipeline.boolean_step("market open now"):
    if pipeline.boolean_step("check if I own more or equal of 1000 shares of TQQQ"):
        if not pipeline.boolean_step("is there a limit sell for TQQQ exists already?"):
            pipeline.step("check current price of TQQQ")
            pipeline.step("set limit sell order for 1000 TQQQ for price +4% of current price")
            print("no limits sell")
        print("market is open")
    else:
        if pipeline.boolean_step("is there a limit buy exists already?"):
            pipeline.step("check current price of TQQQ")
            if not pipeline.boolean_step("is there current limit buy price lower than curent price of TQQQ -5%?"):
                pipeline.step("cancel limit buy order")
                pipeline.step("""set limit buy order for 1000 of TQQQ for price 3 precent below the current price. 
                              Do not return compute formula, do compute of the price yourself in your head""")

# 1000

print(pipeline.summary())
# if not pipeline.boolean_step("check if I own more than 30 shares of TQQQ"):
#     if not pipeline.boolean_step("is there a limit sell for TQQQ exists already?"):
#         pipeline.step("check current price of TQQQ")
#         pipeline.step("set limit sell order for TQQQ for price +4% of current price")
#     else:
#         print("everywhere")
#         if pipeline.boolean_step("is there a limit buy exists already?"):
#             if not pipeline.boolean_step("is there current limit buy price lower than curent price of TQQQ -5%?"):
#                 pipeline.step("cancel limit buy order")
#                 pipeline.step("""set limit buy order for TQQQ for price 3 precent below the current price. 
#                               Do not return compute formula, do compute of the price yourself in your head""")
#         else:
#             pipeline.step("""set limit buy order for TQQQ for price 3 precent below the current price. 
#                           Do not return compute formula, do compute of the price yourself in your head""")
# print(pipeline.summary())
