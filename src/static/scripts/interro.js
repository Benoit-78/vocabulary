
document.addEventListener(
    "DOMContentLoaded",
    function () {
        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = `${progressBar}%`;
    }
);

function goToInterroSettings(token) {
    window.location.href = `/interro/interro-settings?token=${token}`;
}


function sendUserSettings(token, databaseName, testType, numWords) {
    fetch(
        `/interro/save-interro-settings?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                databaseName: databaseName,
                testType: testType,
                numWords: numWords
            })
        }
    )
    .then(response => {
        if (!response.ok) { // Check if the response status is NOK (outside the range 200-299)
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        startTest(token, databaseName)
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function startTest(token, databaseName) {
    total = parseInt(numWords, 10);
    if (!isNaN(numWords)) {
        // Check if the conversion was successful
        const params = {
            token: {token},
            databaseName: {databaseName},
            testType: {testType},
            total: {total},
            count: 0,
            score: 0,
        };
        // Create a new URLSearchParams object and append each parameter
        const searchParams = new URLSearchParams(params);
        // Construct the URL with the parameters
        window.location.href = `/interro/interro-question?${searchParams.toString()}`;
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
    fetch(`/user-answer/${userName}`, {
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