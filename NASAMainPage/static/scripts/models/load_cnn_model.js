document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submitbutton');
    const statusDiv = document.getElementById('status');
    const fileDiv = document.getElementById("prediction-result")

    const imageArray = []

    const classes = []
    for (const [cls, imagesArray] of Object.entries(images)) {
        classes.push(cls)
    }

    console.log(classes)

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

    async function loadImage(filePath){
        const img = new Image();
        img.src = filePath;
        await new Promise((resolve) =>{
            img.onload = resolve;
        })
        return tf.browser.fromPixels(img)
            .resizeNearestNeighbor([224, 224]) // Change the size according to your model's input size
            .toFloat()
            .expandDims();
    }

    async function predictImages(model, imagePaths) {
        const imageTensors = await Promise.all(imagePaths.map(loadImage));
        const batchTensor = tf.concat(imageTensors); // Concatenate tensors along the batch dimension
        const predictions = model.predict(batchTensor);
        return predictions.argMax(-1).dataSync(); // Get the predicted class indices
    }

    if (!window.checkedState) {
        window.checkedState = new Map(); // Initialize if not already done
    }

    (async () =>{
        const modelDirectory = '/static/models/' + model_name + "/model.json";  // Ensure model_path is correctly used
        const model = await loadModelFromDirectory(modelDirectory)

        submitButton.addEventListener('click', async function () {
            const list_of_checked = Array.from(window.checkedState.entries())
                .filter(([key, value]) => value)
                .map(([key]) => key);

            console.log(list_of_checked)

            for (const item of list_of_checked) {
                const [cls, name] = item.split(',');
                imageArray.push('/static/Datasets/' + dataset + "/" + cls + "/" + name)
            }

            const predictedClassIndices = await predictImages(model, imageArray);
            predictedClassIndices.forEach((predictedClassIndex, i) => {
                const predictedClass = classes[predictedClassIndex];
                const predictedHeader = document.createElement("h3")
                predictedHeader.innerText = `\`Predicted Class: ${predictedClass}`
                fileDiv.appendChild(predictedHeader)
                console.log(`Predicted class: ${predictedClass}`);
            });
        });

    })();
});