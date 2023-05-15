import os
import subprocess
import shutil
from nsfw_detector import predict
# nsfw_model = predict.load_model(r"C:\Users\goelm\Downloads\february_2019_nsfw.299x299.h5")
nsfw_model = predict.load_model(r"C:\Users\Abhishek\Downloads\february_2019_nsfw.299x299 (1).h5")
import cv2
watch_cascade=cv2.CascadeClassifier(r'cascade.xml')

def check_gun(img_path):
    img = cv2.imread(img_path)
    # img = cv2.imread('framesd.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform object detection
    watches = watch_cascade.detectMultiScale(gray, 1.3, 50, minSize = (100,100))
    for (x, y, w, h) in watches:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # # Display the image with detected objects
    # cv2.imshow('img', img)
    # cv2.waitKey(0)  # Wait until a key is pressed
    # cv2.destroyAllWindows()

    # Check if a gun is displayed
    return len(watches) > 0

def extract_frames(video_path, output_dir, num_frames=5):
    # Create the output directory, if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    subprocess.run(['ffmpeg', '-i', video_path, '-vf', 'fps='+str(num_frames), f'{output_dir}/frame-%04d.png'])

def check_neut(result, fileName):
    if(result[fileName]['hentai']>0.6 or result[fileName]['porn']>0.6 or result[fileName]['sexy']>0.6):
        return True
    else:
        return False

def process_frames(frames_dir):
    for filename in os.listdir(frames_dir):
        if filename.endswith('.png'):
            frame_path = os.path.join(frames_dir, filename)
            if check_neut(predict.classify(nsfw_model, frame_path, 299), frame_path) or check_gun(frame_path):
                shutil.rmtree(frames_dir)
                return True
    #delete frame directory and all files in it
    shutil.rmtree(frames_dir)
    return False
# Example usage
def check_profanity_video(video_file_path):
    output_dir = video_file_path.split('.')[0]
    extract_frames(video_file_path, output_dir)
    return process_frames(output_dir)
