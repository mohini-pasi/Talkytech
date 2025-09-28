import random   # Import random module to pick random replies

# --------------------------
# Predefined long responses
# --------------------------

# Response when user asks about food
R_EATING = "🍔 I don't eat food because I'm a bot — but I do love bytes of data! 😄"

# Response when user asks for advice
R_ADVICE = "💡 If I were you, I'd search the internet — it's full of amazing answers! 🚀"

# Response when user asks "what is a chatbot"
R_CHATBOT = (
    "🤖 A chatbot is a computer program that uses artificial intelligence (AI) "
    "and natural language processing (NLP) to understand your questions and "
    "respond like a human! Pretty cool, right? 🌟"
)

# --------------------------
# Function: unknown response
# --------------------------
def unknown():
    # List of default replies if chatbot doesn't understand the question
    default_responses = [
        "😕 Hmm... I'm not sure how to respond to that. Could you rephrase?",
        "🤔 Can you please ask that in a different way?",
        "📚 I'm still learning! I may not understand everything yet.",
        "✨ That's interesting! Tell me more! 😊",
        "🤷‍♂️ I don't have an answer for that yet, but I'm trying to learn! 💙"
    ]
    # Randomly return one response from the list
    return random.choice(default_responses)


# --------------------------
# Example usage for testing
# --------------------------
if __name__ == "__main__":
    # Run this file directly to test the unknown() function
    print(unknown())
