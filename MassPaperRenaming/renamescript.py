import os
from PyPDF2 import PdfReader as pdf_reader
import shutil

# specify the input and output folder paths
input_folder_path = r"C:\Users\Cr7th\Desktop\dr"
output_folder_path = r"C:\Users\Cr7th\Desktop\DronesNames"
titles=[]
# create the output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# iterate over each file in the input folder
for filename in os.listdir(input_folder_path):
    # check if the file is a PDF
    if filename.endswith(".pdf"):
        file_path = os.path.join(input_folder_path, filename)

        # open the PDF and extract the title
        with open(file_path, 'rb') as file:
            pdf = pdf_reader(file)
            titles.append(pdf.metadata.title)
            titles.append(",")
            print(titles)
        # # create a new filename based on the title
        # if(title!=None):
        #     new_filename = title.strip().replace(" ", "_") + ".pdf"
        #     new_file_path = os.path.join(output_folder_path, new_filename)

        #     # copy the file to the output folder with the new filename
        #     shutil.copyfile(file_path, new_file_path)
            
        #     # print a message to indicate which file was renamed
        #     print(f"{filename} -> {new_filename}")
