function createAccount() {
    var inputNameElement = document.getElementById("content_box1");
    var inputPasswordElement = document.getElementById("content_box2");
    if (inputNameElement) {
        var inputName = inputNameElement;
    }
    if (inputPasswordElement) {
        var inputPassword = inputPasswordElement;
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


function signIn(token) {
    window.location.href = `/sign-in?token=${token}`;
}


async function authenticateUser() {
    const formData = new FormData(document.getElementById('signInForm'));
    console.log(formData)
    try {
        console.log("Sending sign-in request...");
        const response = await fetch(
            "/user/user-token",
            {
                method: "POST",
                body: formData,
            }
        );
        console.log("Authentication request completed.");
        if (response.ok) {
            console.log("Sign-in successful. Processing response...");
            const data = await response.json();
            const accessToken = data.access_token;
            window.location.href = `/user/user-space?token=${accessToken}`;
        } else {
            console.error("Sign-in failed:", response.statusText);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}


function goToUserDashboards(userName, userPassword) {
    window.location.href = `/user/user-dashboards?userName=${userName}&userPassword=${userPassword})`;
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
