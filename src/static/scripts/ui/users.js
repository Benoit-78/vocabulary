import { authenticateUser, goToUserDashboards, goToUserSettings, createAccount, goToUserSpace } from "../api/users.js";


document.addEventListener("DOMContentLoaded", function() {
    const signInButton = document.getElementById("signInButton");
    const token = document.body.dataset.token;

    signInButton.addEventListener("click", function(event) {
        event.preventDefault();

        const inputName = document.getElementById("inputName").value;
        const inputPassword = document.getElementById("inputPassword").value;
        const formData = new URLSearchParams();
        formData.append("username", inputName);
        formData.append("password", inputPassword);
        authenticateUser(token, formData);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const signUpButton = document.getElementById("signUpButton");
    const token = document.body.dataset.token;

    signUpButton.addEventListener("click", function(event) {
        event.preventDefault();

        const inputName = document.getElementById("inputName").value;
        const inputPassword = document.getElementById("inputPassword").value;
        createAccount(token, inputName, inputPassword);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const dashboardButton = document.getElementById("dashboardButton");
    const token = document.body.dataset.token;

    dashboardButton.addEventListener("click", function() {
        goToUserDashboards(token);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const userSettingsButton = document.getElementById("userSettingsButton");
    const token = document.body.dataset.token;

    userSettingsButton.addEventListener("click", function() {
        goToUserSettings(token);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const userSpaceButton = document.getElementById("userSpaceButton");
    const token = document.body.dataset.token;

    userSpaceButton.addEventListener("click", function() {
        goToUserSpace(token);
    });
});
