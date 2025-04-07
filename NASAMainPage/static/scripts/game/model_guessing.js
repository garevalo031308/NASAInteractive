document.addEventListener("DOMContentLoaded", async function() {
    const statusDiv = document.getElementById('modelguess');
    const imageContainer = document.getElementById('image-container');
    console.log(model);

    async function loadImage(filePath, batchShape) {
        const img = new Image();
        console.log(filePath);
        img.src = `/static/${filePath}`;
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

    async function predictImages(model, imagePaths, batchShape) {
        const imageTensors = await Promise.all(imagePaths.map(filePath => loadImage(filePath, batchShape)));
        const predictions = [];
        const timesTaken = [];

        for (const imageTensor of imageTensors) {
            const startTime = performance.now(); // Start time
            const prediction = model.predict(imageTensor);
            const probabilities = prediction.softmax().dataSync(); // Get probabilities using softmax
            const predictedIndex = prediction.argMax(-1).dataSync()[0]; // Ensure correct index retrieval
            const endTime = performance.now(); // End time
            const timeTaken = endTime - startTime; // Calculate time taken
            predictions.push({ predictedIndex, probabilities });
            timesTaken.push(timeTaken);
        }

        return { predictions, timesTaken };
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

    const { predictions, timesTaken } = await predictImages(loaded_model, image_paths, batchShape);
    console.log('Predictions:', predictions);
    console.log('Times taken:', timesTaken);

    const results = predictions.map((prediction, i) => {
        const predictedClass = classChoices[prediction.predictedIndex];
        return {
            predictedClass: predictedClass,
            timeTaken: timesTaken[i]
        };
    });

    // Send the results to the server
    await fetch('save_predictions/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is included
        },
        body: JSON.stringify({ results: results, game_id: game_id })
    });

    // Navigate to the next page
    const url = new URL('/NASAMainPage/game/gameplay', window.location.origin);
    url.searchParams.append('gameid', game_id);
    window.location.href = url.toString();
});

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}