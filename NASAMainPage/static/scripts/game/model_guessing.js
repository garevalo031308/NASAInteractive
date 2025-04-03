document.addEventListener("DOMContentLoaded", async function() {
    const statusDiv = document.getElementById('modelguess');
    const imageElement = document.getElementById('image');
    console.log(model);

    async function loadImage(filePath, batchShape) {
        const img = new Image();
        console.log(filePath);
        img.src = filePath;
        await new Promise((resolve) => {
            img.onload = resolve;
        });
        if (!batchShape) {
            throw new Error("Batch shape is not defined");
        }
        return tf.browser.fromPixels(img)
            .resizeNearestNeighbor([224, 224]) // Use the batch shape here
            .toFloat()
            .expandDims();
    }

    async function predictImage(model, imagePath, batchShape) {
        const imageTensor = await loadImage(imagePath, batchShape);
        const startTime = performance.now(); // Start time
        const prediction = model.predict(imageTensor);
        const probabilities = prediction.softmax().dataSync(); // Get probabilities using softmax
        const predictedIndex = prediction.argMax(-1).dataSync()[0]; // Ensure correct index retrieval
        const endTime = performance.now(); // End time
        const predictedClass = classChoices[predictedIndex];
        const timeTaken = endTime - startTime; // Calculate time taken
        return { predictedClass, probabilities, timeTaken };
    }

    let loaded_model;
    let batchShape;
    if (localStorage.getItem('modelLoaded') === 'true') {
        loaded_model = await tf.loadLayersModel('indexeddb://' + model);
        batchShape = JSON.parse(localStorage.getItem(model + '_batchShape'));
        console.log('Retrieved batch shape from IndexedDB:', batchShape); // Debugging statement
    } else {
        const modelDirectory = '/static/models/' + model + "-" + dataset + "/model.json";
        loaded_model = await tf.loadLayersModel(modelDirectory);
        batchShape = JSON.parse(localStorage.getItem(model + '_batchShape'));
        console.log('Retrieved batch shape from directory:', batchShape); // Debugging statement
    }

    if (!batchShape) {
        console.error("Batch shape is not defined");
        statusDiv.innerText = "Error: Batch shape is not defined";
        return;
    }

    console.log(image);
    const { predictedClass, probabilities, timeTaken } = await predictImage(loaded_model, image, batchShape);
    console.log('Predicted Class:', predictedClass);
    console.log('Probabilities:', probabilities);
    console.log('Time taken for prediction:', timeTaken, 'ms');
    statusDiv.innerText = `Predicted class: ${predictedClass}\nProbabilities: ${probabilities}\nTime taken: ${timeTaken.toFixed(2)} ms`;
});