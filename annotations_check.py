"""
Description: The script reads COCO and VGG JSON files and compares the number of annotations for each image.
Author: Elia Pacioni
Date: 2024-05-17
Version: 1.0
"""
import argparse
import coco_annotation_check as coco
import via_annotation_check as vgg
from tabulate import tabulate
from termcolor import colored

def compare_annotations(vgg_file_path, coco_file_path):
    """
    Compare COCO and VGG annotations
    :param vgg_file_path: Path to the VIA project JSON file (str)
    :param coco_file_path: Path to the COCO JSON file (str)
    :return: None
    """
    # Load COCO data
    coco_data = coco.load_coco_json(coco_file_path)
    unannotated_images_coco, annotation_counts_coco, id_to_filename_coco = coco.process_images_and_annotations(coco_data)

    # Create a mapping from filename to COCO annotation counts and include COCO IDs
    filename_to_coco_anno = {id_to_filename_coco[image_id]: (count, image_id) for image_id, count in annotation_counts_coco.items()}

    # Load VGG data
    vgg_data = vgg.load_via_json(vgg_file_path)
    unannotated_images_vgg, annotation_counts_vgg = vgg.process_via_data(vgg_data)

    # Create a mapping from filename to VGG annotation counts
    filename_to_vgg_anno = {file_info['filename']: count for file_id, count in annotation_counts_vgg.items() for file_info in [vgg_data['_via_img_metadata'][file_id]]}

    # Create a combined result
    combined_results = []

    # Use the union of filenames in both datasets
    all_filenames = set(filename_to_coco_anno.keys()).union(set(filename_to_vgg_anno.keys()))

    total_coco_annotations = 0
    total_vgg_annotations = 0

    # Iterate through all filenames
    for filename in all_filenames:
        coco_anno, coco_id = filename_to_coco_anno.get(filename, (0, None))
        vgg_anno = filename_to_vgg_anno.get(filename, 0)
        difference = vgg_anno - coco_anno
        combined_results.append({
            "image": filename,
            "coco_anno": coco_anno,
            "vgg_anno": vgg_anno,
            "difference": difference,
            "coco_id": coco_id
        })
        total_coco_annotations += coco_anno
        total_vgg_annotations += vgg_anno

    # Sort the results by COCO ID
    combined_results.sort(key=lambda x: (x["coco_id"] is None, x["coco_id"]))

    # Prepare the table data
    table_data = []
    for result in combined_results:
        coco_id_str = str(result['coco_id']) if result['coco_id'] is not None else "N/A"
        row = [
            result['image'],
            coco_id_str,
            result['vgg_anno'],
            result['coco_anno'],
            result['difference']
        ]
        if result['vgg_anno'] == 0 and result['coco_anno'] == 0:
            row = [colored(cell, 'yellow') for cell in row]
        elif result['difference'] == 0 and result['vgg_anno'] > 0 and result['coco_anno'] > 0:
            row = [colored(cell, 'green') for cell in row]
        elif result['difference'] > 0:
            row = [colored(cell, 'red') for cell in row]
        table_data.append(row)

    # Add the total row
    table_data.append([
        "Total",
        "",
        total_vgg_annotations,
        total_coco_annotations,
        total_vgg_annotations - total_coco_annotations
    ])

    # Print the table
    headers = ["Image", "COCO ID", "VGG Annotations", "COCO Annotations", "Difference"]
    print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="center", numalign="center"))

def main():
    parser = argparse.ArgumentParser(description='Compare COCO and VGG annotations.')
    parser.add_argument('vgg_file_path', type=str, help='Path to the VGG JSON file')
    parser.add_argument('coco_file_path', type=str, help='Path to the COCO JSON file')

    args = parser.parse_args()

    compare_annotations(args.vgg_file_path, args.coco_file_path)

if __name__ == "__main__":
    main()
