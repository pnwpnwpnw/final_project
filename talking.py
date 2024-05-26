from vtt_test import *
from tts_test import speak
import openai
import time

def introduction(name):
    speak("Hi "+{name}+", welcome to your home page")
    time.sleep(0.5)
    speak("I'm Jarvis, your personal assistance")
    time.sleep(0.5)
    speak("To talk to me, say Hey, jarvis, I will be right here")
          

# Set your OpenAI API key
openai.api_key = "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"

def get_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print("Error:", e)
        return "Sorry, I couldn't generate a response at the moment."

def listening():
    while True:
        # Get user's question through voice input
        speech = recognize_speech_from_mic()
        # If speech is not recognized, continue to the next loop iteration

        if "jarvis" in speech.lower():
            # Get response from OpenAI based on the speech
            response = get_response(speech)
            # Print the response
            print("Response:", response)
        elif speech.lower() == 'shut down':
            break
        else:
            continue

if __name__ == "__main__":
    listening()