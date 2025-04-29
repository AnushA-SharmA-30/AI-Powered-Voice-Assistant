import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import smtplib
import requests
import pywhatkit
import os
from dotenv import load_dotenv
import openai

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# Speak text
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Listen to voice
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        return r.recognize_google(audio).lower()
    except sr.UnknownValueError:
        speak("I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service is down.")
        return ""

# GPT response

# GPT response
def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or use "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Send email
def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_app_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.quit()

# Get weather
def get_weather(city="Mumbai"):
    api = f"http://api.weatherapi.com/v1/current.json?key=your_weather_api_key&q={city}"
    res = requests.get(api).json()
    if "current" in res:
        temp = res["current"]["temp_c"]
        condition = res["current"]["condition"]["text"]
        return f"It's {temp}°C with {condition} in {city}."
    return "I couldn't get the weather info."

# Handle commands
def handle_command(query):
    if "time" in query:
        speak(datetime.datetime.now().strftime("%I:%M %p"))

    elif "open youtube" in query:
        webbrowser.open("https://youtube.com")

    elif "open google" in query:
        webbrowser.open("https://google.com")

    elif "play music" in query:
        pywhatkit.playonyt("lofi beats")  # or your fav playlist

    elif "weather" in query:
        speak(get_weather("Bangalore"))

    elif "email to" in query:
        speak("What should I say?")
        content = listen()
        send_email("someone@example.com", content)
        speak("Email sent.")

    elif "ai mode" in query or "chatgpt" in query:
        speak("Go ahead, I'm listening.")
        question = listen()
        reply = get_ai_response(question)
        speak(reply)

    elif "exit" in query or "bye" in query:
        speak("Goodbye!")
        exit()

    else:
        speak("Let me think...")
        speak(get_ai_response(query))

# MAIN LOOP
def main():
    speak("Hello! I'm your smart voice assistant.")
    while True:
        query = listen()
        if query:
            handle_command(query)

if __name__ == "__main__":
    main()
