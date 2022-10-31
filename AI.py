from neuralintents import GenericAssistant
import speech_recognition #Library for performing speech recognition
import pyttsx3 as tts #Pyttsx3 is a text-to-speech conversion library
import sys #Exit program if needed
import pyaudio #Can use Python to play and record audio
import pywhatkit #Most popular library for WhatsApp and YouTube automation
import phonenumbers
from phonenumbers import geocoder #Provides geographical coordinates
from googlesearch import search

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 175)

todo_list = [] #For todo and show my todo functions

def hello():
        speaker.say("Hello. What can I do for you?")
        speaker.runAndWait()

def next():
        speaker.say("What else can I do for you?")
        speaker.runAndWait()

def quit():
        speaker.say("Bye")
        speaker.runAndWait()
        sys.exit(0)

def create_note():
        global recognizer

        speaker.say("what do you want to write onto your note?")
        speaker.runAndWait()

        done = False

        while not done:
                try:
                        with speech_recognition.Microphone() as mic:
                                recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
                                audio = recognizer.listen(mic)
                                note = recognizer.recognize_google(audio)
                                note = note.lower() #so we do not have confusion with the case
                                speaker.say("Choose a filename!")
                                speaker.runAndWait()

                                recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
                                audio = recognizer.listen(mic)

                                filename = recognizer.recognize_google(audio)
                                filename = filename.lower()

                        with open(filename, 'w') as f:
                                f.write(note)
                                done = True
                                speaker.say(f"I successfully created the note {filename}")
                                speaker.runAndWait()

                except speech_recognition.UnknownValueError:
                        recognizer = speech_recognition.Recognizer()
                        speaker.say("I did not understand you! Please try again!")
                        speaker.runAndWait()

        if done != False:
                next()

def add_todo():
        global recognizer

        speaker.say("what todo do you want to add?")
        speaker.runAndWait()

        done = False

        while not done:
                try:
                        with speech_recognition.Microphone() as mic:
                                recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
                                audio = recognizer.listen(mic)

                                item = recognizer.recognize_google(audio)
                                item = item.lower()

                                todo_list.append(item)
                                done = True

                                speaker.say(f"I added {item} to the to do list!")
                                speaker.runAndWait()
                except speech_recognition.UnknownValueError:
                        recognizer = speech_recognition.Recognizer()
                        speaker.say("I did not understand. Please try again!")
                speaker.runAndWait()

        if done != False:
                next()

def show_todos():
        speaker.say("The items on your to do list are the following")
        for item in todo_list:
                speaker.say(item)
        speaker.runAndWait()

        next()

def youtube():
        global recognizer

        speaker.say("What video would you like to see?")
        speaker.runAndWait()

        done = False

        while not done:
                try:
                        with speech_recognition.Microphone() as mic:
                                recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
                                audio = recognizer.listen(mic)
                                video = recognizer.recognize_google(audio)
                                video = video.lower()

                                speaker.say(f"I will play your {video}")
                                play = pywhatkit.playonyt({video})

                                done = True

                                #speaker.say(f"Did you say {video}")
                                #speaker.runAndWait()
                                #check_audio = recognizer.listen(mic)

                                #confirm = recognizer.recognize_google(check_audio)
                                #confirm = confirm.lower()

                                #if confirm == "Yes":
                                        #speaker.say(f"I will play your {video}")
                                        #play = pywhatkit.playonyt({video})
                                        #done = True
                                #if confirm == "No":
                                        #youtube()

                except speech_recognition.UnknownValueError:
                        recognizer = speech_recognition.Recognizer()
                        speaker.say("I did not understand you!")
                        youtube()

        if done != False:
                next()

mappings = {
        "greeting": hello,
        "create_note": create_note,
        "add_todo": add_todo,
        "show_todos": show_todos,
        "exit": quit,
        "next": next,
        "youtube": youtube

}

assistant = GenericAssistant('Intents.json', intent_methods = mappings)
assistant.train_model()

assistant.save_model()
assistant.load_model()

while True:
        try:
                with speech_recognition.Microphone() as mic:
                        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                        audio = recognizer.listen(mic)

                        message = recognizer.recognize_google(audio)
                        message = message.lower()

                assistant.request(message)

        except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()