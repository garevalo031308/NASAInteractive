document.addEventListener('DOMContentLoaded', function () {
    const mode_buttons = document.querySelectorAll('#modeselection button');
    const gamemode_buttons = document.querySelectorAll('#gamemode button');
    const dataset_buttons = document.querySelectorAll("#dataset button");
    const difficulty_buttons = document.querySelectorAll('#difficulty button');
    const model_div = document.getElementById("model");

    const datasetinfo = document.getElementById("datasetinfo");
    const startGame = document.getElementById("startgame")

    const usernameBox = document.getElementById("username")

    if (mode_buttons.length > 0) mode_buttons[0].classList.add('active');
    if (gamemode_buttons.length > 0) gamemode_buttons[0].classList.add('active');
    if (dataset_buttons.length > 0) dataset_buttons[0].classList.add('active');
    if (difficulty_buttons.length > 0) difficulty_buttons[0].classList.add('active')

    function displayDatasetInfo(dataset_name) {
        // Clear existing content
        datasetinfo.innerHTML = '';

        // Find the selected dataset
        for (const [dataset, data] of Object.entries(datasets)) {
            if (dataset_name === dataset) {
                // Create and append dataset name
                const datasetNameElement = document.createElement('h3');
                datasetNameElement.textContent = dataset;
                datasetinfo.appendChild(datasetNameElement);

                // Create and append number of images
                const numberOfImagesElement = document.createElement('h4');
                numberOfImagesElement.textContent = `Number of Images: ${data.number_of_images}`;
                datasetinfo.appendChild(numberOfImagesElement);

                const descriptionElement = document.createElement('h4');
                descriptionElement.textContent = `Description: ${data.description}`;
                datasetinfo.appendChild(descriptionElement);

                // Create and append class information
                const classElement = document.createElement('div');
                classElement.id = "datasetclasses";

                for (const cls of data.classes) {
                    const classNameElement = document.createElement('p');
                    classNameElement.textContent = cls.class_name;
                    classElement.appendChild(classNameElement);
                }

                datasetinfo.appendChild(classElement);
            }
        }
    }

    function displayStartGame() {
        startGame.innerHTML = "";
        const startTitle = document.createElement("h2");
        startTitle.innerText = "Start Game";
        const startButton = document.createElement("button");
        startButton.type = "button";
        startButton.innerText = "Start Game";

        startButton.classList.add('active');

        startGame.appendChild(startTitle);
        startGame.appendChild(startButton);

        startButton.addEventListener('click', () => {
            const activeModeButton = document.querySelector('#modeselection button.active');
            const activeGamemodeButton = document.querySelector('#gamemode button.active');
            const activeDatasetButton = document.querySelector('#dataset button.active');
            const activeDifficultyButton = document.querySelector('#difficulty button.active');
            const activeModelButton = document.querySelector('#model button.active');

            console.log("Active Mode Button: ", activeModeButton ? activeModeButton.textContent : "None");
            console.log("Active Gamemode Button: ", activeGamemodeButton ? activeGamemodeButton.textContent : "None");
            console.log("Active Dataset Button: ", activeDatasetButton ? activeDatasetButton.textContent : "None");
            console.log("Active Difficulty Button: ", activeDifficultyButton ? activeDifficultyButton.textContent : "None");
            console.log("Active Model Button: ", activeModelButton ? activeModelButton.textContent : "None");
            console.log("Username: ", usernameBox.value)

            // Construct the URL with query parameters
            const url = new URL('NASAMainPage/game/loading', window.location.origin);
            if (activeModeButton) url.searchParams.append('mode', activeModeButton.textContent);
            if (activeGamemodeButton) url.searchParams.append('gamemode', activeGamemodeButton.textContent);
            if (activeDatasetButton) url.searchParams.append('dataset', activeDatasetButton.textContent);
            if (activeDifficultyButton) url.searchParams.append('difficulty', activeDifficultyButton.textContent);
            if (activeModelButton) url.searchParams.append('model', activeModelButton.textContent);
            if (usernameBox.value) url.searchParams.append("username", usernameBox.value)


            // // Navigate to the constructed URL
            window.location.href = url.toString();
        });
    }

    function displayModels(dataset_name){
        model_div.innerHTML = ""

        for (const [dataset, models] of Object.entries(dataset_to_models)){
            const modelTitle = document.createElement("h2")
            modelTitle.innerText = "Model"
            model_div.appendChild(modelTitle)
            if (dataset_name === dataset){
                for (let model of models){
                    const modelButton = document.createElement('button')
                    modelButton.textContent = model
                    model_div.appendChild(modelButton)

                    // Add event listener to the newly created button
                    modelButton.addEventListener('click', () => {
                        const model_buttons = model_div.querySelectorAll('button');
                        model_buttons.forEach(btn => btn.classList.remove('active'));
                        modelButton.classList.add('active');
                        displayStartGame()
                    });
                }
            }
        }
    }

    mode_buttons.forEach(button => {
        button.addEventListener('click', () => {
            mode_buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        });
    });

    gamemode_buttons.forEach(button => {
        button.addEventListener('click', () => {
            gamemode_buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        });
    });

    dataset_buttons.forEach(button => {
        button.addEventListener('click', () => {
            dataset_buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            displayDatasetInfo(button.textContent);
            displayModels(button.textContent)
        });
    });

    difficulty_buttons.forEach(button => {
        button.addEventListener('click', () => {
            difficulty_buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        });
    });
});