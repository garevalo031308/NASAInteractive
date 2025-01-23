document.addEventListener('DOMContentLoaded', async function() {
    const statusDiv = document.getElementById('status');

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

    if (!window.checkedState) {
        window.checkedState = new Map(); // Initialize if not already done
    }

    const modelDirectory = '/static/models/' + model + "/model.json";  // Ensure model_path is correctly used

    if (localStorage.getItem('modelLoaded') === 'true') {
        statusDiv.innerText = 'Model already loaded';
    } else {
        const model = await loadModelFromDirectory(modelDirectory);
    }
});