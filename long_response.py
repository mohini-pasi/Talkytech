import random

R_EATING = "I don't like eating anything because I'm a bot obviously!"
R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"
R_CHATBOT = "A chatbot is a computer program that uses artificial intelligence (AI) and natural language processing (NLP) to understand customer questions and automate responses to them, simulating human conversation."

def unknown():
    default_responses = [
        "I'm not sure how to respond to that.",
        "Can you please rephrase your question?",
        "I'm still learning, so I might not understand everything.",
        "That's interesting! Can you tell me more?",
        "I don't have an answer for that right now."
    ]
    return random.choice(default_responses)

# Example usage
print(unknown())