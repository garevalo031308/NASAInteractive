document.addEventListener('DOMContentLoaded', () => {
    const statusDiv = document.getElementById('loadedornot');
    statusDiv.innerText = 'Script loaded. Ready to upload model.';

    const resultDiv = document.getElementById('prediction-result');

    // Load the TensorFlow.js model from the specified directory
    async function loadModelFromDirectory(directoryPath) {
        try {
            const model = await tf.loadLayersModel(directoryPath);
            console.log('Model loaded successfully');
            statusDiv.innerText = 'Model loaded successfully';
            return model;
        } catch (error) {
            console.error('Error loading the model:', error);
            statusDiv.innerText = 'Error loading the model. Please try again later.';
        }
    }

    // Load and preprocess the images
    async function loadImage(filePath) {
        const img = new Image();
        img.src = filePath;
        await new Promise((resolve) => {
            img.onload = resolve;
        });
        return tf.browser.fromPixels(img)
            .resizeNearestNeighbor([224, 224]) // Change the size according to your model's input size
            .toFloat()
            .expandDims();
    }

    // Predict the class of the image
    async function predictImage(model, imagePath) {
        const imageTensor = await loadImage(imagePath);
        const prediction = model.predict(imageTensor);
        return prediction.argMax(-1).dataSync()[0];
    }

    // Load the model and make a prediction
    (async () => {
        const modelDirectory = '/static/models/VGG1/model.json'; // Change this to the path of your model's JSON file
        const model = await loadModelFromDirectory(modelDirectory);
        const classes = ['bright_dune', 'crater', 'dark_dune', 'edge', 'other', 'streak'];
        const imagePath = '/static/Datasets/HiRISE/Streak/ESP_012971_2015_RED-0072.jpg'; // Change this to the path of your image
        const predictedClassIndex = await predictImage(model, imagePath);
        const predictedClass = classes[predictedClassIndex];
        console.log(`Predicted class: ${predictedClass}`);
        resultDiv.textContent = `Predicted class: ${predictedClass}`;
    })();
});