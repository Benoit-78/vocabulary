
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


function sendUserSettings(token, language, testType, numWords) {
    fetch(
        `/interro/save-interro-settings?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                databaseName: language,
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
        startTest(token, numWords)
    })
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function startTest(token, numWords) {
    total = parseInt(numWords, 10);
    count = 0;
    score = 0;
    // Check if the conversion was successful
    if (!isNaN(numWords)) {
        window.location.href = `/interro/interro-question?token=${token}&total=${total}&count=${count}&score=${score}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function showTranslation(token, numWords, count, score) {
    total = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    if (!isNaN(numWords)) {
        window.location.href = `/interro/interro-answer?token=${token}&total=${total}&count=${count}&score=${score}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function sendUserAnswer(token, answer, count, numWords, score, content_box1, content_box2) {
    fetch(
        `/interro/user-answer?token=${token}`,
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
        if (data && data.message === "User response stored successfully") {
            const score = data.score;
            console.log("Score:", score);
            if (count < numWords) {
                nextGuess(token, numWords, count, score);
            } else {
                endInterro(token, numWords, count, score);
            }
        } else {
            console.error("Error with user answer acquisition.");
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(token, numWords, count, score) {
    total = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    window.location.href = `/interro/interro-question?token=${token}&total=${total}&count=${count}&score=${score}`;
}


function endInterro(token, numWords, count, score) {
    total = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    console.log("Total:", total);
    console.log("Count:", count);
    console.log("Score:", score);
    if (score === total) {
        window.location.href = `/interro/interro-end?token=${token}&total=${total}&score=${score}`;
    } else {
        window.location.href = `/interro/propose-rattraps?token=${token}&total=${total}&score=${score}`;
    }
}


function launchRattraps(token, newTotal, newCount, newScore) {
    console.log("Total:", newTotal);
    console.log("Count:", newCount);
    console.log("Score:", newScore);
    fetch(
        `/interro/launch-rattraps?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                count: newCount,
                total: newTotal,
                score: newScore,
            }),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "Rattraps created successfully") {
            total = data.total;
            console.log("Total:", total);
            count = data.count;
            console.log("Count:", count);
            score = data.score;
            console.log("Score:", score);
            window.location.href = `/interro/interro-question?token=${token}&total=${total}&count=${count}&score=${score}`;
        } else {
            console.error("Error with rattraps creation.");
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    })
}