import { goToRoot } from "../api/main.js";


document.addEventListener("DOMContentLoaded", function() {
    const quitButton = document.getElementById("quitButton");
    const token = document.body.dataset.token;

    quitButton.addEventListener("click", function() {
        goToRoot(token);
    });
});
