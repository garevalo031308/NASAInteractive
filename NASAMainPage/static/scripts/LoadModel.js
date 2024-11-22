document.addEventListener('DOMContentLoaded', () => {
    const statusDiv = document.getElementById('loadedornot');
    statusDiv.innerText = 'Script loaded. Ready to upload model.';

    const uploadJSONInput = document.getElementById('upload-json');
    const resultDiv = document.getElementById('prediction-result');

    // Load the TensorFlow.js model from the uploaded file
    async function loadModelFromFile(file) {
        try {
            const model = await tf.loadLayersModel(tf.io.browserFiles([file]));
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

    // Event listener for file input
    uploadJSONInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (file) {
            const model = await loadModelFromFile(file);
            const classes = ['bright_dune', 'crater', 'dark_dune', 'edge', 'other', 'streak'];
            const imagePath = 'ESP_012687_1930_RED-0005.jpg'; // Change this to the path of your image
            const predictedClassIndex = await predictImage(model, imagePath);
            const predictedClass = classes[predictedClassIndex];
            console.log(`Predicted class: ${predictedClass}`);
            resultDiv.textContent = `Predicted class: ${predictedClass}`;
        }
    });
});