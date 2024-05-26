# VIA annotations checker

The creation of accurate annotations is of paramount importance for the efficacy of machine learning algorithms that rely on them. However, it is relatively simple to encounter errors in annotations that appear to be correct but are, in fact, formally flawed.
This project enables the user to ascertain the number of annotations associated with each image in the VIA or COCO project. Additionally, it facilitates a comparison between the two versions, thereby facilitating the identification of any errors.

## Structure of the project
The project is structured as follows:

- `README.md`: This file.
- `LICENSE`: The license file.
- `requirements.txt`: The file containing the required libraries.
- `coco_annotations_checker.py`: The script that verifies the COCO annotations.
- `via_annotations_checker.py`: The script that verifies the VIA annotations.
- `annotations_checker.py`: The script compares the VIA and COCO annotations and presents a summary table.


## How to use the project

This project can be utilized to examine either VIA annotations or COCO annotations, or both.

In accordance with the selected use case, the appropriate script must be invoked. 
The following section outlines the necessary steps to configure the environment and execute the project.

### 1. Python version and packages required

The code was tested with python version 3.12.
To install the required packages, run the following command in the terminal:

```python -m pip install -r requirements.txt```

### 3. How to run the script
The following command should be employed to execute the entirety of the script:

```python annotations_checker.py <path_to_via_annotations.json> <path_to_coco_annotations.json>```

Otherwise, you can use the script for VIA annotations: 
    
```python via_annotations_checker.py <path_to_via_annotations.json>```

Or for COCO annotations:

```python coco_annotations_checker.py <path_to_coco_annotations.json>```

