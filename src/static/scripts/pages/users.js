function createAccount() {
    var inputNameElement = document.getElementById("content_box1");
    var inputPasswordElement = document.getElementById("content_box2");
    if (inputNameElement) {
        var inputName = inputNameElement.value;
    }
    if (inputPasswordElement) {
        var inputPassword = inputPasswordElement.value;
    }
    fetch("/create-user-account", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            input_name: inputName,
            input_password: inputPassword
        }),
    })
        .then(function (response) { return response.json(); })
        .then(function (data) {
        if (data && data.message === "User account created successfully") {
            // Use sessionStorage to store userName
            sessionStorage.setItem('userName', data.userName);
            // Redirect to user-space with userName as a query parameter
            window.location.href = "/user-space?userName=".concat(data.userName, "?userPassword=").concat(data.userPassword);
        }
        else if (data && data.message === "User name not available") {
            // Redirect to create-account route
            window.location.href = "/create-account";
        }
        else {
            console.error("Unable to create user account");
        }
    })
        .catch(function (error) {
        console.error("Error sending user answer:", error);
    });
}
function signIn() {
    var inputNameElement = document.getElementById("inputName");
    var inputPasswordElement = document.getElementById("inputPassword");
    if (inputNameElement) {var inputName = inputNameElement.value;}
    if (inputPasswordElement) {var inputPassword = inputPasswordElement.value;}
    fetch("/user/authenticate-user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            input_name: inputName,
            input_password: inputPassword
        }),
    })
    .then(function (response) {
        if (response.ok) {
            return response.text();
        } else {
            console.error('Error:', response.statusText);
            return Promise.reject('Error occurred');
        }
    })
    .then(function (data) {
        if (data && data.message === "User credentials validated successfully") {
            console.log("User credentials validated successfully.");
            document.body.innerHTML = data;
        }
        else {
            window.location.href = "/sign-in";
            console.error("Invalid credentials");
        }
    })
        .catch(function (error) {
        console.error("Error:", error);
    });
}
function goToUserDashboards(userName, userPassword) {
    window.location.href = "/user/user-dashboards?userName=".concat(userName, "&userPassword=").concat(userPassword);
}
function goToUserSettings(userName, userPassword) {
    var params = {
        userName: userName,
        userPassword: userPassword
    };
    var searchParams = new URLSearchParams(params);
    window.location.href = "/user/user-settings?".concat(searchParams.toString());
}
function goToUserSpace(userName, userPassword) {
    window.location.href = "/user/user-space?userName=".concat(userName, "&userPassword=").concat(userPassword);
}
