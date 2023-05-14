import base64
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from audioCheck import check_profanity_audio, check_profanity
from videoCheck import check_profanity_video

app = Flask(__name__)
CORS(app)


@app.route('/video', methods=['POST'])
def process_data():
    print('recieved something')
    data = request.json.get('data')
    if data:
        # Decode the base64 data and save it to a file
        binary_data = base64.b64decode(data.split(',')[1])
        with open('recording.webm', 'wb') as f:
            f.write(binary_data)

        audio_profanity = check_profanity_audio('recording.webm')
        videoProfanity = check_profanity_video('recording.webm')
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
    print('recieved something')
    data = request.json.get('data')
    if data:
        return check_profanity(data)

if __name__ == '__main__':
    app.run(debug=True)
