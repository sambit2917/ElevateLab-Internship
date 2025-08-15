print("🤖 Hello! I am ChatBuddy. If you want to exit type 'bye'")

while True:
    user_input = input("You :").lower()
    # Exit Condition
    if user_input == 'bye':
        print("ChatBuddy : GoodBye have a grat day😊")
        break

    # Greetings
    elif user_input in ['hii', 'hello', 'hey']:
        print("ChatBuddy: Hello there how can I help you today?")
    # Asking about wellbeing
    elif user_input in ['how are you', 'how are you doing']:
        print("ChatBuddy: I am doing great, thanks for your asking! How abut you?")
    # Asking for name
    elif 'your name' in user_input:
        print('ChatBuddy: I am ChatBuddy, your friendly chatbot!')
    # Weather query
    elif 'weather' in user_input:
        print("ChatBuddy: I can't check the weather tody, but I hope it's sunny, where you are?")
    # Default replay
    else:
        print("ChatBuddy: I am not sure how to respond on this but I am learning eveyday!")