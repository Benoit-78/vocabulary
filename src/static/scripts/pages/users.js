function goToUserSpace(userName) {
    var encodedUserName = encodeURIComponent(userName)
    window.location.href = "/user-space/" + encodedUserName;
}


function signIn() {
    var inputName = document.getElementById("input1").value;
    var inputPassword = document.getElementById("input2").value;
    fetch("/check-input-creds", {
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
        console.error("Error sending user answer:", error);
    });
}
