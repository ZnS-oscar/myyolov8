import math
import os

def calculate_vertices(x_c, y_c, width, height, angle):
    # Convert angle from degrees to radians
    angle_rad = math.radians(angle)

    # Calculate half dimensions
    half_width = width / 2
    half_height = height / 2

    # Calculate the offset of each corner relative to the center
    corners = [
        (-half_width, -half_height),
        (-half_width, half_height),
        (half_width, half_height),
        (half_width, -half_height),
    ]

    # Calculate rotated corner positions
    vertices = []
    for dx, dy in corners:
        x = x_c + (dx * math.cos(angle_rad)) - (dy * math.sin(angle_rad))
        y = y_c + (dx * math.sin(angle_rad)) + (dy * math.cos(angle_rad))
        vertices.append((x, y))

    return vertices


def process_bounding_boxes(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if not line or ':' not in line:
                continue
            # Parse the line
            label, coords = line.split(':')
            x_c, y_c, width, height, angle = map(float, coords.split(','))

            # Calculate vertices
            vertices = calculate_vertices(x_c, y_c, width, height, angle)

            # Format vertices to string
            vertex_str = ' '.join(f'{vx:.2f} {vy:.2f}' for vx, vy in vertices)

            # Write to output file
            outfile.write(f'{label[0]} {vertex_str}\n')

def process_all_files_in_folder(input_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join('D:\emppool\obb', f"{os.path.splitext(filename)[0]}_OBB_format.txt")
            process_bounding_boxes(input_file, output_file)
# Replace 'input.txt' with the path to your input file
# Replace 'output.txt' with the desired path for the output file
process_all_files_in_folder('D:\emppool\\bboxlbl')