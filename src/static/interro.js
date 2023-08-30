function startTest() {
    window.location.href = '/interro_question';
}


function goToRoot() {
    window.location.href = '/';
}


function showTranslation() {
    window.location.href = '/interro_answer';
}


function nextGuess() {
    window.location.href = '/interro_question';
}


function endInterro() {
    window.location.href = '/interro_end';
}


function sendUserSettings(testType, numWords) {
    fetch("/user-settings", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            testType: testType,
            numWords: numWords
        }),
    })
    .then(answer => answer.json())
    .then(data => {
        startTest()
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function sendUserAnswer(answer, progressBar, numberOfQuestions) {
    fetch("/user-answer", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            answer: answer,
            progress_percent: progressBar
        }),
    })
    .then(answer => answer.json())
    .then(data => {
        if (progressBar <= numberOfQuestions) {
            nextGuess();
        } else {
            endInterro();
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


document.addEventListener(
    "DOMContentLoaded",
    function () {
        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = `${progress_percent}%`;
    }
);