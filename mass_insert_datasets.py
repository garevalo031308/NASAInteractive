import os
import shutil
import sqlite3

# Path to your SQLite3 database file
db_path = 'db.sqlite3'

# Connect to the SQLite3 database
conn = sqlite3.connect(db_path)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Path to the root dataset directory
dataset_root = 'Datasets'

# Traverse the directory structure
for dataset_name in os.listdir(dataset_root):
    dataset_path = os.path.join(dataset_root, dataset_name)
    if os.path.isdir(dataset_path):
        # Get the dataset ID from the database
        cursor.execute("SELECT id FROM NASAMainPage_dataset WHERE dataset_name = ?", (dataset_name,))
        dataset_id = cursor.fetchone()
        if dataset_id:
            dataset_id = dataset_id[0]
            for class_name in os.listdir(dataset_path):
                class_path = os.path.join(dataset_path, class_name)
                if os.path.isdir(class_path):
                    # Get the class ID from the database
                    cursor.execute("SELECT id FROM NASAMainPage_datasetclasses WHERE dataset_class_name = ? AND dataset_id = ?", (class_name, dataset_id))
                    class_id = cursor.fetchone()
                    if class_id:
                        class_id = class_id[0]
                        for image_name in os.listdir(class_path):
                            image_path = os.path.join(class_path, image_name)
                            if os.path.isfile(image_path):
                                # Define the destination path for the image
                                dest_dir = os.path.join('NASAMainPage','static', 'Datasets', dataset_name, class_name)
                                os.makedirs(dest_dir, exist_ok=True)
                                dest_path = os.path.join(dest_dir, image_name)

                                # Copy the image to the destination directory
                                shutil.copy(image_path, dest_path)

                                # Insert the image record into the Picture table
                                cursor.execute("""
                                    INSERT INTO NASAMainPage_picture (dataset_id, dataset_class_id, image, image_name)
                                    VALUES (?, ?, ?, ?)
                                """, (dataset_id, class_id, dest_path, image_name))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()