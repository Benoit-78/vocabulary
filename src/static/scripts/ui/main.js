import { goToRoot, interroGuest } from "../api/main.js";


document.addEventListener("DOMContentLoaded", function() {
    const guestInterroButton = document.getElementById("guestInterroButton");
    const token = document.body.dataset.token;

    guestInterroButton.addEventListener("click", function() {
        interroGuest(token);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const quitButton = document.getElementById("quitButton");
    const token = document.body.dataset.token;

    quitButton.addEventListener("click", function() {
        goToRoot(token);
    });
});