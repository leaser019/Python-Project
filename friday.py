import pyttsx3
import datetime

friday = pyttsx3.init()
voice = friday.getProperty('voices')
friday.setProperty('voice',voice[1].id)

def speak(audio):
    friday.say(audio)
    friday.runAndWait()
def time():
    Time=datetime.datetime.now().strftime("%I:%M:%p")
    speak(Time)
    print(Time)
def welcome():
    hour=datetime.datetime.now().hour
    
    if hour >=0 and hour <=12:
        speak('Good Morning')
    elif hour>12 and hour <18:
        speak('Good Afternoon')
    if hour<18 and hours <24 : 
        speak('Good Night') 
    speak("How can i help you")
    
if  __name__ =="__main__":
    welcome()        
      
    