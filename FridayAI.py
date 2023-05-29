import speech_recognition as sr
import os
import pyttsx3 as tts   
import webbrowser
import openai
import time
import datetime
import random
from config import apikeyopenai
from config import apikeyopenweather
from config import apikeynewsapi
import requests
import json
import googletrans as gt
import wikipedia
import string
import re

engine = tts.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


# SAYING TEXT
def say(text):
    engine.say(text)
    engine.runAndWait()

# TAKING COMMAND FROM USER
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        # r.energy_threshold = 500
        # r.energy_threshold = 1200
        r.energy_threshold = 2000

        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Friday"
            # return input("Some Error Occurred. Please Enter Command: ")


# ARTIFICIAL INTELLIGENCE
def ai(prompt):
    openai.api_key = apikeyopenai
    text = f"Open AI responce for Prompt: {prompt} \n ********************************\n\n"

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    text += response.choices[0].message.content
    # print(response.choices[0].message.content)
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"C:\\Users\\HP\\Desktop\\Programming\\Projects\\Friday\\Openai/{prompt}.txt", "w") as f:
        f.write(text)


# CHAT OPENAI
chatStr = ""
def chat(cquery):
    global chatStr
    openai.api_key = apikeyopenai
    chatStr += f"Fahad: {cquery}\n Friday: " 
    response = openai .ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": chatStr}])
    say(response.choices[0].message.content)
    chatStr += f"{response.choices[0].message.content}\n"
    return response.choices[0].message.content

# GENERATE PASSWORD
def generatepassword(length=10):
    say("generating password")
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    print(password)





if __name__ == "__main__":

    # say("Hello I am Friday A.I. How may I help you?")
    inputk = input("Voice or typing: " )
    if "voice" in inputk:
        say("Hello Boss I am Friday A.I. How may I help you?")
    elif "typing" in inputk:
        say("Hello Boss I am Friday A.I. How may I help you? Please type your command")
    while True:
        if "voice" in inputk:
            print("Listening...")
            query = takeCommand()
        elif "typing" in inputk:
            query = input("Enter Command: " )
        # print("Listening...")
        # query = input("Enter Command: ")

#       QUIT FRIDAY
        if "shutdown Friday".lower() in query.lower():
            say("Thank you Fahad, Have a good day")
            break


#       OPEN WEBSITES
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://wikipedia.com"], ["Chat GPT", "https://chat.openai.com"], ["music online", "https://music.youtube.com"], ["mail", "https://mail.google.com"], ["google drive", "https://drive.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Sir...")
                webbrowser.open(site[1])


#       PLAY MUSIC
        if "play music".lower() in query.lower():
            musicnames = os.listdir('D:\Spotify songs')
            music = random.choice(musicnames)
            musicPath = f"D:\Spotify songs\{music}"
            say(f"Playing {music}")
            os.startfile(musicPath)


#       ASK TIME
        if "the time".lower() in query.lower():
            strftTime = datetime.datetime.now().strftime('%H:%M')
            say(f"Sir the time is {strftTime}")


