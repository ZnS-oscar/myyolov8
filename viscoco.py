import os
import json
import cv2

def visualize_coco_labels(coco_json_path, images_dir, output_dir):
    # Load COCO JSON
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)

    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Map category IDs to category names
    category_mapping = {cat['id']: cat['name'] for cat in coco_data['categories']}

    # Process each image
    for img in coco_data['images']:
        image_path = os.path.join(images_dir, img['file_name'])
        output_path = os.path.join(output_dir, img['file_name'])
        
        # Load image
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue
        image = cv2.imread(image_path)

        # Get annotations for this image
        annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] == img['id']]
        for ann in annotations:
            bbox = ann['bbox']  # [x, y, width, height]
            category_id = ann['category_id']
            label = category_mapping[category_id]
            x, y, width, height = map(int, bbox)

            # Draw bounding box
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

            # Draw label
            label_text = f"{label}"
            cv2.putText(image, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save visualized image
        cv2.imwrite(output_path, image)

    print(f"Visualized images saved to {output_dir}")

# Example usage
coco_json_path = "path/to/your/coco.json"  # Path to COCO JSON file
images_dir = "path/to/your/images"        # Path to the folder containing images
output_dir = "vis"                        # Output directory for visualized images
visualize_coco_labels(coco_json_path, images_dir, output_dir)
