document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submitbutton');
    const statusDiv = document.getElementById('status');
    const fileDiv = document.getElementById("prediction-result");

    const imageArray = [];

    const classes = [];
    for (const [cls, imagesArray] of Object.entries(images)) {
        classes.push(cls);
    }

    window.checkedState = new Map(); // Map to store options chosen

    console.log(classes);

    function getBatchShape(modelDirectory) {
        return fetch(modelDirectory)
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`HTTP error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then((data) => {
                const batch_shape_list = data['modelTopology']['model_config']['config']['layers'][0]["config"]["batch_input_shape"];
                console.log(batch_shape_list);
                if (batch_shape_list[1] === null && batch_shape_list[2] === null) {
                    return [1024, 0]
                } else {return [batch_shape_list[1], batch_shape_list[2]];}
            })
            .catch((error) => {
                console.error("Unable to fetch data:", error);
                return null;
            });
    }

    async function loadModelFromDirectory(directoryPath) {
        try {
            const model = await tf.loadLayersModel(directoryPath);
            statusDiv.innerText = 'Model loaded successfully';
            submitButton.disabled = false;
            return model;
        } catch (error) {
            statusDiv.innerText = "Error loading the model: " + error;
        }
    }

    async function loadImage(filePath, batch_shape) {
        const img = new Image();
        img.src = filePath;
        await new Promise((resolve) => {
            img.onload = resolve;
        });
        return tf.browser.fromPixels(img)
            .resizeNearestNeighbor(batch_shape) // Change the size according to your model's input size
            .toFloat()
            .expandDims();
    }

    async function predictImages(model, imagePaths, batch_shape) {
        const imageTensors = await Promise.all(imagePaths.map(filePath => loadImage(filePath, batch_shape)));
        const batchTensor = tf.concat(imageTensors); // Concatenate tensors along the batch dimension
        const predictions = model.predict(batchTensor);
        return predictions.argMax(-1).dataSync(); // Get the predicted class indices
    }

    if (!window.checkedState) {
        window.checkedState = new Map(); // Initialize if not already done
    }

    (async () => {
        const modelDirectory = '/static/models/' + model_name + "-" + dataset + "/model.json";  // Ensure model_path is correctly used
        const batch_shape = await getBatchShape(modelDirectory);
        const model = await loadModelFromDirectory(modelDirectory);

        submitButton.addEventListener('click', async function () {
            const list_of_checked = Array.from(window.checkedState.entries())
                .filter(([key, value]) => value)
                .map(([key]) => key);

            console.log(list_of_checked);

            for (const item of list_of_checked) {
                const [cls, name] = item.split(',');
                imageArray.push('/static/Datasets/' + dataset + "/" + cls + "/" + name);
            }

            const startTime = new Date(); // Start timer

            const predictedClassIndices = await predictImages(model, imageArray, batch_shape);

            const endTime = new Date(); // End timer
            const timeTakenMs = endTime - startTime; // Calculate time taken in milliseconds
            const timeTakenSec = (timeTakenMs / 1000).toFixed(2); // Calculate time taken in seconds

            console.log(`Time taken for prediction: ${timeTakenMs} ms (${timeTakenSec} seconds)`);

            predictedClassIndices.forEach((predictedClassIndex, i) => {
                const predictedClass = classes[predictedClassIndex];
                const predictedHeader = document.createElement("h3");
                predictedHeader.innerText = `Predicted Class: ${predictedClass}`;
                fileDiv.appendChild(predictedHeader);
                console.log(`Predicted class: ${predictedClass}`);
            });

            const timeTakenElement = document.createElement("p");
            timeTakenElement.innerText = `Time taken for prediction: ${timeTakenMs} ms (${timeTakenSec} seconds)`;
            fileDiv.appendChild(timeTakenElement);
        });
    })();
});