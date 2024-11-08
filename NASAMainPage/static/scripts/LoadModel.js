import * as tf from '@tensorflow/tfjs';

let model;

// Function to load the model with error handling
async function loadModel() {
    try {
        model = await tf.loadLayersModel('/static/models/VGG16F1/model.json');
        console.log('Model loaded successfully');
    } catch (error) {
        console.error('Error loading the model:', error);
        document.getElementById('prediction-result').innerText = 'Error loading the model. Please try again later.';
    }
}

// Function to load and preprocess the image
async function loadImage(imagePath) {
    const img = new Image();
    img.src = imagePath;
    await new Promise((resolve) => {
        img.onload = resolve;
    });

    return tf.browser.fromPixels(img)
        .resizeNearestNeighbor([224, 224]) // Resize the image to the required size
        .toFloat()
        .div(tf.scalar(255.0)) // Normalize the image
        .expandDims();
}

// Function to make a prediction
async function predictImage(imagePath) {
    try {
        const imageTensor = await loadImage(imagePath);
        const predictions = model.predict(imageTensor);
        const predictedIndex = tf.argMax(predictions, -1).dataSync()[0];


        // Class names
        const classNames = ["bright_dune", "crater", "dark_dune", "edge", "other", "streak"];
        const predictedLabel = classNames[predictedIndex];

        // Update the HTML element with the prediction result
        document.getElementById('prediction-result').innerText = `Predicted label: ${predictedLabel}`;
    } catch (error) {
        console.error('Error making prediction:', error);
        document.getElementById('prediction-result').innerText = 'Error making prediction. Please try again later.';
    }
}

// Load the model and make a prediction
await loadModel();
const imagePath = 'NASAMainPage/static/Datasets/HiRISE/Crater/ESP_011386_2065_RED-0026.jpg';
await predictImage(imagePath);