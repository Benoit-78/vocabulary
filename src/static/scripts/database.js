
function goToUserDatabases(token) {
    window.location.href = `/database/list-databases?token=${token}`;
}


function chooseDatabase(token) {
    var databaseName = document.getElementById("databaseName").value;
    fetch(
        `/database/choose-database?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                db_name: databaseName
            }),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "Database chosen successfully.") {
            window.location.href = `/database/fill_database?token=${token}&databaseName=${databaseName}`;
        } else if (data && data.message === `Database ${databaseName} name not available.`) {
            window.location.href = `/database/user-databases?token=${token}`;
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


function createDatabase(token) {
    var databaseName = document.getElementById("databaseName").value;
    fetch(
        `/database/create-database?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                db_name: databaseName
            }),
        }
    )
    .then(response => response.json())
    .then(data => {
        if (data && data.message === "Database created successfully.") {
            window.location.href = `/database/fill-database?token=${token}&databaseName=${databaseName}`;
        } else if (data && data.message === "Database name not available.") {
            window.location.href = `/database/user-databases?token=${token}`;
            console.error("Database name not available");
        } else {
            console.error("Error with the database creation");
        }
    })
    .catch(error => {
        console.error("", error);
    });
}




function addWord(token, databaseName) {
    var foreign = document.getElementById("input1").value;
    var native = document.getElementById("input2").value;
    fetch(
        `/database/add-word?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                db_name: databaseName,
                foreign: foreign,
                native: native
            }),
        }
    )
    .then(response => response.json())
    .then(data => {
        if (data && data.message === "Word added successfully.") {
            console.log(token)
            console.log(databaseName)
            window.location.href = `/database/fill-database?token=${token}&databaseName=${databaseName}`;
        } else {
            console.error("Error with the word creation.");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}
