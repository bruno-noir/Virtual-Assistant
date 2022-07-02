# filtering warnings : controls whether warnings are controlled or displayed

import warnings  # warning module
import pyttsx3  # text to speech conversion
import speech_recognition as sr  # speech recognition module
from gtts import gTTS
import playsound
import os
import datetime
import calendar
import random
import wikipedia
import webbrowser
import ctypes
import winshell
import subprocess
import pyjokes
import smtplib
import requests
import json
from twilio.rest import Client
import wolframalpha
import time

warnings.filterwarnings("ignore")

engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

def talk(audio):
    engine.say(audio)
    engine.runAndWait()


# talk("This is a test") #program will say this is a test while running

# creating functions
# function to take in audio and recognized the speech then return that speech as a string

def rec_audio():
    recog = sr.Recognizer()

    with sr.Microphone() as source:  # we are using microphone as a source
        print("Listening...")
        audio = recog.listen(source)

    data = " "

    try:
        data = recog.recognize_google(audio)
        print("You said: " + data)

    except sr.UnknownValueError:
        print("Assistant could not understand the audio")

    except sr.RequestError as ex:
        print("Request Error from Google Speech Recognition" + ex)

    return data


rec_audio() #testing the fun if it recognises our speech or not

def response(text):
    print(text)

    tts = gTTS(text=text, lang="en")

    audio = "Audio.mp3"
    tts.save(audio)

    playsound.playsound(audio)

    os.remove(audio)


def call(text):
    action_call = "Anya"

    text = text.lower()

    if action_call in text:
        return True

    return False


def today_date():
    now = datetime.datetime.now()
    date_now = datetime.datetime.today()
    week_now = calendar.day_name[date_now.weekday()]
    month_now = now.month
    year_now = now.year

    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    ordinals = [
        "1st",
        "2nd",
        "3rd",
        "4th",
        "5th",
        "6th",
        "7th",
        "8th",
        "9th",
        "10th",
        "11th",
        "12th",
        "13th",
        "14th",
        "15th",
        "16th",
        "17th",
        "18th",
        "19th",
        "20th",
        "21st",
        "22nd",
        "23rd",
        "24th",
        "25th",
        "26th",
        "27th",
        "28th",
        "29th",
        "30th",
        "31st"
    ]

    return f'Today is {week_now}, {months[month_now - 1]} the {ordinals[date_now - 1]}.'  # month start from 0 not 1


def say_hello(text):
    greet = ["hi", "hola", "greetings", "wassup", "hello", "howdy", "what's good", "hey there", "kemcho"]
    response = ["hi", "hola", "greetings", "wassup", "hello", "howdy", "what's good", "hey there", "kemcho"]

    for word in text.split():
        if word.lower() in greet:
            return random.choice(response) + "."

        return ""


def wiki_person(text):
    list_wiki = text.split()
    for i in range(0, len(list_wiki)):
        if i + 3 <= len(list_wiki) - 1 and list_wiki[i].lower() == 'who' and list_wiki[i + 1].lower() == "is":
            return list_wiki[i + 2] + " " + list_wiki[i + 3]


# function to take notes and save it
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


