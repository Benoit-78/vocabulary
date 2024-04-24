
function goToUserDatabases(token) {
    window.location.href = `/database/list-databases?token=${token}`;
}


function chooseDatabase(token) {
    var dropdown = document.getElementById("dropdown");
    var databaseName = dropdown.value;
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
        if (data && data.message === "Database chosen successfully") {
            window.location.href = `/database/fill-database?token=${token}&databaseName=${databaseName}`;
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
        if (data && data.message === "Database created successfully") {
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


function deleteDatabase(token) {
    var dropdown = document.getElementById("dropdown");
    var databaseName = dropdown.value;
    fetch(
        `/database/delete-database?token=${token}`,
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
            window.location.href = `/database/list-databases?token=${token}`;
        } else {
            console.error("Error with the database deletion.");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
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
        if (data && data.message === "Word added successfully") {
            window.location.href = `/database/fill-database?token=${token}&databaseName=${databaseName}`;
        } else if (data && data.message === "Word already exists") {
            window.location.href = `/database/fill-database?token=${token}&databaseName=${databaseName}&errorMessage=${data.message}`;
        } else {
            console.error("Error with the word creation.");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


document.addEventListener(
    "DOMContentLoaded",
    function() {
        // Bind the submit event of the form to the uploadCSV function
        document.getElementById("csvForm").addEventListener(
            "submit",
            function(event) {
                event.preventDefault(); // Prevent the form from submitting normally
                var token = document.getElementById("token").value;
                uploadCSV(token); // Call the uploadCSV function
            }
        );
    }
);


function uploadCSV(token) {
    console.log("Uploading CSV file...");
    var formData = new FormData();
    var fileInput = document.getElementById("csvFile");
    formData.append("csvFile", fileInput.files[0]);
    fetch(
        `/database/upload-csv?token=${token}`,
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
        console.log(data);
    })
    .catch(error => {
        // Handle errors
        console.error("Error in csv loading:", error);
    });
}