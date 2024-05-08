import { signIn, goToUserDashboards, goToUserSettings} from "../api/users.js";


document.addEventListener("DOMContentLoaded", function() {
    const signInButton = document.getElementById("signInButton");
    const token = document.body.dataset.token;

    signInButton.addEventListener("click", function() {
        signIn(token);
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
