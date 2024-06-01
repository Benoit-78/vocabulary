export { goToUserDatabases, chooseDatabase, createDatabase, addWord };


function goToUserDatabases(token) {
    window.location.href = `/v1/database/list-databases?token=${token}`;
}


function createDatabase(token, databaseName) {
    fetch(
        `/v1/database/create-database?token=${token}`,
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
        if (data && data.message === "Database created successfully") {
            window.location.href = `/v1/database/fill-database?token=${token}&databaseName=${databaseName}`;
        } else if (data && data.message === "No database name given") {
            console.error("No database name given");
            window.location.href = `/v1/database/list-databases?token=${token}&errorMessage=${data.message}`;
        } else if (data && data.message === "Database name not available") {
            console.error("Database name not available");
            window.location.href = `/v1/database/list-databases?token=${token}&errorMessage=${data.message}`;
        } else {
            console.error("Error with the database creation");
        }
    })
    .catch(error => {
        console.error("", error);
    });
}


function seeDatabase(token, databaseName) {
    fetch(
        `/v1/database/retrieve-database?token=${token}`,
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
        if (data && data.message === "Retrieved database words successfully") {
            window.location.href = `/v1/database/see-database?token=${token}&databaseName=${databaseName}&versionTable=${versionTable}&themeTable=${themeTable}`;
        } else {
            console.error("Error with the database words retreieval");
        }
    })
    .catch(error => {
        console.error("", error);
    });
}


function chooseDatabase(token, databaseName) {
    fetch(
        `/v1/database/choose-database?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({db_name: databaseName}),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "Database chosen successfully") {
            window.location.href = `/v1/database/fill-database?token=${token}&databaseName=${databaseName}`;
        } else if (data && data.message === `Database ${databaseName} name not available`) {
            window.location.href = `/v1/database/list-databases?token=${token}`;
            console.error("Database name not available");
        }
            else {
            console.error("Error with the database selection");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function addWord(token, databaseName, foreign, native) {
    fetch(
        `/v1/database/add-word?token=${token}`,
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
        if (data && data.message === "Word added successfully") {
            window.location.href = `/v1/database/fill-database?token=${token}&databaseName=${databaseName}`;
        } else if (data && data.message === "Word already exists") {
            window.location.href = `/v1/database/fill-database?token=${token}&databaseName=${databaseName}&errorMessage=${data.message}`;
        } else {
            console.error("Error with the word creation");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function deleteDatabase(token) {
    var dropdown = document.getElementById("dropdown");
    var databaseName = dropdown.value;
    fetch(
        `/v1/database/delete-database?token=${token}`,
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
        if (data && data.message === "Database deleted successfully") {
            window.location.href = `/v1/database/list-databases?token=${token}`;
        } else {
            console.error("Error with the database deletion");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function uploadCSV(token) {
    console.log("Uploading CSV file...");
    var formData = new FormData();
    var fileInput = document.getElementById("csvFile");
    formData.append("csvFile", fileInput.files[0]);
    fetch(
        `/v1/database/upload-csv?token=${token}`,
        {
            method: "POST",
            body: formData
        }
    )
    .then(response => {
        if (response.ok) {
            return response.text();
        }
        throw new Error("Network response was not ok");
    })
    .then(data => {
        // Handle response from the server
        console.log("Data extracted from the server");
    })
    .catch(error => {
        // Handle errors
        console.error("Error in csv loading:", error);
    });
}