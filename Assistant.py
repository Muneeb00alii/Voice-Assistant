import speech_recognition as sr
from bs4 import BeautifulSoup
import pywhatkit as kit
import datetime
import requests
import wikipedia
import webbrowser
import os
import pyttsx3
import smtplib
import warnings

# Function to convert text to speech and print in command prompt
def speak(text):
    print(text)  # Print the text in the command prompt
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def get_audio(recognizer):
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    print("Recognizing...")
    try:
        query = recognizer.recognize_google(audio).lower()
        print(f"User said: {query}\n")
        return query
    except Exception as e:
        print(e)
        return ""

# Function to get the current time
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

# Function to get the current date
def get_date():
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {current_date}")

# Function to get the weather
def get_weather():
    try:
        url = "https://www.google.com/search?q=weather+in+Lahore+Pakistan"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            weather_data = soup.find('div', class_='BNeawe').text
            speak(f"The weather in Lahore, Pakistan is {weather_data}")
        else:
            speak("Sorry, I couldn't fetch the weather information at the moment. Please try again later.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather information at the moment. Please try again later.")

# Function to open websites or applications
def open_url(query):
    if "youtube" in query:
        webbrowser.open_new_tab("https://www.youtube.com")
        speak("Opening YouTube")
    elif "chatgpt" in query:
        webbrowser.open_new_tab("https://www.chat.openai.com")
        speak("Opening ChatGPT")
    elif "vs code" in query:
        os.system("code")  # Opens VS Code application
        speak("Opening Visual Studio Code")

# Function to provide contact details
def provide_contact_details():
    speak("You can contact Muneeb at +923219697820 or email him at muneeb00ali@gmail.com.")

def send_whatsapp_message(recipient_number, message, hour, minute):
    kit.sendwhatmsg(recipient_number, message, hour, minute)

# Function to leave a message for Muneeb
def leave_message_for_muneeb():
    speak("Please leave your message for Monique.")
    speak("What is your name?")
    user_name = get_audio()
    speak("Please leave your message.")
    user_message = get_audio()
    with open("monique_messages.txt", "a") as file:
        file.write(f"From: {user_name}\nMessage: {user_message}\n\n")
    speak("Your message has been saved successfully.")
    speak("Here is a Message from Muneeb. Hi it's Muneeb. I'm currently busy. I'll get back to you as soon as possible. Thank you for your message.")

def send_email(sender_email, sender_password, recipient_email, message):
    # Compose the email
    subject = "Email from Muneeb's Python Voice Assistant Chloe"
    body = message
    mail = f"Subject: {subject}\n\n{body}"
    # Log in to the email server (Outlook.com)
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    # Send the email
    server.sendmail(sender_email, recipient_email, mail)
    print("Email sent successfully!")
    speak("Email sent successfully!")

    server.quit()


# Function to read news headlines
def read_news(recognizer):
    url = "https://news.google.com/rss"
    response = requests.get(url)
    if response.status_code == 200:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # Ignore the warning
            soup = BeautifulSoup(response.text, "html.parser")
        news_list = soup.find_all("item")
        batch_size = 5
        index = 0
        while index < len(news_list):
            speak(f"Here are {batch_size} news headlines:")
            for news in news_list[index:index+batch_size]:
                speak(news.title.text)
            index += batch_size
            if index < len(news_list):
                speak("Would you like to hear more news headlines?")
                response = get_audio(recognizer)
                if "yes" not in response:
                    speak("Exiting news headlines.")
                    break
            else:
                speak("That's all for now. Exiting news headlines.")
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")

def main():
    contacts = {"sister" : "+923394004815", "father" : "+923009697820", "myself" : "+923219697820"}
    os.system("cls")  # Clear the command prompt
    print("Initializing Chloe...\n")
    recognizer = sr.Recognizer()
    # wake_word = "chloe"
    speak("Hi! I'm Muneeb's Personal Assistant Chloe. How can I help you today?")
    while True:
        # user_input = get_audio(recognizer)
        # if wake_word in user_input:
        #     speak("Hi! I'm Muneeb's Personal Assistant. How can I help you today?")
        
        query = get_audio(recognizer)
        if "time" in query:
            get_time()
        elif "email" in query:
            speak("Please enter the recipient's email address.")
            recipient_email = input("Recipient's Email: ")
            message = get_audio(recognizer)
            send_email("chloe.wang.mq@outlook.com", "password", recipient_email,message)
        elif "date" in query:
            get_date()
        elif "weather" in query:
            get_weather()
        elif "news" in query:
            read_news(recognizer)
        elif "search" in query or "google" in query:
            speak("What do you want to search for?")
            search_query = get_audio(recognizer)
            webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query}")
        elif "wikipedia" in query:
            speak("What do you want to know about?")
            wiki_query = get_audio(recognizer)
            try:
                summary = wikipedia.summary(wiki_query, sentences=2)
                speak(f"According to Wikipedia, {summary}")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any information on that.")
        elif "who is" in query:
            person = query.split("who is")[-1].strip()
            try:
                summary = wikipedia.summary(f"{person} (politician)", sentences=4)
                speak(f"{person} is {summary}")
            except wikipedia.exceptions.PageError as e:
                speak(f"Sorry, I couldn't find any information on {person}.")
                print(e)
            except Exception as e:
                speak("An error occurred while fetching information.")
                print(e)
        elif any(word in query for word in ["good", "great", "thank you"]):
            speak("You're welcome! Is there anything else I can assist you with?")
        elif "open" in query:
            open_url(query)
        elif "contact" in query:
            provide_contact_details()
            speak(" Would you like to leave a message for him?. If yes then say message.")
        elif "message" in query and "muneeb" in query:
            leave_message_for_muneeb()
        elif "send message on whatsapp" in query or "whatsapp" in query:
            speak("Who do you want to send the message to.")
            recipient_number = get_audio(recognizer)
            if recipient_number in contacts:
                recipient_number = contacts[recipient_number]
            else:
                speak("Sorry, I don't have the contact details for that person. Woiuld you like to enter the number manually?")
                recipient_number = input("Recipient's Phone Number: ")
            speak("What message would you like to send?")
            message = input("Message: ")
            speak("At what time should I send the message? Please enter the hour.")
            hour = int(input("Hour (24-hour format): "))
            speak("And the minute?")
            minute = int(input("Minute: "))
            send_whatsapp_message(recipient_number, message, hour, minute)
        elif "name" in query:
            speak("My name is Chloe. I am Muneeb's personal assistant.")
        elif "stop" in query or "exit" in query or "bye" in query:
            speak("Goodbye!")
            break
        elif "shut" in query:   
            speak("Teri  asi shut up karaan ge ke sat naslain yad karien ge")
        else:
            # speak("I'm sorry, I didn't get that. Please try again.")
            continue

main()
