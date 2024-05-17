"""
Description: The script reads a VIA project JSON file and finds images without annotations and counts the annotations for each image.
Author: Elia Pacioni
Date: 2024-05-17
Version: 1.0
"""
import argparse
import json
from collections import defaultdict

def load_via_json(file_path):
    """
    Load data from the VIA project JSON file
    :param file_path: Path to the VIA project JSON file (str)
    :return: Data from the VIA project JSON file
    """
    with open(file_path) as file:
        return json.load(file)

# Process VIA project data to find unannotated images and count annotations for each image
def process_via_data(data):
    """
    Process VIA project data to find unannotated images and count annotations for each image
    :param data: Data from the VIA project JSON file
    :return: List of unannotated images and dictionary of annotation counts for each image
    """

    annotation_counts = defaultdict(int)

    # Iterate through each file entry in the VIA project
    for file_id, file_info in data["_via_img_metadata"].items():
        # Count the number of regions (annotations) for each image
        annotation_counts[file_id] = len(file_info["regions"])

    # Find images without annotations
    unannotated_images = [file_id for file_id, count in annotation_counts.items() if count == 0]

    return unannotated_images, annotation_counts

def print_via_results(unannotated_images, annotation_counts, data):
    """
    Print the results of the VIA project data processing
    :param unannotated_images: list of unannotated images
    :param annotation_counts: dictionary of annotation counts for each image
    :param data: Data from the VIA project JSON file
    :return: None
    """
    if unannotated_images:
        print("Images without annotations:")
        for file_id in unannotated_images:
            print(f"ID: {file_id}, Filename: {data['_via_img_metadata'][file_id]['filename']}")
    else:
        print("All images have annotations.")

    print("Total images without annotations:", len(unannotated_images))

    print("\nAnnotation counts for each image:")
    for file_id, count in annotation_counts.items():
        print(f"Image ID: {file_id}, Filename: {data['_via_img_metadata'][file_id]['filename']}, Annotation Count: {count}")
    
    print(f"\nTotal annotations: {sum(annotation_counts.values())}")

def main():
    parser = argparse.ArgumentParser(description='VIA Annotation Check')
    parser.add_argument('file_path', type=str, help='Path to the VIA project JSON file')
    args = parser.parse_args()

    # Load VIA project data
    data = load_via_json(args.file_path)

    # Process VIA project data
    unannotated_images, annotation_counts = process_via_data(data)

    # Print results
    print_via_results(unannotated_images, annotation_counts, data)

if __name__ == "__main__":
    main()
