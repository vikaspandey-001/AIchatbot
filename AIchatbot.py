import pyttsx3
from datetime import datetime
import speech_recognition as sr
import wikipedia
import openai
import os
import sys
import webbrowser

openai.api_key=os.environ["OPENAI_API_KEY"]

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(audio):
    '''
    This function  is used to speak the argument audio in system voice.
    '''
    print("AI Bot is speaking...")
    engine.say(audio)
    engine.runAndWait()

def wishme():
    '''
    This function is used to wish according to time.
    '''
    hour=int(datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning sir")
    elif hour>12 and hour<18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

def lisening_user():
    '''
    This function is used to listen the user's speech.
    '''
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold=0.5
        audio=r.listen(source)
    try:
        print("Recognising...")
        query=r.recognize_google(audio,language="en-in")
        print(f"User: {query}")
    except Exception as e:
        # print(e)
        print("say that again please!")
        return"None"
    return query

def wiki(query):
    '''
    Function for searching on wikipedia
    '''
    query=query.replace("wikipedia","")
    results=wikipedia.summary(query,sentences=2)
    return results

def gpt_searching(ask):
    '''
    This function is used to search the query using openai.
    '''
    ask=ask.replace("gpt","")
    response=openai.Completion.create(
        engine="text-davinci-003",
        prompt=ask
    )
    answer=response.choices[0].text
    return answer

def browser_search(search):
    '''
    This function is used to open browser according to user need.
    '''
    search= search.replace("open","")     # we will get search as " youtube in browser"
    search=search.replace ("in browser","")       # we will get search as " youtube "
    search=search[1:len(search)-1]      # we will get query as "youtube"
    opening=f"www.{search}.com"        # youtube will open in browser as "www.youtube.com"
    return opening

def play_music():
    '''
    This function is used to play the music for user from the music directory.
    '''
    music_dir="C:\\Users\\Vikas Pandey\\Music"
    songs=os.listdir(music_dir)
    print(songs[0])
    return os.startfile(os.path.join(music_dir,songs[0]))

if __name__=='__main__':
    speak("Welcome back sir, How can I assist you?")
    while True:
        query=lisening_user().lower()
        # speak(query)

        # logic for executing task based on query
        if query=="wish me":
            wishme()
        elif "wikipedia" in query:
            speak("Sure sir wait a while.")
            try:
                results=wiki(query)
                print(results)
                speak("according to wikipedia")
                speak(results)
            except Exception:
                speak("can't find it on wikipedia!")
            
        elif "tell" in query:
            speak("Sure sir wait a while.")
            results=gpt_searching(query)
            print(results)
            speak("according to openai")
            speak(results)
        elif "exit" in query:
            speak("Goodbye sir.")
            sys.exit()
        elif "in browser" in query:
            url=browser_search(query)
            webbrowser.open(url)
        elif "play music" in query:
           speak("Playing the song")
           play_music()
           
        