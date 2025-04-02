document.addEventListener('DOMContentLoaded', async function() {
    const statusDiv = document.getElementById('status');
    const countdownDiv = document.createElement("div");
    const imageContainer = document.getElementById('image-container');

    const images = [];

    async function loadModelFromDirectory(directoryPath, modelName) {
        try {
            const model = await tf.loadLayersModel('indexeddb://' + modelName);
            const batchShape = JSON.parse(localStorage.getItem(modelName + '_batchShape'));
            statusDiv.innerText = 'Model loaded successfully from IndexedDB';
            localStorage.setItem('modelLoaded', 'true');
            return { model, batchShape };
        } catch (error) {
            console.error("Error loading the model from IndexedDB: ", error);
            statusDiv.innerText = "Error loading the model from IndexedDB, loading from URL...";
            try {
                const model = await tf.loadLayersModel('/static/models/' + directoryPath + '/model.json');
                statusDiv.innerText = 'Model loaded successfully from URL';
                const saveResult = await model.save('indexeddb://' + modelName); // Save the model to IndexedDB using the model name
                console.log(saveResult);
                const batchShape = await getBatchShape('/static/models/' + directoryPath + '/model.json');
                localStorage.setItem(modelName + '_batchShape', JSON.stringify(batchShape));
                localStorage.setItem('modelLoaded', 'true');
                return { model, batchShape };
            } catch (urlError) {
                statusDiv.innerText = "Error loading the model from URL: " + urlError;
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
                const batch_shape_list = data['modelTopology']['model_config']['config']['layers'][0]["config"]["batch_input_shape"];
                const batch_shape = [batch_shape_list[1], batch_shape_list[2]];

                return [batch_shape_list[1], batch_shape_list[2]];
            })
            .catch((error) => {
                console.error("Unable to fetch data:", error);
                return null;
            });
    }

    function displayImages() {
        round_images.forEach(imageData => {
            for (const [cls, imgSrc] of Object.entries(imageData)) {
                const imgElement = document.createElement('img');
                imgElement.src = `/static/${imgSrc}`;
                imgElement.alt = cls;
                imageContainer.appendChild(imgElement);
            }
        });
    }

    function startGameAfterDelay() {
        let countdown = 5;
        countdownDiv.innerText = `Starting game in ${countdown} seconds...`;
        const interval = setInterval(() => {
            countdown -= 1;
            countdownDiv.innerText = `Starting game in ${countdown} seconds...`;
            if (countdown === 0) {
                clearInterval(interval);

                const url = new URL('NASAMainPage/game/gameplay', window.location.origin);
                url.searchParams.append('gameid', game_id);
                window.location.href = url.toString();
            }
        }, 1000);
    }

    if (!window.checkedState) {
        window.checkedState = new Map(); // Initialize if not already done
    }

    const modelDirectory = model + "-" + dataset;  // Ensure model_path is correctly used

    if (localStorage.getItem('modelLoaded') === 'true') {
        statusDiv.innerText = 'Model already loaded';
        displayImages();
        startGameAfterDelay();
    } else {
        await loadModelFromDirectory(modelDirectory, model);
        displayImages();
        startGameAfterDelay();
    }
});