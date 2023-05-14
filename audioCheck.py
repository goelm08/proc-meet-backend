import subprocess
import os
import speech_recognition as sr
import torch
import librosa
import numpy as np
import soundfile as sf
from IPython.display import Audio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer


# Initialize tokenizer and model
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

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
    input_audio, _ = librosa.load(audio_file_name, sr=16000)

    # Tokenize the input audio
    input_values = tokenizer(input_audio, return_tensors="pt").input_values

    # Get logits from the model
    logits = model(input_values).logits

    # Get the predicted token ids
    predicted_ids = torch.argmax(logits, dim=-1)

    # Decode the token ids to get the transcription
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    print(transcription)
    os.remove(audio_file_name)
    return check_profanity(transcription)


def check_profanity_audio_google(video_file_path):
    audio_file_name = video_file_path.split('.')[0] + '.wav'
    extract_audio(video_file_path, audio_file_name)
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_name) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        print(text)
    os.remove(audio_file_name)
    return check_profanity(text)
