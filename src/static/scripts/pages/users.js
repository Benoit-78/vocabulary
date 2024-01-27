
function createAccount() {
    var inputName = document.getElementById("content_box1").value;
    var inputPassword = document.getElementById("content_box2").value;
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
        if (data && data.message === "User account created successfully") {
            // Use sessionStorage to store userName
            sessionStorage.setItem('userName', data.userName);
            // Redirect to user-space with userName as a query parameter
            window.location.href = `/user-space?userName=${data.userName}`;
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
