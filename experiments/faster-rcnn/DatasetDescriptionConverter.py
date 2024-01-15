# import json
#
#
#
# with open("/home/vorkov/Workspace/Python/TrafficSignDetection/experiments/russianTrafficSigns/val_anno.json", 'r') as json_file:
#     data = json.load(json_file)
#
# annotations = data['annotations']
# images = data['images']
#
# output_lines = []
#
# for annotation in annotations:
#     image_id = annotation['image_id']
#     image_info = next(image for image in images if image['id'] == image_id)
#
#     file_name = image_info['file_name']
#     bbox = annotation['bbox']
#
#     output_line = f"{file_name};{bbox[0]};{bbox[1]};{bbox[0] + bbox[2]};{bbox[1] + bbox[3]};{annotation['category_id']}"
#     output_lines.append(output_line)
#
# with open("/home/vorkov/Workspace/Python/TrafficSignDetection/experiments/russianTrafficSigns/val_labels.txt", 'w') as output_file:
#     output_file.write('\n'.join(output_lines))


import os



def check_file_existence(file_path):
    return os.path.exists(file_path)


def get_files_from_dataset(dataset_path):
    with open(dataset_path, 'r') as file:
        lines = file.readlines()

    return set(line.split(';')[0] for line in lines)


def get_files_in_directory(directory_path):
    return set("images/" + file_name for file_name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file_name)))


def check_dataset_files(dataset_path, additional_dataset_path, directory_X):
    dataset_files = get_files_from_dataset(dataset_path)
    additional_files = get_files_from_dataset(additional_dataset_path)
    directory_X_files = get_files_in_directory(directory_X)

    missing_files = directory_X_files - (dataset_files | additional_files)
    counter = 1
    for file_name in missing_files:
        file_path = os.path.join("/experiments/russianTrafficSigns/images/", file_name)
        os.remove(file_path)
        print(f"File does not appear in any dataset:{counter} {file_name} ")
        counter += 1


# Пример использования:
output_dataset_path = "/home/vorkov/Workspace/Python/TrafficSignDetection/experiments/russianTrafficSigns/train_labels.txt"
additional_dataset_path = "/home/vorkov/Workspace/Python/TrafficSignDetection/experiments/russianTrafficSigns/val_labels.txt"
directory_X = "/home/vorkov/Workspace/Python/TrafficSignDetection/experiments/russianTrafficSigns/images/images"
check_dataset_files(output_dataset_path, additional_dataset_path, directory_X)