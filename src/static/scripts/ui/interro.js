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
    console.log("Token:", token)

    sendUserSettingsButton.addEventListener("click", function() {
        const databaseName = document.getElementById('databaseName').value
        const testType = document.getElementById('testType').value
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
        showTranslation(token, numWords, count, score);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const yesButton = document.getElementById("yesButton");
    const token = document.body.dataset.token;

    yesButton.addEventListener("click", function() {
        sendUserAnswer(
            token, 'Yes', count, numWords, score, content_box1, content_box2
        );
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const noButton = document.getElementById("noButton");
    const token = document.body.dataset.token;

    noButton.addEventListener("click", function() {
        sendUserAnswer(
            token, 'No', count, numWords, score, content_box1, content_box2
        );
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const rattrapsButton = document.getElementById("rattrapsButton");
    const token = document.body.dataset.token;

    rattrapsButton.addEventListener("click", function() {
        launchRattraps(token, newTotal, newCount, newScore);
    });
});
