from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
import keyboard
from googletrans import Translator  
from gtts import gTTS  
import os

import uvicorn

app = FastAPI()

# Initialize the recognizer
recognizer = sr.Recognizer()

# Enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def save_text_to_file(text, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

async def audio_to_text():
    translator = Translator()
    with sr.Microphone() as source:
        print("Please speak into the microphone...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        # Listen for audio input
        audio = recognizer.listen(source)

        try:
            print("Transcribing audio...")
            # Use Google Speech Recognition to convert audio to text
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            translated_text = translator.translate(text, dest='ta')
            save_text_to_file(translated_text.text, "tamilConvert.txt")  # 'ta' is Tamil code
            print(translated_text)
 
            # Text to Speech (Tamil)
            tts = gTTS(text=translated_text.text, lang='ta')
            # if os.path.exists("output.mp3"):
            #     print("slkdjflks")
            #     os.remove("output.mp3")
            tts.save("output.mp3")  # Save as MP3 file
            os.system("output.mp3")
            print("Tamil audio generated! Saved as output.mp3")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            print("Error occurred: ", str(e))
            return "Error occurred: " + str(e)

# Define a route to handle audio input and return text
@app.get("/audio-to-text")
async def convert_audio_to_text():
    file_path = await audio_to_text()
    if file_path:
        audioOutput = "output.mp3"
        return  FileResponse(audioOutput,media_type="audio/mpeg")
    

# if __name__ == "__m_":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
