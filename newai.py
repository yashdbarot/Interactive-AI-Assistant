import os
import subprocess
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import time


engine = pyttsx3.init()

NAME_FILE = "name.txt"
SEARCH_HISTORY_FILE = "search_history.txt"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  
        try:
            audio = recognizer.listen(source, timeout=8) 
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            speak("Sorry, I couldn't understand you.")
        except sr.WaitTimeoutError:
            print("No speech detected.")
            speak("No speech detected.")
        return None

def get_user_name():
    if os.path.exists(NAME_FILE) and os.path.getsize(NAME_FILE) > 0:
        with open(NAME_FILE, "r") as file:
            name = file.read().strip()
        return name
    else:
        speak("What is your name?")
        name = listen()
        if name:
            with open(NAME_FILE, "w") as file:
                file.write(name)
            speak(f"Nice to meet you, {name}!")
            return name
        else:
            speak("I didn't catch your name. Please try again.")
            return get_user_name()

def log_search(query):
    with open(SEARCH_HISTORY_FILE, "a") as file:
        file.write(query + "\n")

def find_software(query, search_paths):
    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if query in file.lower() and file.endswith((".exe", ".lnk")):  
                    return os.path.join(root, file)
    return None

def open_software(software_path):
    try:
        speak("Opening the software.")
        print(f"Opening: {software_path}")
        subprocess.Popen(software_path, shell=True)
    except Exception as e:
        print(f"Error: {e}")
        speak("I couldn't open the software.")

def search_wikipedia(query):
    try:
        speak(f"Searching Wikipedia for {query}.")
        result = wikipedia.summary(query, sentences=2)
        print(result)
        speak(result)
        log_search(f"Wikipedia search: {query}")
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No page found on Wikipedia for your query.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("I encountered an error while searching Wikipedia.")

def search_web(query):
    """Perform a web search."""
    speak(f"Searching the web for {query}.")
    webbrowser.open(f"https://www.google.com/search?q={query}")
    log_search(f"Web search: {query}")

def search_youtube(query):
    """Perform a YouTube search."""
    speak(f"Searching YouTube for {query}.")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    log_search(f"YouTube search: {query}")

def play_music(app_name):
    apps = {"youtube": "YouTube", "apple music": "Apple Music", "amazon music": "Amazon Music"}
    if app_name in apps:
        speak(f"Opening {apps[app_name]} for you.")
        webbrowser.open(f"https://www.{app_name.replace(' ', '')}.com")
        log_search(f"Music app opened: {apps[app_name]}")
    else:
        speak("Sorry, I couldn't find that music app.")

def create_text_file():
    speak("What do you want to write in the file?")
    text = listen()
    if text:
        filename = f"speech_to_text_{int(time.time())}.txt"
        with open(filename, "w") as file:
            file.write(text)
        speak(f"I have saved your text in {filename}.")
    else:
        speak("I didn't catch that. Please try again.")

def perform_system_task(task):
    """Perform system tasks like shutdown, restart, sleep."""
    tasks = {
        "shut down": "shutdown /s /t 1",
        "restart": "shutdown /r /t 1",
        "sleep": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0",
        "open settings": "start ms-settings:"
    }
    if task in tasks:
        speak(f"Performing {task} now.")
        os.system(tasks[task])
    else:
        speak("I couldn't recognize the task you want.")

def main():
    search_paths = [
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        "C:\\Users\\YourUsername\\Desktop",
        "C:\\Users\\YourUsername\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs",
        "C:\\",
    ]

    name = get_user_name()
    if name:
        speak(f"Welcome back, {name}!")

    while True:
        speak("How can I assist you?")
        query = listen()

        if query:
            if "search" in query:
                speak("What do you want to search?")
                search_query = listen()
                if search_query:
                    search_web(search_query)
            elif "wikipedia" in query:
                speak("What should I search on Wikipedia?")
                wiki_query = listen()
                if wiki_query:
                    search_wikipedia(wiki_query)
            elif "youtube" in query:
                speak("What should I search on YouTube?")
                yt_query = listen()
                if yt_query:
                    search_youtube(yt_query)
            elif "play music" in query:
                speak("Which app should I use: YouTube, Apple Music, or Amazon Music?")
                app_query = listen()
                if app_query:
                    play_music(app_query)
            elif "create file" in query:
                create_text_file()
            elif "shut down" in query or "restart" in query or "sleep" in query or "open settings" in query:
                perform_system_task(query)
            elif "exit" in query or "quit" in query:
                speak("Goodbye! Have a great day!")
                break
            else:
                speak(f"Searching for software: {query}. Please wait.")
                software_path = find_software(query, search_paths)
                if software_path:
                    open_software(software_path)
                    log_search(f"Software search and open: {query}")
                else:
                    speak("Sorry, I couldn't find the software.")
                    log_search(f"Software search failed: {query}")
        else:
            speak("I didn't catch that. Please try again.")

if __name__ == "__main__":
    main()
