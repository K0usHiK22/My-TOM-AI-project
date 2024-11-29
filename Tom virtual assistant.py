#A PERSONAL VIRTUAL ASSISTANT 
#NAME : TOM AI

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
  

def hello_greeting():
     """greeting function which greets the user according to time
     whenever he wakes the AI up"""
     now = datetime.now()
     hour = now.hour
     if hour < 12:
        return "Good morning sir, ."
     elif 12 <= hour < 18:
        return "Good afternoon sir, ."
     else:
        return "Good evening sir, ."
     

def play_youtube(song):
    """A function to play anything on youtube using pywhatkit module"""
    kit.playonyt(song)


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
 

def open_apps(app_name):  
    """A function to open the below given applications whenever the user tells to the AI"""      
    try:
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "command prompt": "cmd.exe",
            "task manager": "taskmgr.exe"
        }

        if app_name in apps:
            app_path = (apps[app_name])
            if platform.system() == "Windows":
                subprocess.Popen(app_path)
                talk_something(f"opening {app_name}, sir")
        else:
            talk_something(f"sorry i couldn't find the {app_name}, sir")
    except Exception as e:
        talk_something("error occured opening the app, sir")
        print(f"error as {e}")


def calculations(expressions):
        """this function calculates the numbers and"""
        try:
            expression = expression.replace("plus", "+").replace("minus", "-")
            expression = expression.replace("times", "*").replace("into", "*")
            expression = expression.replace("divided by", "/").replace("over", "/")
            expression = expression.replace("square root of", "math.sqrt")
            expression = expression.replace("^", "**")
            allowed_globals = {"__builtins__": None, "math": math}
            result = eval(expressions, allowed_globals)
            return f"the result, is {result}"
        except Exception as e:
            return f"error while calculating {str(e)}"
        

def get_weather(city, api_key):
    """This function provides the weather report"""
    try:
        # OpenWeather API URL
        api_key = "YOUR API KEY HERE"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        # Fetch data
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:  # Successful request
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            report = (
                f"The weather in {city} is currently {weather} "
                f"with a temperature of {temperature}°C. "
                f"Humidity is at {humidity}% and wind speed is {wind_speed} meters per second."
            )
            
            print(report)
            talk_something(report)
        else:
            print("City not found or API error!")
            talk_something("Sorry, I couldn't fetch the weather report. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
        talk_something("An error occurred while fetching the weather report.")

        
def close_Window_tom(window_name):
    """This function is used to close the window by using pygetwindow module 
    whenever the user wants to close it"""
    try:
        windows = gw.getAllTitles()
        matching_windows = [win for win in windows if window_name.lower() in win.lower()]
        if matching_windows:
            for window in matching_windows:
                app_window = gw.getWindowsWithTitle(window)[0]
                if "chrome" in app_window.title.lower():
                    app_window.close()
                    talk_something(f"chrome with {app_window} window tab is now closed, sir")
                else:
                    app_window.close()
                    talk_something(f"the application {app_window} has been now closed, sir")
        else:
            talk_something(f"there is no {window_name} found to be closed, sir")
    except Exception as e:
        talk_something(f"error occured closing the {window_name}")
        print(f"error...{e}")


def get_info_from_wikipedia(query):
    """A function to fetch the information from wikipedia by using wikipedia module 
    whenever the user commands to AI"""
    try:
        if not query: 
            return "I need a topic to fetch information from Wikipedia, sir."
        info = wikipedia.summary(query, sentences = 3)
        return info
    except wikipedia.exceptions.DisambiguationError as e:
        return  f"Your query returned multiple results: {', '.join(e.options[:5])}. Please specify more clearly."
    except wikipedia.exceptions.PageError:
        return "I couldn't find anything related to that on Wikipedia, sir."
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Sorry, the request timed out while fetching Wikipedia data."
    except Exception as e:
        print(f"an error ocured {str(e)}")


def send_whatsapp_message(contact_number, message):
    """A function which sends the whatsapp message using the number provided by the user
    it opens the whatsapp web if logged in then sends the message using pywhatkit"""
    try:
        kit.sendwhatmsg_instantly(f"+91{contact_number}", message)
        time.sleep(15)
    except Exception as e:
        talk_something("error occued while sending the message, sir!!")
        print(f"error occured {e}")


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
    

"""main block of the code"""
if __name__ == "__main__":
    try:
        """the AI begins to start"""
        talk_something("initializing Tom Ai....hold on...")
        talk_something("checking the system")
        talk_something("turning the engine on")
        talk_something("checking the AI")
        talk_something("good to go")

        while True:
            r = sr.Recognizer()
            talk_something("please give a wakeup call to tom AI!!!")
            print("recognizing...")

            try:
                with sr.Microphone() as source:
                    recogniser.adjust_for_ambient_noise(source, duration = 3)
                    print("Listening...")
                    audio = r.listen(source, timeout=10, phrase_time_limit=5)
                    word = r.recognize_google(audio).lower()
                    word = word.lower()


                if "hello tom" in word or "hey tom" in word or "tommy" in word:
                    greet = hello_greeting()
                    talk_something(f"hello {greet}, {(random.choice(opening.wakeup_tom))}")
                    is_active = True

                    while is_active:
                        with sr.Microphone() as source:
                            print("Tom Ai is Active now, give commands...")
                            users_command = listen_for_user(None)

                            processingcommand(users_command)
                            talk_something(random.choice(opening.tom_command_responses))
                        
            except sr.UnknownValueError:
                talk_something("I couldn't understand your wake-up command.")
            except sr.RequestError as e:
                talk_something("I'm having trouble connecting to the system.")
                print(f"RequestError: {e}")

    except KeyboardInterrupt:
        talk_something("Shutting down Tom AI. Goodbye!")
    except Exception as e:
        talk_something("An unexpected error occurred. Please restart the system.")
        print(f"Unhandled Error: {e}")