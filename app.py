# pip install flask
from flask import Flask, render_template, request, jsonify  
# Flask → Used to create the web server, connect frontend (HTML) with backend (Python),
# handle routes, and send responses in JSON or HTML.

import re  
# re (Regular Expressions) → Used to split and clean user input, detect keywords,
# and extract patterns (like names) from messages.

import long_response as long   # Custom Python file (not a pip library)
# This is your own file that stores predefined long replies (R_EATING, R_ADVICE, etc.)
# to keep the main code clean and modular.
(__name__)

user_name = None  # Temporary user name (session ke liye, permanent nahi)

# Function: Check how much a user message matches with recognised words
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Count matching words
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculate percentage match
    percentage = float(message_certainty) / float(len(recognised_words))

    # Check required words (agar required words missing ho to response 0 hoga)
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Return match score
    return int(percentage * 100) if has_required_words or single_response else 0


# Function: Check all possible responses and return best one
def check_all_messages(message):
    global user_name
    highest_prob_list = {}  # Dictionary to store {response: probability}

    # Nested helper function to add possible responses
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(
            message, list_of_words, single_response, required_words
        )

    # Detect user name
    if 'name' in message:
        name = extract_name_from_message(message)
        if name:
            user_name = name.capitalize()
            return f"✨ Nice to meet you, {user_name}! How can I assist you?"
    if 'i' in message and 'am' in message:
        name = extract_name_from_message(message)
        if name:
            user_name = name.capitalize()
            return f"😊 Got it, {user_name}! How can I help you today?"

    # Personalized responses if name already detected
    hello = f"👋 Hello{' ' + user_name if user_name else ''}! I\'m TalkyTech. How can I help you today?"
    bye = f"👋 Goodbye{' ' + user_name if user_name else ''}! See you soon! 🌟"

    # Define responses with matching keywords
    response(hello, ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response(bye, ['bye', 'goodbye', 'see', 'later'], single_response=True)
    response('😊 I\'m doing great! Thanks for asking. How about you?',
             ['how', 'are', 'you', 'doing'], single_response=True)
    response('😃 Glad to hear that! Tell me more! ✨',
             ['fine', 'good', 'great', 'okay', 'ok'], single_response=True)
    response('🙏 You\'re welcome! Always here for you. 💙',
             ['thank', 'thanks', 'thankyou'], single_response=True)
    response('🤖 I\'m TalkyTech — your AI friend! What would you like to know? 🌐',
             ['who', 'are', 'you'], required_words=['you'])
    response('🤖 My name is TalkyTech! And you are? 🧑‍💻',
             ['is', 'your', 'name'], single_response=True)
    response('🙏 Namaste! How can I assist you today? 🌼',
             ['namaste'], single_response=True)
    response('🌙 Good night! Sleep tight and dream big! 😴',
             ['good', 'night', 'gn'], single_response=True)
    response('☀️ Good morning! Wishing you a productive day ahead! 🌈',
             ['good', 'morning', 'gm'], single_response=True)
    response('🌆 Good evening! How was your day? ✨',
             ['good', 'evening'], single_response=True)
    response('🗣️ I can chat in English and a bit of Hindi! 🇮🇳',
             ['language'], single_response=True)
    response('💻 Need help with coding, tech, or just want to chat? I\'m here! 🤝',
             ['help', 'technology', 'coding', 'support'], single_response=True)
    response('😆 Want to hear a joke? Just say "tell me a joke"! 🤪',
             ['joke', 'funny', 'laugh'], single_response=True)
    response('💡 Did you know? The first computer bug was an actual moth! 🐛',
             ['fact', 'technology', 'fun', 'interesting'], single_response=True)
    response('✨ I\'m always learning new things. Ask me anything! 🔍',
             ['what', 'can', 'you', 'do'], single_response=True)
    response('🎓 I can share programming resources, tutorials and tips! 📘',
             ['resources', 'learning', 'programming', 'learn'], single_response=True)
    response('🤖 I can explain how a chatbot works if you\'d like!',
             ['how', 'chatbot', 'work'], required_words=['chatbot'])
    response('💡 Here\'s my advice: Keep learning, stay curious, and never stop exploring! 🌍',
             ['give', 'advice'], required_words=['advice'])

    # Responses imported from long_response.py
    response(long.R_ADVICE, ['advice'])
    response(long.R_EATING, ['eat', 'food', 'hungry'], required_words=['eat'])
    response(long.R_CHATBOT, ['chatbot', 'work'], required_words=['chatbot'])

    # More fun replies
    response('😅 I\'m just a bot, but I love chatting with you! 💬',
             ['do', 'you', 'like', 'me'], required_words=['like'])
    response('😜 Haha, you\'re funny! Keep going! 🤣',
             ['haha', 'lol'], single_response=True)

    # Choose best match (highest probability)
    best_match = max(highest_prob_list, key=highest_prob_list.get)

    # If no match found, use unknown response
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Function: Extract name from message (like "my name is Mohini")
def extract_name_from_message(message):
    name = None
    if 'name' in message:
        try:
            index = message.index('is')
            name = message[index + 1]
        except:
            pass
    elif 'am' in message:
        try:
            index = message.index('am')
            name = message[index + 1]
        except:
            pass
    return name


# Function: Process user input → return chatbot response
def get_response(user_input):
    # Convert to lowercase and split into words by spaces/punctuation using regex
    # Example: "Hello, how are you?" → ["hello", "how", "are", "you"]
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    
    # Get chatbot response based on split words
    return check_all_messages(split_message)


# Flask Routes

# Route for the homepage
@app.route('/')
def home():
    # When the page reloads, reset user_name (session reset effect)
    global user_name
    user_name = None
    return render_template('index.html')  # Render frontend template


# Route for chatbot response (called via AJAX/Fetch from frontend)
@app.route('/get_response', methods=['POST'])
def get_bot_response():
    # Get user input from frontend form
    user_input = request.form['user_input']

    # Process the user input through chatbot logic
    response = get_response(user_input)

    # Return chatbot response in JSON format (so frontend JS can use it)
    return jsonify({'response': response})


# Run the Flask app
if __name__ == "__main__":
    # debug=True → auto-reloads server on code change + shows error details
    app.run(debug=True)
