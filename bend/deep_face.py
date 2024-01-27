import cv2
from deepface import DeepFace
import pandas as pd
import csv
import json
import os

import firebase_admin
from firebase_admin import credentials, firestore, storage

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
  'fastmtcnn',
]
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

face_representations_file = os.path.join('model_faces', 'representations_vgg_face.pkl')
if os.path.exists(face_representations_file):
    os.remove(face_representations_file)


# Use the service account key JSON file to authenticate
file_name = 'netwark-10966-firebase-adminsdk-cje0h-e979d7c50d.json'
file_path = os.path.join(os.path.dirname(__file__), file_name)
cred = credentials.Certificate(file_path)
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

# Download images from Firebase Storage to local "model_faces" directory
user_images_bucket_name = "netwark-10966.appspot.com"
user_images_bucket = storage.bucket(user_images_bucket_name)
blobs = user_images_bucket.list_blobs()
local_model_faces_directory = "model_faces/"

blobs = user_images_bucket.list_blobs()

# Download images
for blob in blobs:
    # Create local file path
    print(blob)
    local_file_path = f"{local_model_faces_directory}{blob.name}"
    print(local_file_path)

    # Download the blob to the local file
    blob.download_to_filename(local_file_path)

    print(f"Downloaded {blob.name} to {local_file_path}")




# result = DeepFace.verify(img1_path = "model_faces/Pranav_Tadepalli.png", img2_path = "pranav_seen.jpg",detector_backend = backends[7])

# Initialize the webcam
cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera

def get_face_coords(result):
    # Initialize an empty dictionary to store the results
    result_dict = {}

    # Iterate through rows in the DataFrame
    for index, row in result.iterrows():
        # Extract information from the row
        identity = row['identity']
        source_x = row['source_x']
        source_y = row['source_y']
        source_w = row['source_w']
        source_h = row['source_h']

        # Calculate the ratio of the top of the head relative to the full resolution
        ratio_x = source_x / 1920  # Assuming full resolution width is 1920
        ratio_y = source_y / 1080  # Assuming full resolution height is 1080

        # Store the result in the dictionary
        result_dict[identity.split('/')[-1].split('.')[0]] = (ratio_x, ratio_y)
    return result_dict

def write_csv(coordinates_json):
    csv_filename = "../graphics/output.csv"
    # Iterate through the given JSON with coordinates
    name, coordinates = list(coordinates_json.items())[0] if coordinates_json else ("","")
    # Fetch user data from Firestore
    user_doc = db.collection('users').document(name).get()
    print(user_doc)
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["name", "first_name", "last_name", "hometown", "team_role", "position", "interests", "organization", "contact", "image", "xcoord", "ycoord"])
            # Write a row to the CSV file
            csv_writer.writerow([
                name,
                user_data.get("first_name", ""),
                user_data.get("last_name", ""),
                user_data.get("hometown", "").replace(",",""),
                user_data.get("team_role", ""),
                user_data.get("position", ""),
                " ".join(user_data.get("interests", [])),
                user_data.get("organization", ""),
                user_data.get("contact", ""),
                user_data.get("image", ""),
                coordinates[0],  # xcoord
                coordinates[1]   # ycoord
            ])

while True:
    # Capture video frame-by-frame
    ret, frame = cap.read()
        # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Create a three-channel representation of the grayscale image
    gray_rgb = cv2.merge([gray, gray, gray])

    frame = gray_rgb

    # Display the resulting frame
    cv2.imwrite('curr.jpg', frame)
    try:
        result = DeepFace.find("curr.jpg",db_path = "model_faces",detector_backend = backends[7]) #7
        result = result[0]
        print(result)

        face_dict = get_face_coords(result)
        write_csv(face_dict)
        print(face_dict)
    except ValueError:
        print("NoFace")



    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()



