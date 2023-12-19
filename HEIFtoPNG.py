import os
import imageio
from tqdm import tqdm

HEIF_DIRECTORY = r"C:\Users\Cr7th\Pictures\Photos for conversion to JPG"
CONVERTED_DIRECTORY = r"C:\Users\Cr7th\Pictures\Converted Photos"

def convert_heif_to_png(input_directory, output_directory):
    all_files = []
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith(".heic") or file.lower().endswith(".heif"):
                all_files.append(os.path.join(root, file))

    with tqdm(total=len(all_files), desc="Converting files", unit="file") as pbar:
        for input_path in all_files:
            output_path = os.path.join(
                output_directory, 
                os.path.splitext(os.path.basename(input_path))[0] + ".png"
            )
            try:
                img = imageio.imread(input_path)
                imageio.imwrite(output_path, img)
                pbar.update(1)
            except Exception as e:
                print(f"Error converting {input_path}: {e}")

# Convert HEIF images from HEIF_DIRECTORY to PNG and save them in CONVERTED_DIRECTORY
convert_heif_to_png(HEIF_DIRECTORY, CONVERTED_DIRECTORY)
