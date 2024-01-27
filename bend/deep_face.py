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

result = DeepFace.verify(img1_path = "model_faces/Pranav_Tadepalli.png", img2_path = "pranav_seen.jpg",detector_backend = backends[4])
print(result)