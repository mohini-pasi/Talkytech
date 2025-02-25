from flask import Flask, render_template, request, jsonify
import re
import long_response as long
import random

app = Flask(__name__)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses
    response('Hello! I am TalkyTech, your AI assistant. How can I help you today?', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('Goodbye! Have a great day!', ['bye', 'goodbye'], single_response=True)
    response('I am doing well! Thank you for asking. How about you?', ['how', 'are', 'you', 'doing'], single_response=True)
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you! I appreciate your kind words.', ['i', 'love', 'talkytech'], required_words=['talkytech'])
    response('My name is TalkyTech, and I am an AI chatbot. What is your name?', ['is', 'your', 'name'], single_response=True)
    response('Namaste! How can I assist you?', ['namaste'], single_response=True)
    response('Good night! Wishing you all the best!', ['good night', 'gn'], single_response=True)
    response('Good morning! Hope you have a wonderful day!', ['good morning', 'gm'], single_response=True)
    response('I can understand and communicate in both English and Hindi.', ['language'], single_response=True)
    response('I am here to assist you with any questions you may have about technology, coding, or just to chat!', ['help', 'technology', 'coding'], single_response=True)
    response('What would you like to know about AI?', ['AI', 'artificial', 'intelligence'], single_response=True)
    response('I can provide you with resources for learning programming.', ['resources', 'learning', 'programming'], single_response=True)
    response('Would you like to hear a joke?', ['joke', 'funny'], single_response=True)
    response('I can share a fun fact about technology!', ['fact', 'technology'], single_response=True)

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
    response(long.R_CHATBOT, ['chatbot', 'work', 'of'], required_words=['work', 'chatbot'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.form['user_input']
    response = get_response(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)