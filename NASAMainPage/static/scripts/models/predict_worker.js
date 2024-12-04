// NASAMainPage/static/scripts/models/predict_worker.js
importScripts('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs');

let model;

onmessage = async function(e) {
    const { type, data } = e.data;

    if (type === 'loadModel') {
        try {
            model = await tf.loadLayersModel(data.modelPath);
            postMessage({ type: 'modelLoaded' });
        } catch (error) {
            postMessage({ type: 'error', error: error.message });
        }
    } else if (type === 'predict') {
        try {
            const batchTensor = tf.tensor(data.batchTensor, [data.batchSize, 224, 224, 3]);
            const predictions = model.predict(batchTensor);
            const predictedClassIndices = predictions.argMax(-1).dataSync();
            postMessage({ type: 'predictions', predictions: Array.from(predictedClassIndices) });
        } catch (error) {
            postMessage({ type: 'error', error: error.message });
        }
    }
};