
import { goToInterroSettings } from "../api/users.js"; // Adjust the path as needed

document.addEventListener("DOMContentLoaded", function() {
    // Get references to the buttons
    const interroButton = document.getElementById("interroButton");
    const addWordsButton = document.getElementById("addWordsButton");

    // Add click event listeners to the buttons
    interroButton.addEventListener("click", function() {
        // Call the goToInterroSettings function from the API module
        const token = document.getElementById("token").value;
        goToInterroSettings(token);
    });

    addWordsButton.addEventListener("click", function() {
        // Call the goToUserDatabases function from the API module
        const token = document.getElementById("token").value;
        goToUserDatabases(token);
    });
});

document.addEventListener(
    "DOMContentLoaded",
    function () {
        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = `${progressBar}%`;
    }
);

