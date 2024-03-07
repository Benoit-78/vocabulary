
function createAccount() {
    var inputNameElement = document.getElementById("content_box1") as HTMLInputElement;
    var inputPasswordElement = document.getElementById("content_box2") as HTMLInputElement;
    if (inputNameElement) {
        var inputName = inputNameElement.value;
    }
    
    if (inputPasswordElement) {
        var inputPassword = inputPasswordElement.value;
    }
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
    var inputNameElement = document.getElementById("inputName") as HTMLInputElement;
    var inputPasswordElement = document.getElementById("inputPassword") as HTMLInputElement;
    if (inputNameElement) {var inputName = inputNameElement.value;}
    if (inputPasswordElement) {var inputPassword = inputPasswordElement.value;}
    fetch("/user/authenticate-user", {
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
                console.log("User credentials validated successfully.");
                document.body.innerHTML = data;
            } else {
                window.location.href = "/sign-in";
                console.error("Invalid credentials");
            }
        })
    .catch(error => {
        console.error("Error:", error);
    });
}


function goToUserDashboards(userName, userPassword) {
    window.location.href = `/user/user-dashboards?userName=${userName}&userPassword=${userPassword}`;
}


function goToUserSettings(userName: string, userPassword: string) {
    const params = {
        userName: userName,
        userPassword: userPassword
    };
    const searchParams = new URLSearchParams(params);
    window.location.href = `/user/user-settings?${searchParams.toString()}`;
}


function goToUserSpace(userName, userPassword) {
    window.location.href = `/user/user-space?userName=${userName}&userPassword=${userPassword}`;
}