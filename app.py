from flask import Flask, jsonify, request
from flask_cors import CORS
import pyttsx3
import webbrowser
import datetime
import pyjokes
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

def speechtx(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    rate = engine.getProperty("rate")
    engine.setProperty("rate", 130)
    engine.say(text)
    engine.runAndWait()

def open_application(application):
    if application.lower() == "ms excel":
        os.system("start excel")
        speechtx("Opening Microsoft Excel.")
    elif application.lower() == "music player":
        os.system("start spotify")  # Assuming Spotify is installed
        speechtx("Opening the music player.")
    elif application.lower() == "notepad":
        os.system("start notepad")
        speechtx("Opening Notepad.")
    elif application.lower() == "web browser":
        webbrowser.open("https://www.google.com")
        speechtx("Opening the web browser.")
    elif application.lower() == "whatsapp":
        webbrowser.open("https://web.whatsapp.com/")
        speechtx("Opening WhatsApp.")
    elif application.lower() == "calculator":
        os.system("start calc")
        speechtx("Opening the calculator.")
    else:
        speechtx("Sorry, I don't know how to open that application.")

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speechtx(f"Searching for {query} on Google.")

def search_general(query):
    search_google(query)

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')
    if command:
        process_command(command)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'No command received'}), 400

def tell_name():
    name = "My name is Peter."
    speechtx(name)

def tell_age():
    age = "I am two years old."
    speechtx(age)

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speechtx(f"The current time is {current_time}.")

def tell_date():
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speechtx(f"Today's date is {current_date}.")

def tell_joke():
    joke = pyjokes.get_joke()
    speechtx(joke)

def process_command(command):
    command = command.lower()
    if "your name" in command:
        tell_name()
    elif "old are you" in command:
        tell_age()
    elif "time" in command:
        tell_time()
    elif "date" in command:
        tell_date()
    elif "joke" in command:
        tell_joke()
    elif "open" in command:
        application = command.replace("open ", "").strip()
        open_application(application)
    elif "search" in command:
        query = command.replace("search ", "").strip()
        search_google(query)
    elif "exit" in command or "shutdown" in command:
        speechtx("Shutting down the assistant. Goodbye!")
        exit()
    else:
        search_general(command)

if __name__ == "__main__":
    app.run(debug=True)
