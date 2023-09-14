function goToRoot() {
    window.location.href = '/';
}


document.addEventListener(
    "DOMContentLoaded",
    function () {
        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = `${progressBar}%`;
    }
);


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
        startTest(numWords)
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function startTest(numWords) {
    numWords = parseInt(numWords, 10);
    // Check if the conversion was successful
    if (!isNaN(numWords)) {
        window.location.href = `/interro_question/${numWords}/0/0`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function showTranslation(numWords, count, score) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    if (!isNaN(numWords)) {
        window.location.href = `/interro_answer/${numWords}/${count}/${score}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function sendUserAnswer(answer, count, numberOfQuestions, score, content_box1, content_box2) {
    fetch("/user-answer", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            answer: answer,
            count: count,
            number_of_questions: numberOfQuestions,
            score: score,
            english: content_box1,
            french: content_box2
        }),
    })
    .then(answer => answer.json())
    .then(data => {
        // Extract the updated score from the JSON response
        const score = data.score;
        if (count < numberOfQuestions) {
            nextGuess();
        } else {
            endInterro(score, numberOfQuestions);
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
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


function nextCatchupGuess() {
    window.location.href = '/rattraps_question';
}