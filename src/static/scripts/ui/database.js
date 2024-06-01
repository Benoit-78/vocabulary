import { goToUserDatabases, chooseDatabase, createDatabase, addWord } from "../api/database.js";


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
    const createDatabaseButton = document.getElementById("createDatabaseButton");
    const token = document.body.dataset.token;

    createDatabaseButton.addEventListener("click", function() {
        var databaseName = document.getElementById("databaseName").value;
        createDatabase(token, databaseName);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const seeDatabaseButton = document.getElementById("seeDatabaseButton");
    const token = document.body.dataset.token;

    seeDatabaseButton.addEventListener("click", function() {
        var databaseName = document.getElementById("databaseName").value;
        seeDatabase(token, databaseName);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const chooseDatabaseButton = document.getElementById("chooseDatabaseButton");
    const token = document.body.dataset.token;

    chooseDatabaseButton.addEventListener("click", function() {
        var dropdown = document.getElementById("dropdown");
        var databaseName = dropdown.value;
        chooseDatabase(token, databaseName);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const addWordButton = document.getElementById("addWordButton");
    const token = document.body.dataset.token;

    addWordButton.addEventListener("click", function() {
        var foreign = document.getElementById("input1").value;
        var native = document.getElementById("input2").value;
        addWord(token, databaseName, foreign, native);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const userDatabasesButton = document.getElementById("userDatabasesButton");
    const token = document.body.dataset.token;

    userDatabasesButton.addEventListener("click", function() {
        goToUserDatabases(token);
    });
});
