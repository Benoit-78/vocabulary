import { sendUserSettings, showTranslation, sendUserAnswer, launchRattrap } from "../api/interro.js";


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
    const sendUserSettingsButton = document.getElementById("sendUserSettingsButton");
    const token = document.body.dataset.token;

    sendUserSettingsButton.addEventListener("click", function() {
        const databaseName = document.getElementById('databaseName').value;
        const testLength = document.getElementById('testLength').value;
        const params = {
            databaseName: databaseName,
            testType: testType,
            testLength: testLength
        }
        sendUserSettings(token, params);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const showTranslationButton = document.getElementById("showTranslationButton");
    const token = document.body.dataset.token;
    var decodedInterroDict = decodeHtmlEntities(decodeHtmlEntities(interroDict));
    var decodedOldInterroDict = decodeHtmlEntities(decodeHtmlEntities(oldInterroDict));
    var decodedFaultsDict = decodeHtmlEntities(decodeHtmlEntities(faultsDict));
    const params = {
        testCount: testCount,
        databaseName: databaseName,
        faultsDict: decodedFaultsDict,
        testIndex: testIndex,
        interroCategory: interroCategory,
        interroDict: decodedInterroDict,
        oldInterroDict: decodedOldInterroDict,
        testPerf: testPerf,
        testScore: testScore,
        testLength: testLength,
        testType: testType,
    };

    showTranslationButton.addEventListener("click", function() {
        showTranslation(token, params);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const yesButton = document.getElementById("yesButton");
    const token = document.body.dataset.token;
    var decodedInterroDict = decodeHtmlEntities(decodeHtmlEntities(interroDict));
    var decodedOldInterroDict = decodeHtmlEntities(decodeHtmlEntities(oldInterroDict));
    var decodedFaultsDict = decodeHtmlEntities(decodeHtmlEntities(faultsDict));
    const params = {
        userAnswer: 'Yes',
        contentBox1: contentBox1,
        contentBox2: contentBox2,
        testCount: testCount,
        databaseName: databaseName,
        faultsDict: decodedFaultsDict,
        testIndex: testIndex,
        interroCategory: interroCategory,
        interroDict: decodedInterroDict,
        oldInterroDict: decodedOldInterroDict,
        testPerf: testPerf,
        testScore: testScore,
        testLength: testLength,
        testType: testType,
    };

    yesButton.addEventListener("click", function() {
        sendUserAnswer(token, params);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const noButton = document.getElementById("noButton");
    const token = document.body.dataset.token;
    var decodedInterroDict = decodeHtmlEntities(decodeHtmlEntities(interroDict));
    var decodedOldInterroDict = decodeHtmlEntities(decodeHtmlEntities(oldInterroDict));
    var decodedFaultsDict = decodeHtmlEntities(decodeHtmlEntities(faultsDict));
    const params = {
        userAnswer: 'No',
        contentBox1: contentBox1,
        contentBox2: contentBox2,
        testCount: testCount,
        databaseName: databaseName,
        faultsDict: decodedFaultsDict,
        testIndex: testIndex,
        interroCategory: interroCategory,
        interroDict: decodedInterroDict,
        oldInterroDict: decodedOldInterroDict,
        testPerf: testPerf,
        testScore: testScore,
        testLength: testLength,
        testType: testType,
    };
    
    noButton.addEventListener("click", function() {
        sendUserAnswer(token, params);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const rattrapButton = document.getElementById("rattrapButton");
    const token = document.body.dataset.token;
    var decodedInterroDict = decodeHtmlEntities(decodeHtmlEntities(interroDict));
    var decodedFaultsDict = decodeHtmlEntities(decodeHtmlEntities(faultsDict));
    var decodedOldInterroDict = decodeHtmlEntities(decodeHtmlEntities(oldInterroDict));
    const params = {
        databaseName: databaseName,
        faultsDict: decodedFaultsDict,
        testIndex: testIndex,
        interroCategory: interroCategory,
        interroDict: decodedInterroDict,
        oldInterroDict: decodedOldInterroDict,
        testScore: testScore,
        testLength: testLength,
        testType: testType
    }
    console.log("Params:", params)
    
    rattrapButton.addEventListener("click", function() {
        launchRattrap(token, params);
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
