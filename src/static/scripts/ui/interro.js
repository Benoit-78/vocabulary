import { goToInterroSettings } from "../api/interro.js";


document.addEventListener("DOMContentLoaded", function() {
    const interroButton = document.getElementById("interroButton");
    const token = document.body.dataset.token;

    interroButton.addEventListener("click", function() {
        goToInterroSettings(token);
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const progressBar = document.getElementById("progress-bar");

    progressBar.style.width = `${progressBar}%`;
});
