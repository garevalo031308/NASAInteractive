document.addEventListener("DOMContentLoaded", async function () {
    const statusDiv = document.getElementById('status');
    const imageContainer = document.getElementById('image-container');

    async function loadModel(modelName, directoryPath) {
        try {
            const model = await tf.loadLayersModel('indexeddb://' + modelName + "_" + dataset);
            const batchShape = JSON.parse(localStorage.getItem(modelName + "_" + dataset + '_batchShape'));
            statusDiv.innerText = 'Model loaded successfully from IndexedDB';
            return { model, batchShape };
        } catch (error) {
            console.error("Error loading the model from IndexedDB: ", error);
            statusDiv.innerText = "Error loading the model from IndexedDB, loading from URL...";
            try {
                const model = await tf.loadLayersModel('/static/models/' + directoryPath + '/model.json');
                statusDiv.innerText = 'Model loaded successfully from URL';
                await model.save('indexeddb://' + modelName + "_" + dataset); // Save to IndexedDB
                const batchShape = await getBatchShape('/static/models/' + directoryPath + '/model.json');
                localStorage.setItem(modelName + "_" + dataset + '_batchShape', JSON.stringify(batchShape));
                localStorage.setItem(modelName + "_" + dataset + '_modelLoaded', 'true');
                return { model, batchShape };
            } catch (urlError) {
                statusDiv.innerText = "Error loading the model from URL: " + urlError;
                throw urlError;
            }
        }
    }

    function getBatchShape(modelDirectory) {
        return fetch(modelDirectory)
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`HTTP error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then((data) => {
                const batchShapeList = data['modelTopology']['model_config']['config']['layers'][0]["config"]["batch_input_shape"];
                return [batchShapeList[1], batchShapeList[2]];
            })
            .catch((error) => {
                console.error("Unable to fetch data:", error);
                return null;
            });
    }

    async function loadImage(filePath, batchShape) {
        const img = new Image();
        img.src = `/static/${filePath}`;
        await new Promise((resolve) => {
            img.onload = resolve;
        });
        if (!batchShape) {
            throw new Error("Batch shape is not defined");
        }
        return tf.browser.fromPixels(img)
            .resizeNearestNeighbor(batchShape) // Use the batch shape here
            .toFloat()
            .expandDims();
    }

    async function predictImages(model, imagePaths, batchShape) {
        const imageTensors = await Promise.all(imagePaths.map(filePath => loadImage(filePath, batchShape)));
        const predictions = [];
        const timesTaken = [];

        for (const imageTensor of imageTensors) {
            const startTime = performance.now();
            const prediction = model.predict(imageTensor);
            const probabilities = prediction.softmax().dataSync();
            const predictedIndex = prediction.argMax(-1).dataSync()[0];
            const endTime = performance.now();
            const timeTaken = endTime - startTime;
            predictions.push({ predictedIndex, probabilities });
            timesTaken.push(timeTaken);
        }

        return { predictions, timesTaken };
    }

    async function savePredictions(results) {
        await fetch('save_predictions/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ results: results, game_id: game_id })
        });
    }

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

    function startGame() {
        const url = new URL('/NASAMainPage/game/gameplay', window.location.origin);
        url.searchParams.append('gameid', game_id);
        window.location.href = url.toString();
    }

    // Main logic
    const modelDirectory = model + "-" + dataset;
    let loadedModel, batchShape;

    try {
        if (localStorage.getItem(model + "_" + dataset +'_modelLoaded') === 'true') {
            statusDiv.innerText = 'Model already loaded';
            loadedModel = await tf.loadLayersModel('indexeddb://' + model + "_" + dataset);
            batchShape = JSON.parse(localStorage.getItem(model + "_" + dataset + '_batchShape'));
        } else {
            const modelData = await loadModel(model, modelDirectory);
            loadedModel = modelData.model;
            batchShape = modelData.batchShape;
        }

        const { predictions, timesTaken } = await predictImages(loadedModel, image_paths, batchShape);

        const results = predictions.map((prediction, i) => {
            const predictedClass = classChoices[prediction.predictedIndex];
            return {
                predictedClass: predictedClass,
                timeTaken: timesTaken[i]
            };
        });

        await savePredictions(results);
        startGame();
    } catch (error) {
        console.error("Error during model preparation or guessing:", error);
    }
});