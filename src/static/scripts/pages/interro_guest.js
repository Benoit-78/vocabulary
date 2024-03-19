document.addEventListener(
    "DOMContentLoaded",
    function () {
        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = `${progressBar}%`;
    }
);


function sendUserSettings(testType, numWords, token) {
    fetch(
        `/guest/save-interro-settings?token=${token}`,
        {
            method: "POST",
            headers:
            {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                testType: testType,
                numWords: numWords,
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
        startTest(numWords, token)
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function startTest(numWords, token) {
    numWords = parseInt(numWords, 10);
    // Check if the conversion was successful
    if (!isNaN(numWords)) {
        window.location.href = `/guest/interro-question/${numWords}/0/0?token=${token}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}



function showTranslation(numWords, count, score, token) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    if (!isNaN(numWords)) {
        window.location.href = `/guest/interro-answer/${numWords}/${count}/${score}?token=${token}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function sendUserAnswer(answer, count, numWords, score, content_box1, content_box2, token) {
    fetch(
        `/guest/user-answer?token=${token}`,
        {
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
        }
    )
    .then(answer => answer.json())
    .then(data => {
        // Extract the updated score from the JSON response
        const score = data.score;
        if (count < numWords) {
            nextGuess(numWords, count, score, token);
        } else {
            endInterro(numWords, count, score, token);
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(numWords, count, score, token) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    window.location.href = `/guest/interro-question/${numWords}/${count}/${score}?token=${token}`;
}


function endInterro(numWords, count, score, token) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    if (score === numWords) {
        window.location.href = `/guest/interro-end/${numWords}/${score}?token=${token}`;
    } else {
        window.location.href = `/guest/propose-rattraps/${numWords}/${count}/${score}?token=${token}`;
    }
}
