import { sendGuestSettings, showTranslation, sendUserAnswer, launchRattrap } from "../api/guest.js";


document.addEventListener("DOMContentLoaded", function () {
    const progressBar = document.getElementById("progress-bar");
    setTimeout(() => {
        progressBar.style.width = `${progressBar}%`;
    }, 100);
});


// ============================================================
// English
document.addEventListener("DOMContentLoaded", function() {
    const englishButton = document.getElementById("englishButton");
    const token = document.body.dataset.token;
    englishButton.addEventListener("click", function() {
        sendGuestSettings(token, "English");
    });
});


// German
document.addEventListener("DOMContentLoaded", function() {
    const germanButton = document.getElementById("germanButton");
    const token = document.body.dataset.token;
    germanButton.addEventListener("click", function() {
        sendGuestSettings(token, "German");
    });
});


// Dutch
document.addEventListener("DOMContentLoaded", function() {
    const dutchButton = document.getElementById("dutchButton");
    const token = document.body.dataset.token;
    dutchButton.addEventListener("click", function() {
        sendGuestSettings(token, "Dutch");
    });
});


// Spanish
document.addEventListener("DOMContentLoaded", function() {
    const spanishButton = document.getElementById("spanishButton");
    const token = document.body.dataset.token;
    spanishButton.addEventListener("click", function() {
        sendGuestSettings(token, "Spanish");
    });
});


// Portuguese
document.addEventListener("DOMContentLoaded", function() {
    const portugueseButton = document.getElementById("portugueseButton");
    const token = document.body.dataset.token;
    portugueseButton.addEventListener("click", function() {
        sendGuestSettings(token, "Portuguese");
    });
});


// Russian
document.addEventListener("DOMContentLoaded", function() {
    const russianButton = document.getElementById("russianButton");
    const token = document.body.dataset.token;
    russianButton.addEventListener("click", function() {
        sendGuestSettings(token, "Russian");
    });
});


// Arabic
document.addEventListener("DOMContentLoaded", function() {
    const arabicButton = document.getElementById("arabicButton");
    const token = document.body.dataset.token;
    arabicButton.addEventListener("click", function() {
        sendGuestSettings(token, "Arabic");
    });
});


// Hebrew
document.addEventListener("DOMContentLoaded", function() {
    const hebrewButton = document.getElementById("hebrewButton");
    const token = document.body.dataset.token;
    hebrewButton.addEventListener("click", function() {
        sendGuestSettings(token, "Hebrew");
    });
});


// Chinese
document.addEventListener("DOMContentLoaded", function() {
    const chineseButton = document.getElementById("chineseButton");
    const token = document.body.dataset.token;
    chineseButton.addEventListener("click", function() {
        sendGuestSettings(token, "Chinese");
    });
});


// Latin
document.addEventListener("DOMContentLoaded", function() {
    const latinButton = document.getElementById("latinButton");
    const token = document.body.dataset.token;
    latinButton.addEventListener("click", function() {
        sendGuestSettings(token, "Latin");
    });
});


// Greek
document.addEventListener("DOMContentLoaded", function() {
    const greekButton = document.getElementById("greekButton");
    const token = document.body.dataset.token;
    greekButton.addEventListener("click", function() {
        sendGuestSettings(token, "Greek");
    });
});


// ============================================================
document.addEventListener("DOMContentLoaded", function() {
    const showTranslationButton = document.getElementById("showTranslationButton");
    const token = document.body.dataset.token;
    showTranslationButton.addEventListener("click", function() {
        showTranslation(token, interroCategory, testLength, testCount, testScore, testLanguage);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const yesButton = document.getElementById("yesButton");
    const token = document.body.dataset.token;
    yesButton.addEventListener("click", function() {
        sendUserAnswer(
            token, interroCategory, 'Yes', testCount, testLength, testScore, contentBox1, contentBox2, testLanguage
        );
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const noButton = document.getElementById("noButton");
    const token = document.body.dataset.token;
    noButton.addEventListener("click", function() {
        sendUserAnswer(
            token, interroCategory, 'No', testCount, testLength, testScore, contentBox1, contentBox2, testLanguage
        );
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const rattrapButton = document.getElementById("rattrapButton");
    const token = document.body.dataset.token;
    rattrapButton.addEventListener("click", function() {
        launchRattrap(token, interroCategory, newWords, newCount, newScore, testLanguage);
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
