from deepface import DeepFace
import os

# Specify the folder containing the images for the database
database_folder = "model_faces"

# Use the build_database function to create the database
DeepFace.build_database(database_folder)