import os
import shutil
import sqlite3
from zipfile import ZipFile


def get_directory_information(file_name):
    valid_extensions = {'.png', '.jpg', '.jpeg'}
    directory = {"Dataset Name": file_name}
    classes = {}
    total_images = 0
    for class_name in os.listdir(file_name):
        class_path = os.path.join(file_name, class_name)
        if os.path.isdir(class_path):
            image_count = 0
            for image in os.listdir(class_path):
                if os.path.splitext(image)[1].lower() in valid_extensions:
                    image_count += 1
                    total_images += 1
            classes[class_name] = image_count
    directory["Total Images"] = total_images
    return directory, classes


def check_if_dataset_in_database(dataset_name, total_images, cursor, conn):
    cursor.execute("SELECT id FROM NASAMainPage_dataset WHERE dataset_name = ?", (dataset_name,))
    dataset_id = cursor.fetchone()
    if not dataset_id:
        cursor.execute("INSERT INTO NASAMainPage_dataset (dataset_name, dataset_number_of_images) VALUES (?, ?)",
                       (dataset_name, total_images))
        conn.commit()
        cursor.execute("SELECT id FROM NASAMainPage_dataset WHERE dataset_name = ?", (dataset_name,))
        dataset_id = cursor.fetchone()
    return dataset_id[0]


def insert_class_and_images(cursor, conn, dataset_id, class_name, class_image_count, class_path, valid_extensions):
    cursor.execute("SELECT id FROM NASAMainPage_datasetclasses WHERE dataset_class_name = ? AND dataset_id = ?",
                   (class_name, dataset_id))
    class_id = cursor.fetchone()
    if not class_id:
        cursor.execute(
            "INSERT INTO NASAMainPage_datasetclasses (dataset_id, class_number_of_images, dataset_class_name) VALUES (?, ?, ?)",
            (dataset_id, class_image_count, class_name))
        conn.commit()
        cursor.execute("SELECT id FROM NASAMainPage_datasetclasses WHERE dataset_class_name = ? AND dataset_id = ?",
                       (class_name, dataset_id))
        class_id = cursor.fetchone()
    class_id = class_id[0]
    for image_name in os.listdir(class_path):
        image_path = os.path.join(class_path, image_name)
        if os.path.isfile(image_path) and os.path.splitext(image_name)[1].lower() in valid_extensions:
            # Update the image_path to include the directory structure
            updated_image_path = os.path.join('NASAMainPage', 'static', 'Datasets', dataset_id, class_name, image_name)
            cursor.execute(
                "INSERT INTO NASAMainPage_picture (image, image_name, dataset_id, dataset_class_id) VALUES (?, ?, ?, ?)",
                (updated_image_path, image_name, dataset_id, class_id))
            conn.commit()


def mass_insert(input_file_name):
    db_path = "db.sqlite3"
    file_name = input_file_name
    valid_extensions = {'.png', '.jpg', '.jpeg'}

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with ZipFile(file_name, 'r') as zipobject:
        zipobject.extractall()

    name_without_extension = os.path.splitext(file_name)[0]
    dataset_info, classes_info = get_directory_information(name_without_extension)
    dataset_id = check_if_dataset_in_database(name_without_extension, dataset_info["Total Images"], cursor, conn)

    # Define the destination directory
    dest_dir = os.path.join('NASAMainPage', 'static', 'Datasets', name_without_extension)
    os.makedirs(dest_dir, exist_ok=True)

    for class_name, class_image_count in classes_info.items():
        class_path = os.path.join(name_without_extension, class_name)
        dest_class_path = os.path.join(dest_dir, class_name)
        os.makedirs(dest_class_path, exist_ok=True)

        # Move the class directory to the destination
        for image_name in os.listdir(class_path):
            image_path = os.path.join(class_path, image_name)
            if os.path.isfile(image_path):
                shutil.move(image_path, os.path.join(dest_class_path, image_name))

        insert_class_and_images(cursor, conn, dataset_id, class_name, class_image_count, dest_class_path,
                                valid_extensions)

    cursor.close()
    conn.close()