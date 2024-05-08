import { goToUserDatabases } from "../api/database.js";


document.addEventListener("DOMContentLoaded", function() {
    const csvForm = document.getElementById("csvForm")
    const token = document.body.dataset.token;

    csvForm.addEventListener("submit", function(event) {
        // Prevent the form from submitting normally
        event.preventDefault();
        uploadCSV(token);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const addWordButton = document.getElementById("addWordsButton");
    const token = document.body.dataset.token;

    addWordButton.addEventListener("click", function() {
        goToUserDatabases(token);
    });
});
