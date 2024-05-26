import speech_recognition as sr

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Please wait. Calibrating microphone...")
    # listen for 5 seconds and create the ambient noise energy level
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print("Microphone calibrated")

    print("Say something!")
    with microphone as source:
       audio = recognizer.listen(source)

    print("Recognizing...")
    try:
      # recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
       print("Google Web Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech service; {0}".format(e))
    
if __name__ == "__main__":
  recognize_speech_from_mic()