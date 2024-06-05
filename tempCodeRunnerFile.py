from flask import Flask, jsonify, request
from flask_cors import CORS
import pyttsx3
import webbrowser
import datetime
import pyjokes
import speech_recognition as sr
import os
import ctypes

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
        website = command.replace("open ", "").strip()
        open_website(website)
    elif "search" in command:
        query = command.replace("search ", "").strip()
        search_google(query)
    elif "calculator" in command:
        open_calculator()
    elif "microsoft office" in command:
        open_microsoft_office()
    elif "file explorer" in command:
        open_file_explorer()
    elif "web browser" in command:
        open_web_browser()
    elif "shutdown" in command:
        shutdown_computer()
    elif "restart" in command:
        restart_computer()
    elif "lock" in command:
        lock_computer()
    elif "notepad" in command:
        open_notepad()
    else:
        search_general(command)

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

def open_website(website):
    if not website.startswith("http"):
        website = "http://" + website
    webbrowser.open(website)
    speechtx(f"Opening {website}.")

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speechtx(f"Searching for {query} on Google.")

def search_general(query):
    search_google(query)

def open_calculator():
    os.system("calc")

def open_microsoft_office():
    os.system("start excel")
    os.system("start winword")
    os.system("start powerpnt")

def open_file_explorer():
    os.system("explorer")

def open_web_browser():
    webbrowser.open("http://www.google.com")

def shutdown_computer():
    os.system("shutdown /s /t 1")

def restart_computer():
    os.system("shutdown /r /t 1")

def lock_computer():
    ctypes.windll.user32.LockWorkStation()

def open_notepad():
    os.system("notepad")

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')
    if command:
        process_command(command)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'No command received'}), 400

if __name__ == "__main__":
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        while True:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio)
                print("You said:", command)
                process_command(command)
            except sr.UnknownValueError:
                print("Sorry, could not understand the audio.")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
