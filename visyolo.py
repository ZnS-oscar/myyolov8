import os
import cv2

def visualize_yolo_labels(labels_dir, images_dir, output_dir, class_names):
    """
    Visualize YOLO labels on images and save the results.
    
    Args:
    - labels_dir: Directory containing YOLO label files (.txt).
    - images_dir: Directory containing corresponding images.
    - output_dir: Directory to save visualized images.
    - class_names: List of class names corresponding to class IDs.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over label files
    for label_file in os.listdir(labels_dir):
        if not label_file.endswith('.txt'):
            continue

        # Get the corresponding image file
        image_file = label_file.replace('.txt', '.jpg')  # Adjust for your image extension if needed
        image_path = os.path.join(images_dir, image_file)
        if not os.path.exists(image_path):
            print(f"Image not found for {label_file}, skipping...")
            continue

        # Load the image
        image = cv2.imread(image_path)
        img_height, img_width, _ = image.shape

        # Read the label file
        label_path = os.path.join(labels_dir, label_file)
        with open(label_path, 'r') as f:
            lines = f.readlines()

        # Draw each bounding box on the image
        for line in lines:
            parts = line.strip().split()
            class_id, center_x, center_y, width, height = map(float, parts)
            class_id = int(class_id)

            # Convert normalized YOLO bbox to pixel coordinates
            x1 = int((center_x - width / 2) * img_width)
            y1 = int((center_y - height / 2) * img_height)
            x2 = int((center_x + width / 2) * img_width)
            y2 = int((center_y + height / 2) * img_height)

            # Draw the bounding box
            color = (0, 255, 0)  # Green color for the bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            # Add the label text
            label_text = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"
            cv2.putText(image, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Save the visualized image
        output_path = os.path.join(output_dir, image_file)
        cv2.imwrite(output_path, image)

    print(f"Visualized images saved to {output_dir}")

# Example usage
labels_dir = "/home/lhx/myyolov8/labels"      # Directory containing YOLO .txt label files
images_dir = "/home/lhx/myyolov8/data_zoo/pcbhbb_slice_coco/images"           # Directory containing images
output_dir = "vis"                      # Directory to save visualized images
class_names = ["class1", "class2", "class3","class4", "class5", "class6"]  # Replace with your class names

visualize_yolo_labels(labels_dir, images_dir, output_dir, class_names)
