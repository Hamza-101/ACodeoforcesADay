import os
from PyPDF2 import PdfReader as pdf_reader

# Specify the input and output location-paths
Input_Folder = "C:/Users/Cr7th/Desktop/"
Output_Folder = "C:/Users/Cr7th/Desktop/"
files=[]


# Create the output folder if it doesn't exist
if not os.path.exists(Output_Folder):
    os.makedirs(Output_Folder)

# Iterate over each file at the input path
for Output_Folder in os.listdir(Input_Folder):

    # Check the file extension if PDF or not
    if Output_Folder.endswith(".pdf"):
        FilePath = os.path.join(Input_Folder, Output_Folder)

        # Open the PDF and extract the title
        with open(FilePath, 'rb') as file:
            pdf = pdf_reader(file)
            files.append(pdf.metadata.title)
            files.append(",")
            print(files)
