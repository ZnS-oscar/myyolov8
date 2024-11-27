import json
import os

def coco_to_yolo(coco_json_path, output_dir):
    # Load COCO JSON
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
    
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Map category IDs to continuous indices for YOLO
    category_mapping = {cat['id']: i for i, cat in enumerate(coco_data['categories'])}
    
    # Process each annotation
    image_annotations = {}
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        category_id = category_mapping[ann['category_id']]
        bbox = ann['bbox']  # [x, y, width, height]
        
        # Convert COCO bbox to YOLO format
        x, y, width, height = bbox
        image_info = next(img for img in coco_data['images'] if img['id'] == image_id)
        img_width, img_height = image_info['width'], image_info['height']
        center_x = (x + width / 2) / img_width
        center_y = (y + height / 2) / img_height
        norm_width = width / img_width
        norm_height = height / img_height
        
        # Prepare YOLO annotation line
        yolo_annotation = f"{category_id} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}"
        
        # Group annotations by image
        if image_id not in image_annotations:
            image_annotations[image_id] = []
        image_annotations[image_id].append(yolo_annotation)
    
    # Write YOLO annotation files
    for img in coco_data['images']:
        image_id = img['id']
        file_name = os.path.splitext(img['file_name'])[0] + '.txt'
        output_file_path = os.path.join(output_dir, file_name)
        with open(output_file_path, 'w') as f:
            if image_id in image_annotations:
                f.write("\n".join(image_annotations[image_id]))
    
    print(f"Converted annotations saved to {output_dir}")

# Example usage
coco_json_path = "/home/lhx/myyolov8/data_zoo/pcbhbb_slice_coco/images.json"  # Path to the COCO JSON file
output_dir = "labels"        # Directory to save YOLO annotations
coco_to_yolo(coco_json_path, output_dir)
