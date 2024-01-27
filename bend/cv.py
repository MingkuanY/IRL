import face_recognition
import os

all_faces = []
all_people = os.listdir("model_faces")
for file in all_people:
    picture = face_recognition.load_image_file(f"model_faces/{file}")
    encoding = face_recognition.face_encodings(picture)[0]
    all_faces.append(encoding)

# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

unknown_picture = face_recognition.load_image_file("pranav_seen.jpg")
unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

# Now we can see the two face encodings are of the same person with `compare_faces`!

results = all_people[face_recognition.compare_faces(all_faces, unknown_face_encoding).index(True)]
print(results)