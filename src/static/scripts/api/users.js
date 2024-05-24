export { authenticateUser, goToUserDashboards, goToUserSettings, createAccount, goToUserSpace };


async function createAccount(token, inputName, inputPassword) {
    try {
        const response = await fetch(
            `/user/create-user-account?token=${token}`,
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(
                    {
                        input_name: inputName,
                        input_password: inputPassword
                    }
                ),
            }
        )
        const data = await response.json();
        if (data && data.message === "User account created successfully") {
            window.location.href = `/user/user-space?token=${data.token}`;
        } else if (data && data.message === "User name not available") {
            window.location.href = `/sign-up?token=${data.token}&errorMessage=${data.message}`;
        } else if (data && data.message === "User name or password not provided") {
            window.location.href = `/sign-up?token=${data.token}&errorMessage=${data.message}`;
        } else {
            console.error("Error in sign-up");
        }
    } catch(error) {
        console.error("Error:", error);
    };
}


async function authenticateUser(token, formData) {
    console.log("formData:", formData.toString());
    console.log("username:", formData.get("username"));
    console.log("password:", formData.get("password"));
    try {
        const response = await fetch(
            `/user/user-token?token=${token}`,
            {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: formData.toString(),
            }
        );
        const data = await response.json();
        console.log(data);
        if (data && data.message === "User successfully authenticated") {
            window.location.href = `/user/user-space?token=${data.token}`;
        } else if (data && data.message === "Unknown user") {
            window.location.href = `/sign-in?token=${data.token}&errorMessage=${data.message}`;
        } else if (data && data.message === "Password incorrect") {
            window.location.href = `/sign-in?token=${data.token}&errorMessage=${data.message}`;
        } else if (data && data.message === "User name or password not provided") {
            window.location.href = `/sign-in?token=${data.token}&errorMessage=${data.message}`;
        } else {
            console.error("Error in sign-in");
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
