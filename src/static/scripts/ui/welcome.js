import { interroGuest, signUp, aboutTheApp, help } from "../api/welcome.js";


document.addEventListener("DOMContentLoaded", function() {
    const guestButton = document.getElementById("guestButton");
    const token = document.body.dataset.token;

    guestButton.addEventListener("click", function() {
        interroGuest(token);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const signUpButton = document.getElementById("signUpButton");
    const token = document.body.dataset.token;

    signUpButton.addEventListener("click", function() {
        signUp(token);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const aboutButton = document.getElementById("aboutButton");
    const token = document.body.dataset.token;

    aboutButton.addEventListener("click", function() {
        aboutTheApp(token);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const helpButton = document.getElementById("helpButton");
    const token = document.body.dataset.token;

    helpButton.addEventListener("click", function() {
        help(token);
    });
});
