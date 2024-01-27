import cv2
from deepface import DeepFace
import pandas as pd
import csv
import json

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

# result = DeepFace.verify(img1_path = "model_faces/Pranav_Tadepalli.png", img2_path = "pranav_seen.jpg",detector_backend = backends[7])

# Initialize the webcam
cap = cv2.VideoCapture(1)  # 0 corresponds to the default camera

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
    # Read data from people.json file
    with open('people.json', 'r') as people_file:
        people_json = json.load(people_file)

    # Prepare CSV file
    csv_filename = "../graphics/output.csv"

    # Write header to CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["name", "interests", "hackathon team role", "organization", "tools", "linkedin", "hometown", "occupation", "xcoord", "ycoord"])

        # Iterate through the given JSON with coordinates
        for name, coordinates in coordinates_json.items():
            # Get the person's information from the people JSON
            person_info = people_json.get(name, {})

            # Write a row to the CSV file
            csv_writer.writerow([
                name,
                " ".join(person_info.get("interests", [])),
                person_info.get("hackathon_team_role", ""),
                person_info.get("organization", ""),
                " ".join(person_info.get("tools", [])),
                person_info.get("linkedin", ""),
                person_info.get("hometown", "").replace(","," "),
                person_info.get("occupation", ""),
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



