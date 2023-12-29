document.addEventListener(
    "DOMContentLoaded",
    function () {
        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = `${progressBar}%`;
    }
);


function sendUserSettings(userName, testType, numWords) {
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
        startTest(userName, numWords)
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function startTest(userName, numWords) {
    var encodedUserName = encodeURIComponent(userName)
    numWords = parseInt(numWords, 10);
    // Check if the conversion was successful
    if (!isNaN(numWords)) {
        window.location.href = `/interro-question/${encodedUserName}/${numWords}/0/0`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function showTranslation(userName, numWords, count, score) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    if (!isNaN(numWords)) {
        window.location.href = `/interro-answer/${userName}/${numWords}/${count}/${score}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function sendUserAnswer(userName, answer, count, numWords, score, content_box1, content_box2) {
    fetch("/user-answer", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            answer: answer,
            count: count,
            number_of_questions: numWords,
            score: score,
            english: content_box1,
            french: content_box2
        }),
    })
    .then(answer => answer.json())
    .then(data => {
        // Extract the updated score from the JSON response
        const score = data.score;
        if (count < numWords) {
            nextGuess(userName, numWords, count, score);
        } else {
            endInterro(userName, numWords, count, score);
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(userName, numWords, count, score) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    window.location.href = `/interro-question/${userName}/${numWords}/${count}/${score}`;
}


function endInterro(userName, numWords, count, score) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    if (score === numWords) {
        window.location.href = `/interro-end/${userName}/${numWords}/${score}`;
    } else {
        window.location.href = `/propose-rattraps/${userName}/${numWords}/${count}/${score}`;
    }
}
