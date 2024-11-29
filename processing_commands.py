"""modules to run the code efficiently"""
import speech_recognition as sr
import pyttsx3
import webbrowser
import random
import opening
import pywhatkit as kit
import subprocess
import platform
import wikipedia
import displaying_info
import requests
import os
import time
import math
import pygetwindow as gw
import pyaudio
from datetime import datetime

pyaudio_instance = pyaudio.PyAudio()
recogniser = sr.Recognizer()
is_active = False

"""funtions"""
def talk_something(text): #speaks whatever the text given using ptttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)   
    engine.setProperty('rate', 130) 
    engine.setProperty('volume', 1.0)  
    engine.say(text)
    engine.runAndWait()
  
def listen_for_user(prompt=None):
    """a function used to make the AI listen to user while he gives the command"""
    if prompt:
        talk_something(prompt)
    with sr.Microphone() as source:
        recogniser.adjust_for_ambient_noise(source)
        print("Listening for your response...")
        audio = recogniser.listen(source, timeout=10, phrase_time_limit=10)
        try:
            user_response = recogniser.recognize_google(audio).lower()
            return user_response
        except sr.UnknownValueError:
            talk_something("Sorry, I didn't catch that. Could you please repeat?")
            return listen_for_user(prompt)
        except sr.RequestError as e:
            talk_something("I'm having trouble connecting. Please try again later.")
            print(f"RequestError: {e}")
            return None
 

"""processes user commands"""
def processingcommand(c):
     global is_active
     c = c.lower()
     if "please open google" in c or "open google" in c: #opens google
          talk_something("opening google")
          webbrowser.open("https://www.google.com/")
          talk_something("google opened sir")
          

     elif "please open gmail" in c or "open gmail" in c: #opens gmail
          webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
          talk_something("gmail opened sir")


     elif "play" in c: #plays songs directly in youtube
            song = c.replace("play", "").strip()
            if not song:
                song = listen_for_user("what do you want me to play sir...")
            if song:
                talk_something(f"playing{song}on youtube")
                kit.playonyt(song)


     elif "open wikipedia" in c: #opens wikipedia
         talk_something("opening wikipedia sir")
         webbrowser.open("https://www.wikipedia.org/")
         talk_something("wikipedia opened sir")


     elif "get from wikipedia" in c: #gets anything from wikipedia and asks to whether display it or not
         query = c.replace("get from wikipedia", "").strip()
         if not query:
             talk_something("what do you want me to fetch from wikipedia sir")
             query = listen_for_user()
         if query:
                info = get_info_from_wikipedia(query)
                talk_something(info)
                talk_something("would you like me to display for your convenience sir??")
                response = listen_for_user()
                if "yes" in response or "do it" in response or "do it tom" in response:
                 talk_something("displaying sir")
                 displaying_info.display_info(info)
                else:
                 talk_something("ok sir im not displaying the result")


     elif "please open youtube" in c or "open youtube" in c: #opens youtube 
            talk_something("Opening YouTube")
            webbrowser.open("https://www.youtube.com/")
            talk_something("youtube opened, sir")
            song = listen_for_user("what do you want me to play sir?")
            if "nothing" in song:
                talk_something("ok sir")
            else:
                talk_something(f"playing{song}on youtube")
                kit.playonyt(song)

            
     elif "calculate" in c: #calculates the basic math
         expression = c.replace("calculate", "").strip()
         if not expression:
             expression = listen_for_user("what would you like me to calculate sir")
         else:
             result = calculations(expression)
             talk_something(result)
             talk_something("would you like me to display for your convinience sir??")
             response = listen_for_user()
             if "yes" in response or "do it" in response or "do it tom" in response:
                 talk_something("displaying the result sir")
                 displaying_info.display_info(result)
             else:
                 talk_something("ok sir im not displaying the result")


     elif "shut down pc" in c or "shutdown pc" in c or "turn off pc" in c: #shuts the PC us os module
        talk_something("Are you sure you want to shut down the PC, sir?")
        confirmation = listen_for_user("Please confirm yes or no.")
        if "yes" in confirmation or "shut it down" in confirmation:
            talk_something("Shutting down the PC, sir. Goodbye.")
            if platform.system() == "Windows":
                os.system("shutdown /s /t 1")


     elif "weather report" in c or "weather" in c: #provides the weather report
        talk_something("Which city's weather report do you need sir?")
        city = listen_for_user("Please specify the city.")
        api_key = "YOUR API KEY HERE"
        get_weather(city, api_key)
    
        
     elif "open" in c: #opens the given applications 
        app_name = c.replace("open", "").strip()
        if app_name:
             open_apps(app_name)
        else:
             talk_something("which application do you like me to open sir")


     elif "send whatsapp message" in c or "send message in whatsapp" in c: #sends the WhatsApp message
        talk_something("please enter the number to send the message sir")
        contact_number = input("Enter the contact name: ")
        talk_something("What is the message sir?")
        message = listen_for_user().lower()
        send_whatsapp_message(contact_number, message)
        talk_something("I've sent the message sir.")

         
     elif "close" in c or "close the window" in c or "close the window tom" in c: #closes the window
         window_name = c.replace("close", "").strip()
         if not window_name:
             talk_something(f"which window would you like me to close, sir")
         else:
             close_Window_tom(window_name)
             talk_something(f"{window_name} has closed")


     elif "wait tom" in c or "wait" in c: #waits for the wakeup call
        talk_something("Okay, sir, I'll wait until you call me again.")
        while True:
            with sr.Microphone() as source:
                print("Waiting for wake word...")
                recogniser.adjust_for_ambient_noise(source, duration=1)
                audio = recogniser.listen(source, timeout=10, phrase_time_limit=10)
                try:
                    word = recogniser.recognize_google(audio).lower()
                    if "wake up tom" in word or "get up" in word:
                        talk_something("I'm awake and ready for your command, sir.")
                        return
                except sr.UnknownValueError:
                    continue  
                except sr.RequestError as e:
                    print(f"Error: {e}")
                    return
    
     elif "exit tom" in c or "shutdown tom" in c: #Exits the TOM AI
         talk_something(random.choice(opening.tom_goodbye_responses))
         exit()
    