# function to send emails
# cuz less secure apps has no access to my email so it currently doesn't work
def send_email(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    server.login("email", "password")
    server.sendmail("email", to, content)
    server.close()


while True:

    try:

        text = rec_audio()
        speak = " "

        if call(text):

            speak = speak + say_hello(text)

            if "date" in text or "day" in text or "month" in text:
                get_today = today_date()
                speak = speak + " " + get_today

            elif "time" in text:
                now = datetime.datetime.now()
                meridiem = ""
                if now.hour >= 12:
                    meridiem = "p.m"
                    hour = now.hour - 12
                else:
                    meridiem = "a.m"
                    hour = now.hour

                if now.minute < 10:
                    minute = "0" + str(now.minute)
                else:
                    minute = str(now.minute)
                speak = speak + " " + "It is " + str(hour) + ":" + minute + " " + meridiem + " ."

            elif "wikipedia" in text or "Wikipedia" in text:
                if "who is" in text:
                    person = wiki_person(text)
                    wiki = wikipedia.summary(person, sentences=2)  # say 2 lines about the person
                    speak = speak + " " + wiki
             # answer to general questions
            elif "wdo are you" in text or "define yourself" in text:
                speak = speak + """Hello, I am Anya. Your Anya. I am here to help you my master. Well, You can command me to perform various tasks such as solving mathematical questions or opening application etcetera"""
            elif "your name" in text:
                speak = speak + "my name is anya"
            elif "who am I" in text:
                speak = speak + "my master"
            elif "why do you exist" in text or "why did you come" in text:
                speak = speak + "It is a secret"
            elif "how are you" in text:
                speak = speak + "I am fine, thank you"
                speak = speak + "\nHow are you?"
            elif "fine" in text or "good" in text:
                speak = speak + "It's good to know that you are doing fine"
            # opening applications and website
            elif "open" in text.lower():
                # opening applications
                if "firefox" in text.lower():
                    speak = speak + "Opening Firefox"
                    os.startfile(
                        r"C:\Program Files\Mozilla Firefox\firefox.exe"
                        # r cuz python does not allow us to use back slash within string
                    )  # location of the file
                elif "wordpad" in text.lower():
                    speak = speak + "Opening wordpad"
                    os.startfile(
                        r"%ProgramFiles%\Windows NT\Accessories\wordpad.exe"
                    )
                elif "vs code" in text.lower():
                    speak = speak + "Opening Visual Studio Code"
                    os.startfile(
                        r"C:\Users\praty\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                    )
                elif "photoshop" in text.lower():
                    speak = speak + "Opening Adobe Photoshop"
                    os.startfile(
                        r"C:\Program Files\Adobe\Adobe Photoshop 2021\Photoshop.exe"
                    )
                elif "figma" in text.lower():
                    speak = speak + "Opening figma"
                    os.startfile(
                        r"C:\Users\praty\AppData\Local\Figma\Figma.exe"
                    )
                # opening websites
                elif "youtube" in text.lower():
                    speak = speak + "Opening youtube"
                    webbrowser.open("https://youtube.com/")
                elif "google" in text.lower():
                    speak = speak + "Opening Google"
                    webbrowser.open("https://google.com/")
                elif "stackoverflow" in text.lower:
                    speak = speak + "Opening StackOverFlow"
                    webbrowser.open("https://stackoverflow.com/")
                elif "facebook" in text.lower():
                    speak = speak + "Opening facebook"
                    webbrowser.open("https://facebook.com/")
                elif "instagram" in text.lower():
                    speak = speak + "Opening instagram"
                    webbrowser.open("https://instagram.com/")
                else:
                    speak = speak + "Application not availabel"

            # search on youtube and google
            elif "youtube" in text.lower():
                ind = text.lower().split().index("youtube")
                search = text.split()[ind + 1:]
                webbrowser.open(
                    "http://www.youtube.com/results?search_query=" + "+".join(search)
                )
                speak = speak + "Opening " + str(search) + " on youtube"
            elif "search" in text.lower():
                ind = text.lower().split().index("search")
                search = text.split()[ind + 1:]
                webbrowser.open(
                    "http://www.google.com/search?q=" + "+".join(search)
                )
                speak = speak + "Searching " + str(search) + " on google"
            elif "google" in text.lower():
                ind = text.lower().split().index("google")
                search = text.split()[ind + 1:]
                webbrowser.open(
                    "http://www.google.com/search?q=" + "+".join(search)
                )
                speak = speak + "Searching " + str(search) + " on google"
            # working with operating system
            elif "change background" in text or "change wallpaper" in text:
                img = r'C:\Users\praty\OneDrive\Pictures'
                list_img = os.listdir(img)
                imgChoice = random.choice(list_img)
                randomImg = os.path.join(img, imgChoice)
                ctypes.windll.user32.SystemParameterInfoW(20, 0, randomImg, 0)
                speak = speak + "BAckground changed successfully"

            elif "play music" in text or "play song" in text:
                talk("Here you go with music")
                music_dir = r'C:\Resources\projects\Music player'
                songs = os.listdir(music_dir)
                d = random.choice(music_dir)
                random = os.path.join(music_dir, d)
                playsound.playsound(random)

            elif "empty recycle bin" in text:
                winshell.recycle_bin().empty(
                    confirm=True, show_progress=False, sound=True
                )
                speak = speak + "recycle bin emptied"
            # tell some python jokes and making notes
            elif "note" in text or "remember this" in text:
                talk("What would you like me to write down?")
                note_text = rec_audio()
                note(note_text)
                speak = speak + "I have made a note of that"
            elif "jokes" in text or "joke" in text:
                speak = speak + pyjokes.get_joke()

            # working with google maps
            elif "where is" in text:
                ind = text.lower().split().index("is")
                location = text.split()[ind + 1:]
                url = "https://www.google.com/maps/place/" + "".join(location)
                speak = speak + "This is where " + str(location) + " is."
            # sending email
            elif "email to computer" in text or "gmail to computer" in text:
                try:
                    talk("What should I say?")
                    content = rec_audio()
                    to = "Reciever email address"
                    send_email(to, content)
                    speak = speak + "Email has been sent!"
                except Exception as e:
                    print(e)
                    talk("I am not able to send this email")

            elif "mail" in text or "email" in text or "gmail" in text:
                try:
                    talk("What should I send")
                    content = rec_audio()
                    to = input("Enter to address: ")
                    send_email(to, content)
                    speak = speak + "Email has been sent!"
                except Exception as e:
                    print(e)
                    talk("I am not able to send this email")

            # weather api
            elif "weather" in text:
                key = "7cffc6c8afde09dbd82e42bf969aab71"
                weather_url = "http://api.openweathermap.org/data/2.5/weather?"
                ind = text.split().index("in")
                location = text.split()[ind + 1:]
                location = "".join(location)
                url = weather_url + "appid=" + key + "&q=" + location
                js = requests.get(url).json()
                if js["cod"] != "404":
                    weather = js["main"]
                    temperature = weather["temp"]
                    temperature = temperature - 273.15
                    humidity = weather["humidity"]
                    desc = js["weather"][0]["description"]
                    weather_response = "The temperature in Celcius is " + str(temperature) + "The humidity is" + str(humidity) + "and weather description is " + str(desc)

                    speak = speak + weather_response
                else:
                    speak = speak + "City not found"

            # to get latest news
            elif "news" in text:
                url = ('https://newsapi.org/v2/everything?'
                       'q=Apple&'
                       'from=2022-06-26&'
                       'sortBy=popularity&'
                       'apiKey=b301986ff17a48329b2cfcb2a3b2be71')
                try:
                    response = requests.get(url)
                except:
                    talk("Please check your connection")

                news = json.loads(response.text)

                for new in news["articles"]:
                    print(str(new["title"]), "\n")
                    talk(str(new["title"]))
                    engine.runAndWait()

                    print(str(new["description"]), "\n")
                    talk(str(new["description"]))
                    engine.runAndWait()
            #to send message using twilio api
            elif "send message" in text or "send a message" in text:
                account_sid = "AC3f14527de11891f292b23f18eccc3b38"
                auth_token = "76626582539554d3590891cc250757a4"
                client = Client(account_sid, auth_token)

                talk("What should i send")
                message = client.messages.create(
                    body=rec_audio(), from_="+19705784869", to="+918102151582"
                )

                print(message.sid)
                speak = speak + "Message sent successfully"
                #its not complete

            #wolframalpha to answer technical questions
            elif "calculate" in text:
                app_id = "UHWLXA-3V7H6RERP8"
                client = wolframalpha.Client(app_id)
                ind = text.lower().split().index("calculate")
                res = client.query(" ".join(text))
                answer = next(res.results).text
                speak = speak + "The answer is " + answer

            elif "what is" in text or "who is" in text:
                app_id = "UHWLXA-3V7H6RERP8"
                client = wolframalpha.Client(app_id)
                ind = text.lower().split().index("is")
                res = client.query(" ".join(text))
                answer = next(res.results).text
                speak = speak + "The answer is " + answer

            #temporary and permanant exit
            elif "don't listen" in text or "stop listening" in text or "do not listen" in text:
                talk("for how many seconds do you want me to sleep")
                a = int(rec_audio())
                time.sleep(a)
                speak = speak + str(a) + " seconds completed, Now you can ask me anything"

            elif "exit" in text or "quit" in text:
                exit()

            response(speak)


    except:
        talk("I don't know that")

#calender api left to do
#twilio api to send messages
#can add more features in wolframalpha
#temporary or permanant exit from the program