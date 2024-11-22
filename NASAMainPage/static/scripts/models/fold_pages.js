// NASAMainPage/static/scripts/models/fold_pages.js

// TODO Add image of confusion matrix
// TODO fix CSS
document.addEventListener('DOMContentLoaded', function() {
    const folddiv = document.getElementById("foldinfo");
    const foldbuttons = document.querySelectorAll(".foldbutton");

    foldbuttons.forEach(button => {
        button.addEventListener('click', function() {
            const foldName = this.value;
            displayFold(foldName);
        });
    });

    function displayFold(foldName) {
        // Clear previous content
        folddiv.innerHTML = '';

        // Create and append fold header
        const foldHeader = document.createElement("h2");
        foldHeader.innerHTML = foldName + " Performance";
        folddiv.appendChild(foldHeader);

        // Create and append class performance header
        const classPerformance = document.createElement("h3");
        classPerformance.innerHTML = "Class Performance";
        folddiv.appendChild(classPerformance);

        // Create and append accuracy
        const accuracy = document.createElement("h3");

        // Create table elements
        const foldTable = document.createElement("table");
        const headerTable = document.createElement("thead");
        const infoTableRow = document.createElement("tr");

        // Create and append table headers
        const classRow = document.createElement("th");
        classRow.innerHTML = "Class";
        const precisionRow = document.createElement("th");
        precisionRow.innerHTML = "Precision";
        const recallRow = document.createElement("th");
        recallRow.innerHTML = "Recall";
        const f1ScoreRow = document.createElement("th");
        f1ScoreRow.innerHTML = "F1 Score";
        const supportRow = document.createElement("th");
        supportRow.innerHTML = "Support";

        infoTableRow.appendChild(classRow);
        infoTableRow.appendChild(precisionRow);
        infoTableRow.appendChild(recallRow);
        infoTableRow.appendChild(f1ScoreRow);
        infoTableRow.appendChild(supportRow);
        headerTable.appendChild(infoTableRow);
        foldTable.appendChild(headerTable);

        const bodyTable = document.createElement("tbody");

        for (const [fold_name, fold_data] of Object.entries(fold)) {
            if (fold_name === foldName) {
                accuracy.innerHTML = "Accuracy: " + fold_data.Accuracy;
                folddiv.appendChild(accuracy);

                for (const [class_name, metrics] of Object.entries(fold_data.Classes)) {
                    const bodyRow = document.createElement("tr");

                    const classData = document.createElement("td");
                    classData.innerHTML = class_name;
                    const precisionData = document.createElement("td");
                    precisionData.innerHTML = metrics.Precision;
                    const recallData = document.createElement("td");
                    recallData.innerHTML = metrics.Recall;
                    const f1ScoreData = document.createElement("td");
                    f1ScoreData.innerHTML = metrics.F1Score;
                    const supportData = document.createElement("td");
                    supportData.innerHTML = metrics.Support;

                    bodyRow.appendChild(classData);
                    bodyRow.appendChild(precisionData);
                    bodyRow.appendChild(recallData);
                    bodyRow.appendChild(f1ScoreData);
                    bodyRow.appendChild(supportData);
                    bodyTable.appendChild(bodyRow);
                }
            }
        }
        foldTable.appendChild(bodyTable);
        folddiv.appendChild(foldTable);
    }
});