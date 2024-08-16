from gtts import gTTS
from playsound import playsound
import json
import time
import os
import random

class Voicemail:
    MESSAGE_FILE = 'messages.json'
    
    def __init__(self):
        self.messages = self.load_messages()

    def load_messages(self):
        try:
            with open(self.MESSAGE_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {'new': [], 'old': []}

    def save_messages(self):
        with open(self.MESSAGE_FILE, 'w') as file:
            json.dump(self.messages, file)

    def play_messages(self):
        self._play_message_list(self.messages['new'], "new")
        self._play_message_list(self.messages['old'], "old")
        print("End of messages")

    def _play_message_list(self, messages, message_type):
        print(f"\nYou have {len(self.messages['new'])} new messages and {len(self.messages['old'])} old messages\n")
        for index in range(len(messages)):
            print(f"\n{message_type.capitalize()} message {index + 1}:")
            print(f"From: {messages[index]['name']}")
            self._play_text_as_speech(messages[index]['message'])
            if self._message_options(messages, index):
                break  # Break if a message was deleted to avoid index issues

    def _play_text_as_speech(self, text):
        try:
            tts = gTTS(text=text, lang='en')
            random_int = random.randint(0,999999)
            audio_file = "message-" + str(random_int) + ".mp3"
            tts.save(audio_file)
            # time.sleep(3)
            playsound(audio_file)
        # finally:
        #     if os.path.exists(audio_file):
        #         os.remove(audio_file)  # Clean up the audio file after playing
        except Exception as error:
            print("error: " + error)

    def _message_options(self, messages, index):
        while True:
            action = input("Enter 's' to skip, 'd' to delete: ").lower()
            if action == 's':
                print("Message skipped.")
                return False  # Continue with the next message
            elif action == 'd':
                print("Message deleted.")
                messages.pop(index)
                self.save_messages()  # Save changes after deleting
                return True  # Break the loop in the play function
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    voicemail = Voicemail()
    voicemail.play_messages()
