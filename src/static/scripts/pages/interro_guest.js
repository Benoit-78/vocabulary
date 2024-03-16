document.addEventListener(
    "DOMContentLoaded",
    function () {
        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = `${progressBar}%`;
    }
);


function sendUserSettings(testType, numWords, token) {
    console.log("testType:", testType);
    console.log("numWords:", numWords);
    console.log("token:", token);
    fetch(
        `/guest/save-interro-settings-guest?token=${token}`,
        {
            method: "POST",
            headers:
            {
                "Content-Type": "application/json",
                // "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                testType: testType,
                numWords: numWords,
            })
        }
    )
    .then(answer => answer.json())
    .then(data => {
        startTest(numWords, token, loader, test)
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function startTest(numWords, token, loader, test) {
    numWords = parseInt(numWords, 10);
    // Check if the conversion was successful
    if (!isNaN(numWords)) {
        // const userId = getUserId(); // Function to retrieve user ID or username
        // localStorage.setItem(`loader_${userId}`, JSON.stringify(loader));
        // localStorage.setItem(`test_${userId}`, JSON.stringify(test));
        window.location.href = `/guest/interro-question-guest/${numWords}/0/0?token=${token}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}

// const userId = getUserId(); // Function to retrieve user ID or username
// const loader = JSON.parse(localStorage.getItem(`loader_${userId}`));
// const test = JSON.parse(localStorage.getItem(`test_${userId}`));


function showTranslation(numWords, count, score) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    if (!isNaN(numWords)) {
        window.location.href = `/interro-answer-guest/${numWords}/${count}/${score}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function sendUserAnswer(answer, count, numWords, score, content_box1, content_box2) {
    fetch("/user-answer-guest", {
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
            nextGuess(numWords, count, score);
        } else {
            endInterro(numWords, count, score);
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(numWords, count, score) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    window.location.href = `/interro-question-guest/${numWords}/${count}/${score}`;
}


function endInterro(numWords, count, score) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    if (score === numWords) {
        window.location.href = `/interro-end-guest/${numWords}/${score}`;
    } else {
        window.location.href = `/propose-rattraps-guest/${numWords}/${count}/${score}`;
    }
}
