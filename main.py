import common



# model = GenerativeModel(model_name="gemini-1.5-flash", tools=[all_functions_tools], system_instruction=system_instruction)
# client = client.GeminiChatClient(all_functions, model, debug=True)

def send_msg_to_user(msg: str):
    """Send a message to the user. Use this function to send messages to the user, not just return text string. Text string that you generate(that is not passed to this function) can be random. User will not see it."""
    print(msg)


clt = common.create_client("local", send_msg_to_user)

#print(client.send_message("can you sell my one SPY call, strike 549, for 8/23/24 by limit price 100$"))
#print(client.send_message("can you cancel order iwth id 550e8400-e29b-41d4-a716-446655440000"))
#print(clt.send_message("can you check order status with id 21e916c1-61a8-4cb9-bbeb-b61338f4b6d9"))
#print(clt.send_message("show me last 10 closed ordders"))
# chat logic
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break
        response = clt.send_message(user_input)
        print("Jessica:", response)