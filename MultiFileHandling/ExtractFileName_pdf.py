import os
from PyPDF2 import PdfReader as pdf_reader

# Specify the input and output location-paths
Input_Folder = "{Input-File Directory}"
files=[]

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