#       OPEN APPS
        apps = [
        ["Adobe Acrobat", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe Acrobat.lnk"],
        ["Excel", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel.lnk"],
        ["Chrome", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome.lnk"],
        ["Microsoft Edge", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Edge.lnk"],
        ["OneDrive", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OneDrive.lnk"],
        ["OneNote", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OneNote.lnk"],
        ["Outlook", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Outlook.lnk"],
        ["PowerPoint", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PowerPoint.lnk"],
        ["PC Manager", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PC Manager.lnk"],
        ["Word", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"],
        ["todo", "C:\\Users\\HP\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Todoist.lnk"],
        ["Media Player", "C:\\Users\\HP\\Desktop\\Media Player.lnk"],
        ["Calculator", "C:\\Users\\HP\\Documents\\Calculator.lnk"],
        ["Files", "C:\\Users\\HP\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\File Explorer.lnk"],
        ["clock", "C:\\Users\\HP\\Documents\\Clock.lnk"]
        ]
        for app in apps:
            if f"open {app[0]}".lower() in query.lower():
                say(f"Opening {app[0]} Sir...")
                os.startfile(app[1])


#       CHAT GPT PROMPT
        if "using artificial intelligence".lower() in query.lower():
            say(f"making {query}")
            query1 = query[30:]
            ai(prompt=query1)


#       GOOGLE SEARCH
        if "google search".lower() in query.lower():
            query2 = query[14:]
            say(f"searching {query2} in google")
            webbrowser.open(f"https://www.google.com/search?q={query2}")


#       YOUTUBE SEARCH
        if "search youtube".lower() in query.lower():
            queryt = query.replace("search youtube ".lower(), "")
            say(f"searching {queryt} in youtube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={queryt}")


#       TRANSLATOR
        if "translate".lower() in query.lower():
            querytr = query.replace("Translate ".lower(), "")
            try:
                say(f"translating {querytr} to hindi")
                translator =gt.Translator()
                translated = translator.translate(querytr, src='en', dest = 'hi')
                say("I can't talk hindi giving command to Iris to translate")
                # print(translated.text)
                engine.setProperty('voice', voices[2].id)
                say(translated.text)
                engine.setProperty('voice', voices[1].id)
                say("Thank you Iris for translating.Taking command from Iris")
            except Exception as e:
                say("Sorry! Cannot translate some error occured")


#       WEATHER
        if "what's the weather in".lower() in query.lower():
            queryweather = query[22:]
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            api_key = apikeyopenweather
            city = queryweather

            def kelvin_celsius(kelvin):
                celsius = kelvin - 273.15
                return celsius

            url = base_url + "appid=" + api_key + "&q=" + city
            response = requests.get(url).json()
            temp_kelvin = response['main']['temp']
            temp_celsius = kelvin_celsius(temp_kelvin)
            feels_like_kelvin = response['main']['feels_like']
            feels_like_celsius = kelvin_celsius(feels_like_kelvin)
            wind_speed = response['wind']['speed']
            humidity = response['main']['humidity']
            description = response["weather"][0]['description']
            sunrise_time = datetime.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
            sunset_time = datetime.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
            say(f"Temprature in {city} is : {temp_celsius:.2f}°C")
            say(f"Temprature in {city} is : feels like {feels_like_celsius:.2f}°C")
            say(f"Humidity in {city} is : {humidity}%")
            say(f"Wind Speed in {city} is : {wind_speed}m/s")
            say(f"General Weather in {city} is : {description}")
            say(f"Sun rises in {city} at {sunrise_time} local time")
            say(f"Sun sets in {city} at {sunset_time} local time")


#       TEMPERATURE
        if "what's the temperature in".lower() in query.lower():
            queryweather = query[25:]
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            api_key = apikeyopenweather
            city = queryweather
            def kelvin_celsius(kelvin):
                celsius = kelvin - 273.15
                return celsius

            url = base_url + "appid=" + api_key + "&q=" + city
            response = requests.get(url).json()
            temp_kelvin = response['main']['temp']
            temp_celsius = kelvin_celsius(temp_kelvin)
            description = response["weather"][0]['description']
            say(f"Temprature in {city} is: {temp_celsius:.2f}°C")
            say(f"General Weather in {city} is: {description}")


#       FETCH NEWS
        if "tell me today's news of".lower() in query.lower():
            say("Hello Nova please read the headlines for boss")
            
            querynews = query.replace("tell me today's news of ".lower(), "")
            datet = datetime.datetime.today() - datetime.timedelta(days=1)
            Previous_Date_Formatted = datet.strftime ('%Y-%m-%d')
            date = str(Previous_Date_Formatted)
            r = requests.get(f"https://newsapi.org/v2/everything?q={querynews}&from={date}&language=en&sortBy=publishedAt&apiKey={apikeynewsapi}")
            data = json.loads(r.content)
            try:
                engine.setProperty('voice', voices[3].id)
                for i in range(5):
                    news = data['articles'][i]['title']
                    description = data['articles'][i]['description']
                    print("News", i+1, ":",news)
                    print("description", i+1, ":", description)
                    say(news)
                    say(description)
            except Exception as e:
                say("No news in Category")
            engine.setProperty('voice', voices[1].id)
            say("Thank you Nova for news")
            


#       SEARCH WIKIPEDIA
        if "search Wikipedia".lower() in query.lower():
            try:
                querywiki = query.replace("Search Wikipedia ", "")
                say("searching wikipedia...")
                results = wikipedia.summary(querywiki, sentences = 2)
                say("according to wikipedia ")
                print(results)
                say(results)
            except Exception as e:
                say("Can't get results for the query please try again")


#       SEARCH AMAZON
        if "search amazon for ".lower() in query.lower():
            queryamazon = query.replace("search amazon for ", "")
            say(f"searching amazon for {queryamazon}")
            webbrowser.open(f"https://www.amazon.in/s?k={queryamazon}&ref=nb_sb_noss")


#       SEARCH FLIPKART
        if "search flipkart for".lower() in query.lower():
            queryflipkart = query.replace("search flipkart for ", "")
            say(f"searching flipkart for {queryflipkart}")
            webbrowser.open(f"https://www.flipkart.com/search?q={queryflipkart}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")


#       GENERATE PASSWORD
        if "generate password".lower() in query.lower():
            try:
                def find_numbers(string):
                    numbers = re.findall(r'\d+', string)
                    return numbers
                text = query
                numbers = find_numbers(text)
                listToStr = int(' '.join([str(elem) for elem in numbers]))
                generatepassword(length = listToStr)
            except Exception as e:
                say("Please specify length of password also")


#       THANK YOU COMMAND
        if "Thank you".lower() in query.lower():
            time.sleep(1)
            say("You're welcome! If you have any further questions or need assistance with anything, feel free to ask. I'm here to help!")


#       CHAT
        else:
            sub_strings = ['open'.lower(), 'google search'.lower(), 'play'.lower(), "Using artificial intelligence".lower(),"What's the weather in".lower(), "tell me today's news of".lower(), "search youtube".lower(), "translate".lower(), "search wikipedia".lower(), "generate passsword".lower(), "what's the weather in".lower(), "what's the temperature in ".lower(), "search amazon for ".lower(), "search flipkart for".lower()]
            if not any(x in query.lower() for x in sub_strings):
                chat(query)

#make a list and use accordingly to particular command




