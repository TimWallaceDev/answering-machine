from flask import Flask, request, send_from_directory
from gtts import gTTS
import json
# import RPi.GPIO as GPIO
import os

app = Flask(__name__)

# Set up GPIO
# LED_PIN = 17
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(LED_PIN, GPIO.OUT)

# Define paths
MESSAGE_AUDIO_FILE = 'messages.txt'
AUDIO_FILE = 'message.mp3'

# Path to store the messages
MESSAGE_FILE = 'messages.json'

def load_messages():
    try:
        with open(MESSAGE_FILE, 'r') as file:
            return json.load(file)
    except:
        return {'new': [], 'old': []}

def save_messages(messages):
    with open(MESSAGE_FILE, 'w') as file:
        json.dump(messages, file)

@app.route('/')
def index():
    return 'Voicemail Server is running'

@app.route('/submit', methods=['POST'])
def submit_message():
    message = request.form.get('message')
    name = request.form.get("name")
    # voicemail = "you have a new message from " + name + " . : " + message
    messages = load_messages()
    message_data = {"name": name, "message": message}

    # Save new message in JSON file for voicemail app
    messages['new'].append(message_data)
    print(messages)
    save_messages(messages)

    # save in txt file for demo
    if message:
        with open(MESSAGE_AUDIO_FILE, 'a') as f:
            f.write(message + '\n')
        # Blink LED to indicate new message
        # GPIO.output(LED_PIN, GPIO.HIGH)
        # GPIO.cleanup()
        return 'Message received!'
    return 'No message received', 400

@app.route('/read-messages', methods=['GET'])
#demo voicemail
def read_messages():
    with open(MESSAGE_FILE, 'r') as f:
        messages = f.readlines()
        print(messages)
    tts = gTTS(text=messages, lang='en')
    tts.save(AUDIO_FILE)
    return send_from_directory('.', AUDIO_FILE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


#you have {blank} new messages and {blank} old messages

#first new message:
    #message
    #option to skip
    #option to delete

#second new message:
    #message
    #option to skip
    #option to delete

#first old message:
    #message
    #option to skip
    #option to delete

#second old message
    #message
    #option to skip
    #option to delete


#end of messages
