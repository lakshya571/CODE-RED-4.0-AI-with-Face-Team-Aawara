import openai
import speech_recognition as sr
from gtts import gTTS
import os
import time
import subprocess

# Step 1: Listening and Speech Recognition (Speech-to-Text)
def listen_and_recognize():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        print("Recognizing speech...")
        speech_text = recognizer.recognize_google(audio)
        print(f"You said: {speech_text}")
        return speech_text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Step 2: Send recognized text to ChatGPT (API Call)
def get_chatgpt_response(prompt_text):
    openai.api_key = "sk-...k48A"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_text,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    answer = response.choices[0].text.strip()
    print(f"ChatGPT response: {answer}")
    return answer

# Step 3: Convert ChatGPT response to speech (Text-to-Speech)
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    audio_file = "response.mp3"
    tts.save(audio_file)
    print("Playing response audio...")
    os.system(f"mpg321 {audio_file}")  # Use appropriate audio player for your system
    return audio_file

# Step 4: Send speech to NVIDIA Audio2Face for facial animation
def send_audio_to_a2f(audio_file):
    # Command to send the audio file to Audio2Face using its API or CLI
    a2f_command = f"Audio2Face_API --input {audio_file}"  # Example command, replace with actual
    print("Sending audio to A2F...")
    subprocess.run(a2f_command, shell=True)
    print("A2F facial animation triggered.")

# Full Workflow: Listen, Process with ChatGPT, Convert to Speech, Animate in A2F
def main_workflow():
    # Step 1: Listen and recognize speech
    speech_text = listen_and_recognize()
    
    if speech_text:
        # Step 2: Get response from ChatGPT
        chatgpt_response = get_chatgpt_response(speech_text)
        
        # Step 3: Convert ChatGPT text response to speech
        audio_file = text_to_speech(chatgpt_response)
        
        # Step 4: Send audio to A2F for facial animation
        send_audio_to_a2f(audio_file)
    
    else:
        print("No valid speech recognized.")

if __name__ == "__main__":
    while True:
        print("Starting interaction loop...")
        main_workflow()
        time.sleep(2)  # Adjust timing for real-time interaction
