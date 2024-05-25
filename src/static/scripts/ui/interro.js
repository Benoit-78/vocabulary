import { goToInterroSettings, sendUserSettings, showTranslation, sendUserAnswer, launchRattraps } from "../api/interro.js";


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


document.addEventListener("DOMContentLoaded", function () {
    const progressBar = document.getElementById("progress-bar");

    progressBar.style.width = `${progressBar}%`;
});


document.addEventListener("DOMContentLoaded", function() {
    const showTranslationButton = document.getElementById("showTranslationButton");
    const token = document.body.dataset.token;

    showTranslationButton.addEventListener("click", function() {
        showTranslation(token, interroCategory, numWords, count, score);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const yesButton = document.getElementById("yesButton");
    const token = document.body.dataset.token;

    yesButton.addEventListener("click", function() {
        sendUserAnswer(
            token, interroCategory, 'Yes', count, numWords, score, content_box1, content_box2
        );
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const noButton = document.getElementById("noButton");
    const token = document.body.dataset.token;

    noButton.addEventListener("click", function() {
        sendUserAnswer(
            token, interroCategory, 'No', count, numWords, score, content_box1, content_box2
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
    // HEADER
    // const thead = document.createElement('thead');
    // const headerRow = document.createElement('tr');
    // tableData.headers.forEach(header => {
    //     const th = document.createElement('th');
    //     th.textContent = header;
    //     headerRow.appendChild(th);
    // });
    // thead.appendChild(headerRow);
    // table.appendChild(thead);
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
    tableContainer.style.transition = "opacity 2s";
    setTimeout(() => {
        tableContainer.style.opacity = 1;
    }, 500); // Delay before fade-in starts
});