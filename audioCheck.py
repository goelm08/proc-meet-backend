import subprocess
import os
import speech_recognition as sr

def extract_audio(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file, # Input file
        output_file       # Output file
    ]
    subprocess.run(command, check=True)

with open(r'offensive.txt') as file:
    profanity_words = file.read()
profanity_words = profanity_words.split('\n')

def check_profanity(text):
    for word in text.split(' '):
        if word.lower() in profanity_words or '*' in word:
            print (word)
            return True
    return False

def check_profanity_audio(video_file_path):
    audio_file_name = video_file_path.split('.')[0] + '.wav'
    extract_audio(video_file_path, audio_file_name)
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_name) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        print(text)
    os.remove(audio_file_name)
    return check_profanity(text)
