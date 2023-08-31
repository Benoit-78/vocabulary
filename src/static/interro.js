function goToRoot() {
    window.location.href = '/';
}


function startTest() {
    window.location.href = '/interro_question';
}


function showTranslation() {
    window.location.href = '/interro_answer';
}


function nextGuess() {
    window.location.href = '/interro_question';
}


function endInterro(score, numberOfQuestions) {
    if (score === numberOfQuestions) {
        window.location.href = '/interro_end';
    } else {
        window.location.href = '/propose_rattraps';
    }
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


function sendUserAnswer(answer, progressBar, numberOfQuestions, score) {
    fetch("/user-answer", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            answer: answer,
            progress_percent: progressBar,
            number_of_questions: numberOfQuestions
        }),
    })
    .then(answer => answer.json())
    .then(data => {
        if (progressBar <= numberOfQuestions) {
            nextGuess();
        } else {
            score++;
            endInterro(score, numberOfQuestions);
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
