"""
Description: The script reads a VIA project JSON file and finds images without annotations and counts the annotations for each image.
Author: Elia Pacioni
Date: 2024-05-17
Version: 1.0
"""
import json
import argparse
from collections import defaultdict

def load_coco_json(file_path):
    """
    Load data from the COCO JSON file
    :param file_path: Path to the COCO JSON file (str)
    :return: Data from the COCO JSON file
    """
    with open(file_path) as file:
        return json.load(file)

def process_images_and_annotations(data):
    """
    Find images without annotations and count annotations for each image
    :param data: Data from the COCO JSON file
    :return: List of unannotated images, dictionary of annotation counts for each image, and mapping from image ID to filename
    """
    images = data["images"]
    annotations = data["annotations"]

    # Create a mapping from image ID to filename
    id_to_filename = {image["id"]: image["file_name"] for image in images}

    # Get the IDs of the annotated images and count annotations
    annotation_counts = defaultdict(int)
    for annotation in annotations:
        annotation_counts[annotation["image_id"]] += 1

    # Find images without annotations
    unannotated_images = [image for image in images if annotation_counts[image["id"]] == 0]

    return unannotated_images, annotation_counts, id_to_filename

def print_results(unannotated_images, annotation_counts, id_to_filename):
    """
    Print the results of the COCO dataset processing
    :param unannotated_images: List of unannotated images
    :param annotation_counts: Dictionary of annotation counts for each image
    :param id_to_filename: Mapping from image ID to filename
    :return: None
    """
    if unannotated_images:
        print("Images without annotations:")
        for image in unannotated_images:
            print(f"ID: {image['id']}, Filename: {image['file_name']}")
    else:
        print("All images have annotations.")

    print("Total images without annotations:", len(unannotated_images))

    print("\nAnnotation counts for each image:")
    for image_id, count in annotation_counts.items():
        filename = id_to_filename.get(image_id, "Unknown")
        print(f"Image ID: {image_id}, Filename: {filename}, Annotation Count: {count}")

    img_count = 0
    for image_id, count in annotation_counts.items():
        if count < 5:
            img_count += 1
    print(f"Total annotations: {sum(annotation_counts.values())}")

def main():
    parser = argparse.ArgumentParser(description="Check COCO dataset annotations")
    parser.add_argument("file_path", help="Path to the COCO JSON file")
    args = parser.parse_args()

    # Load data
    data = load_coco_json(args.file_path)

    # Process images and annotations
    unannotated_images, annotation_counts, id_to_filename = process_images_and_annotations(data)

    # Print results
    print_results(unannotated_images, annotation_counts, id_to_filename)

if __name__ == "__main__":
    main()
