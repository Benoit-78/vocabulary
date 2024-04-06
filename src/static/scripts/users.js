
async function createAccount(token) {
    console.log("createAccount function called");
    const inputName = document.getElementById("inputName").value;
    const inputPassword = document.getElementById("inputPassword").value;
    const formData = new URLSearchParams();
    formData.append("username", inputName);
    formData.append("password", inputPassword);
    try {
        const response = await fetch(
            `/user/create-user-account?token=${token}`,
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    input_name: inputName,
                    input_password: inputPassword
                }),
            }
        )
        const data = await response.json();
        console.log("Response Data:", data);
        if (data && data.message === "User account created successfully") {
            const accessToken = data.token;
            window.location.href = `/user/user-space?token=${accessToken}`;
        } else if (data && data.message === "User name not available") {
            window.location.href = `/sign-up?token=${accessToken}`;
        } else {
            console.error("Error during the creation of user account");
        }
    } catch(error) {
        console.error("Error:", error);
    };
}


function signIn(token) {
    window.location.href = `/sign-in?token=${token}`;
}


async function authenticateUser() {
    const inputName = document.getElementById("inputName").value;
    const inputPassword = document.getElementById("inputPassword").value;
    const formData = new URLSearchParams();
    formData.append("username", inputName);
    formData.append("password", inputPassword);
    try {
        const response = await fetch(
            "/user/user-token",
            {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: formData.toString(),
            }
        );
        if (response.ok) {
            const data = await response.json();
            const token = data.access_token;
            window.location.href = `/user/user-space?token=${token}`;
        } else {
            console.error("Sign-in failed:", response.statusText);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}


function goToUserDashboards(token) {
    window.location.href = `/user/user-dashboards?token=${token}`;
}


function goToUserSettings(token) {
    window.location.href = `/user/user-settings?token=${token}`;
}


function goToUserSpace(token) {
    window.location.href = `/user/user-space?token=${token}`;
}
