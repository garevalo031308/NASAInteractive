import sys
import keras
import tensorflow as tf
import numpy as np
from sklearn.metrics import accuracy_score

def main(user_input):

    reconstructed_model = keras.moels.load_model("NASAMainPage/static/models/VGG16F1.keras")


if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else "No input provided"
    main(user_input)