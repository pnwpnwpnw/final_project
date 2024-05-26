import numpy as np
from PIL import Image
import os
import cv2

def train_classifier(name):
    # Directory to save the classifier file
    directory = "./data/classifiers/"
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory Created")
    
    # Read all the images in the custom data-set
    path = os.path.join(os.getcwd(), "data", "faces", name)

    faces = []
    ids = []
    pictures = []

    # Store images in a numpy format and ids of the user on the same index in imageNp and id lists
    for root, dirs, files in os.walk(path):
        for file in files:
            pictures.append(os.path.join(root, file))

    for pic in pictures:
        img = Image.open(pic).convert('L')
        image_np = np.array(img, 'uint8')
        id = int(os.path.split(pic)[-1].split(name)[0])
        faces.append(image_np)
        ids.append(id)

    ids = np.array(ids)
    
    # Train the classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)

    # Save the classifier
    classifier_file = os.path.join(directory, f"{name}_classifier.xml")
    try:
        clf.write(classifier_file)
        print("Classifier saved successfully")
    except Exception as e:
        print(f"Error saving classifier: {e}")
