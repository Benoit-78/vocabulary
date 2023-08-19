document.addEventListener("DOMContentLoaded", function () {
    const progressBar = document.getElementById("progress-bar");
    progressBar.style.width = `${progress_percent}%`;
});


function goToRoot() {
    window.location.href = '/';
}


function showTranslation() {
    window.location.href = '/interro_2';
}


function nextGuess() {
    window.location.href = '/interro_1';
}