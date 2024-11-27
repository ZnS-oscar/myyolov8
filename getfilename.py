import os

# Define the folder path and output file
folder_path = '/home/lhx/myyolov8/data_zoo/pcbhbb_slice_coco/images'
output_file = 'valhbb.txt'

# Open the output file to write the filtered filenames
with open(output_file, 'w') as f:
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the filename does not start with '160'
        if filename.startswith('160'):
            # Write the filename to the txt file
            f.write(filename + '\n')

print(f"Filtered filenames have been saved to {output_file}.")
