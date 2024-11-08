import keras
import tensorflow as tf
import numpy as np
from sklearn.metrics import accuracy_score

# Load the model
reconstructed_model = keras.models.load_model("VGG16F1.keras")

# Load the image
image_path = "five-fold-cv6/fold-1/2345-as-training/streak/ESP_012971_2015_RED-0005.jpg"
true_label = "streak"

# Class names
class_names = ["bright_dune", "crater", "dark_dune", "edge", "other", "streak"]

# Load and preprocess the image
img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = np.expand_dims(img_array, 0)
img_array = img_array / 255.0

# Make prediction
predictions = reconstructed_model.predict(img_array)
predicted_label = class_names[np.argmax(predictions[0])]

# Calculate the accuracy score
accuracy = accuracy_score([true_label], [predicted_label]) * 100

# Print the results
print(f"Accuracy: {accuracy:.2f}%")
print(f"Predicted label: {predicted_label}")