import base64
import os
import pickle
import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS
from audioCheck import check_profanity_audio, check_profanity, check_profanity_audio_google
from videoCheck import check_profanity_video
from face_rec import register_face, recognize_face

import datetime

app = Flask(__name__)
CORS(app)


@app.route('/video', methods=['POST'])
def process_data():
    print('recieved something')
    data = request.json.get('data')
    if data:
        # Decode the base64 data and save it to a file
        binary_data = base64.b64decode(data.split(',')[1])
        basename = "mylogfile"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix]) + '.webm'
        print(filename)
        with open(filename, 'wb') as f:
            f.write(binary_data)
        try:
            # audio_profanity = check_profanity_audio(filename)
            audio_profanity = check_profanity_audio_google(filename)
        except:
            audio_profanity = False
        try:
            videoProfanity = False
        except:
            videoProfanity = False
        # delete the file
        os.remove(filename)
        # Perform any necessary processing here
        # For example, you can convert the data to a pickle object
        # pickle.dump(binary_data, open("recording.pkl", "wb"))
        return jsonify({'message': 'Data processed successfully',
                        'audio_profanity': audio_profanity,
                        'video_profanity': videoProfanity,
                        'profanity': audio_profanity or videoProfanity
                        }), 200
    else:
        return jsonify({'message': 'Invalid data'}), 400


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json.get('data')
    print(data)
    if data:
        return jsonify({'message': 'Data processed successfully',
                        'profanity': check_profanity(data)
                        }), 200
    else:
        return jsonify({'message': 'Invalid data'}), 400


known_path = "known_faces"  # Set the path to your known faces folder
unknown_path = "unknown_faces"


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    image = request.files['image']
    print(email, password)

    register_face(email, known_path, image)

    return jsonify({'message': 'Data processed successfully', }), 200


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    image = request.files['image']
    print(email, password)

    msg = recognize_face(email, known_path, image)
    if msg != "You are unknown first register your self":
        return jsonify({'message': 'Data processed successfully', 'isValid': True, 'msg': msg}), 200
    else:
        return jsonify({'message': 'Data processed successfully', 'isValid': False, 'msg': msg}), 200


if __name__ == '__main__':
    app.run(debug=True)
