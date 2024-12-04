document.addEventListener('DOMContentLoaded', function(){
    const mainDiv = document.getElementById("divitems")

    async function loadModelFromDirectory(){
        try{
            const model = await tf.loadLayersModel('/static/models/VGG16/model.json')
            tf.tidy(function() {
                let answer = model.predict(tf.zeros([1, 224, 224, 3]))
                console.log(answer.shape)
            })
            const modelH1 = document.createElement("h1")
            modelH1.innerHTML = "Model loaded successfully"
            mainDiv.append(modelH1)
            return model;
        } catch (error){
            const modelH1 = document.createElement("h1")
            modelH1.innerHTML = "Error loading the model: " + error;
            mainDiv.append(modelH1)
        }
    }

    async function predictLoop(){
        tf.tidy(function() {

        })
    }

    async function loadImage(){
        const img = new Image()
        img.src = ""

    }

    loadModelFromDirectory().then(r => {})
});
