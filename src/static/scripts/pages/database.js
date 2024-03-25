

function goToUserDatabases(token) {
    window.location.href = `/database/list-databases?token=${token}`;
}


function createDatabase(userName, userPassword) {
    var databaseName = document.getElementById("databaseName").value;
    fetch("/database/create-database", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            usr: userName,
            pwd: userPassword,
            db_name: databaseName
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.message === "Database created successfully.") {
            window.location.href = `/database/fill_database?userName=${userName}&userPassword=${userPassword}&databaseName=${databaseName}`;
        } else if (data && data.message === "Database name not available.") {
            window.location.href = `/database/user-databases?userName=${userName}&userPassword=${userPassword}`;
            console.error("Database name not available");
        } else {
            console.error("Error with the database creation");
        }
    })
    .catch(error => {
        console.error("", error);
    });
}


function chooseDatabase(userName, userPassword, databaseName) {
    fetch("/database/choose-database", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            usr: userName,
            pwd: userPassword,
            db_name: databaseName
        }),
    })
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "Database chosen successfully.") {
            window.location.href = `/database/fill_database?userName=${userName}&userPassword=${userPassword}&databaseName=${databaseName}`;
        } else if (data && data.message === `Database ${databaseName} name not available.`) {
            window.location.href = `/database/user-databases?userName=${userName}&userPassword=${userPassword}`;
            console.error("Database name not available");
        }
            else {
            console.error("Error with the word creation.");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function addWord(userName, userPassword, databaseName) {
    var foreign = document.getElementById("input1").value;
    var native = document.getElementById("input2").value;
    fetch("/database/add-word", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            usr: userName,
            pwd: userPassword,
            db_name: databaseName,
            foreign: foreign,
            native: native
        }),
    })
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "Word created successfully.") {
            window.location.href = `/fill_database?userName=${userName}&userPassword=${userPassword}&databaseName=${databaseName}`;
        } else {
            console.error("Error with the word creation.");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}
