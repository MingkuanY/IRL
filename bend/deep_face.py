from deepface import DeepFace
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
result = DeepFace.find("pranav_seen.jpg",db_path = "model_faces",detector_backend = backends[7])


print(result)