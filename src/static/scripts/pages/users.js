
function createAccount() {
    var inputName = document.getElementById("content_box1").value;
    var inputPassword = document.getElementById("content_box2").value;
    fetch("/create-user-account", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            input_name: inputName,
            input_password: inputPassword
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.message === "User account created successfully") {
            // Use sessionStorage to store userName
            sessionStorage.setItem('userName', data.userName);
            // Redirect to user-space with userName as a query parameter
            window.location.href = `/user-space?userName=${data.userName}?userPassword=${data.userPassword}`;
        } else if (data && data.message === "User name not available") {
            // Redirect to create-account route
            window.location.href = "/create-account";
        } else {
            console.error("Unable to create user account");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function signIn() {
    var inputName = document.getElementById("content_box1").value;
    var inputPassword = document.getElementById("content_box2").value;
    fetch("/authenticate-user", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            input_name: inputName,
            input_password: inputPassword
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.message === "User credentials validated successfully") {
            window.location.href = `/user-space?userName=${data.userName}?userPassword=${data.userPassword}`;
        } else {
            // Redirect to sign-in route
            window.location.href = "/sign-in";
            console.error("Invalid credentials");
        }
    })
    .catch(error => {
        console.error("", error);
    });
}


function goToUserSpace(userName, userPassword) {
    window.location.href = `/user-space?userName=${userName}?userPassword=${userPassword}`;
}

function goToUserDatabases(userName, userPassword) {
    window.location.href = `/user-databases?userName=${userName}?userPassword=${userPassword}`;
}


function createDatabase(userName, userPassword) {
    var databaseName = document.getElementById("databaseName").value;
    fetch("/create-database", {
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
            window.location.href = `/interro-settings/${userName}`;
        } else {
            // Redirect to sign-in route
            window.location.href = `/user-space?userName=${userName}?userPassword=${userPassword}`;
            console.error("Invalid credentials");
        }
    })
    .catch(error => {
        console.error("", error);
    });
}


var databaseNames = ["Database1", "Database2", "Database3"];
// Get the select element
var selectMenu = document.getElementById("menu");
// Dynamically add options based on the database names
databaseNames.forEach(function(name) {
    var option = document.createElement("option");
    option.value = name;
    option.text = name;
    selectMenu.add(option);
});