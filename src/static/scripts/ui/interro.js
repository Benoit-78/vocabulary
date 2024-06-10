import { goToInterroSettings, sendUserSettings, showTranslation, sendUserAnswer, launchRattraps } from "../api/interro.js";


function decodeHtmlEntities(encodedString) {
    const parser = new DOMParser();
    const decodedString = parser.parseFromString(
        `<!doctype html><body>${encodedString}`,
        'text/html'
    ).body.textContent;
    return decodedString;
}


document.addEventListener("DOMContentLoaded", function () {
    const progressBar = document.getElementById("progress-bar");

    setTimeout(() => {
        progressBar.style.width = `${progressBar}%`;
    }, 100);
});


document.addEventListener("DOMContentLoaded", function() {
    const interroButton = document.getElementById("interroButton");
    const token = document.body.dataset.token;

    interroButton.addEventListener("click", function() {
        goToInterroSettings(token);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const sendUserSettingsButton = document.getElementById("sendUserSettingsButton");
    const token = document.body.dataset.token;

    sendUserSettingsButton.addEventListener("click", function() {
        const databaseName = document.getElementById('databaseName').value
        const numWords = document.getElementById('numWords').value
        sendUserSettings(token, databaseName, testType, numWords);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const showTranslationButton = document.getElementById("showTranslationButton");
    const token = document.body.dataset.token;
    var decodedInterroDict = decodeHtmlEntities(decodeHtmlEntities(interroDict));
    var decodedFaultsDict = decodeHtmlEntities(decodeHtmlEntities(faultsDict));

    showTranslationButton.addEventListener("click", function() {
        showTranslation(token, interroCategory, decodedInterroDict, testLength, index, decodedFaultsDict, perf, count, score);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const yesButton = document.getElementById("yesButton");
    const token = document.body.dataset.token;
    var decodedInterroDict = decodeHtmlEntities(decodeHtmlEntities(interroDict));
    var decodedFaultsDict = decodeHtmlEntities(decodeHtmlEntities(faultsDict));

    yesButton.addEventListener("click", function() {
        sendUserAnswer(
            token, 'Yes', interroCategory, decodedInterroDict, testLength, index, decodedFaultsDict, perf, count, score, content_box1, content_box2
        );
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const noButton = document.getElementById("noButton");
    const token = document.body.dataset.token;
    var decodedInterroDict = decodeHtmlEntities(decodeHtmlEntities(interroDict));
    var decodedFaultsDict = decodeHtmlEntities(decodeHtmlEntities(faultsDict));

    noButton.addEventListener("click", function() {
        sendUserAnswer(
            token, 'No', interroCategory, decodedInterroDict, testLength, index, decodedFaultsDict, perf, count, score, content_box1, content_box2
        );
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const rattrapsButton = document.getElementById("rattrapsButton");
    const token = document.body.dataset.token;

    rattrapsButton.addEventListener("click", function() {
        launchRattraps(token, interroCategory, newTotal, newCount, newScore);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const tableContainer = document.getElementById("table-container");
    const tableData = JSON.parse(document.getElementById('table-data').textContent);
    const table = document.createElement('table');

    table.className = "data-table";
    // BODY
    const tbody = document.createElement('tbody');
    tableData.rows.forEach(rowData => {
        const row = document.createElement('tr');
        rowData.forEach(cellData => {
            const td = document.createElement('td');
            td.textContent = cellData;
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);
    // Append table to container
    tableContainer.appendChild(table);
    // Apply fade-in effect
    tableContainer.style.opacity = 0;
    tableContainer.style.transition = "opacity 0.5s";
    setTimeout(() => {
        tableContainer.style.opacity = 1;
    }, 500); // Delay before fade-in starts
});