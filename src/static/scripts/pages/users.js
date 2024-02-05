
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