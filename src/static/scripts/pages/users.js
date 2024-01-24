
function createAccount() {
    var inputName = document.getElementById("input1").value;
    var inputPassword = document.getElementById("input2").value;
    fetch("/create-account", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            input_name: inputName,
            input_password: inputPassword
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.message === "User credentials created successfully") {
            window.location.href = `/create-database/${data.userName}`;
        } else {
            console.error("Unable to create user account");
        }
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function signIn() {
    var inputName = document.getElementById("input1").value;
    var inputPassword = document.getElementById("input2").value;
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
            window.location.href = `/user-space/${data.userName}`;
        } else {
            console.error("Invalid credentials");
        }
    })
    .catch(error => {
        console.error("", error);
    });
}


function goToUserSpace(userName) {
    var encodedUserName = encodeURIComponent(userName)
    window.location.href = "/user-space/" + encodedUserName;
}
