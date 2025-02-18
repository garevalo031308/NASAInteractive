document.addEventListener('DOMContentLoaded', async function() {
    const statusDiv = document.getElementById('status');
    const countdownDiv = document.createElement("div");
    const imageContainer = document.getElementById('image-container');

    const images = []

    async function loadModelFromDirectory(directoryPath) {
        try {
            const model = await tf.loadLayersModel(directoryPath);
            statusDiv.innerText = 'Model loaded successfully';
            localStorage.setItem('modelLoaded', 'true');
            return model;
        } catch (error) {
            statusDiv.innerText = "Error loading the model: " + error;
        }
    }

    function displayImages() {
        round_images.forEach(imageData => {
            for (const [cls, imgSrc] of Object.entries(imageData)) {
                const imgElement = document.createElement('img');
                imgElement.src = imgSrc;
                imgElement.alt = cls;
                imageContainer.appendChild(imgElement);
                console.log(imageData)
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
                url.searchParams.append('mode', mode);
                url.searchParams.append('gamemode', gamemode);
                url.searchParams.append('dataset', dataset);
                url.searchParams.append('difficulty', difficulty);
                url.searchParams.append('model', model);
                url.searchParams.append('username', username);
                url.searchParams.append('round_images', images.toString())
                window.location.href = url.toString();
            }
        }, 1000);
    }

    if (!window.checkedState) {
        window.checkedState = new Map(); // Initialize if not already done
    }

    const modelDirectory = '/static/models/' + model + "-" + dataset + "/model.json";  // Ensure model_path is correctly used

    if (localStorage.getItem('modelLoaded') === 'true') {
        statusDiv.innerText = 'Model already loaded';
        displayImages();
        startGameAfterDelay();
    } else {
        await loadModelFromDirectory(modelDirectory);
        displayImages();
        startGameAfterDelay();
    }
});