import os
import random
import shutil

# Define source and destination folders (replace with your actual paths)
source_folder = "/home/user/Pictures/from"
destination_folder = "/home/user/Pictures/to"

# Set the number of pictures to move
num_pictures_to_move = 100

# Set the random seed (change this for different selections)
random.seed(1234)  # Example seed

# Get all image files from the source folder
all_images = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

# Randomly select the pictures to move
selected_images = random.sample(all_images, num_pictures_to_move)

# Move the selected pictures
for image in selected_images:
    source_path = os.path.join(source_folder, image)
    dest_path = os.path.join(destination_folder, image)
    shutil.move(source_path, dest_path)

print(f"Successfully moved {num_pictures_to_move} pictures to {destination_folder}.")