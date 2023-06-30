import os
import cv2
from tqdm import tqdm

# Predefined directories for input images and output folders
input_directory = 'E:/eventpictures'
output_directory = 'D:/picturesscript'


# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Iterate through the input directory
for filename in tqdm(os.listdir(input_directory)):
    # Read the image file
    image_path = os.path.join(input_directory, filename)
    try:
        image = cv2.imread(image_path)

        if image is None:
            # print(f"Failed to read image: {image_path}")
            continue

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Check if any faces are detected
        if len(faces) > 0:
            # Create a directory for the detected faces if it doesn't exist
            face_directory = os.path.join(output_directory, f"{filename.split('.')[0]}_faces")
            if not os.path.exists(face_directory):
                os.makedirs(face_directory)

            # Save the original image into the face directory
            face_path = os.path.join(face_directory, filename)
            cv2.imwrite(face_path, image)

            print(f"Original image '{filename}' saved to '{face_directory}'")

        else:
            pass

    except Exception as e:
        print(f"Error processing image: {filename} - {str(e)}")
