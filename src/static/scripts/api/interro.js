
function goToInterroSettings(token) {
    window.location.href = `/interro/interro-settings?token=${token}`;
}


function sendUserSettings(token, language, testType, numWords) {
    console.log("Language:", language);
    console.log("Test type:", testType);
    console.log("Number of words:", numWords);
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
    .then(response => response.json())
    .then(data => {
        if (data && data.message === "Settings saved successfully") {
            numWords = data.test_length;
            startTest(token, numWords)
        } else if (data && data.message === "Empty table") {
            window.location.href = `/interro/interro-settings?token=${token}&errorMessage=${data.message}`;
        } else {
            console.error("Unknown message at interro creation:", data.message);
        }
    })
    .catch(error => {
        console.error("Error with the interro creation:", error);
    });
}


function startTest(token, numWords) {
    total = parseInt(numWords, 10);
    count = 0;
    score = 0;
    console.log("Number of words:", total);
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
    console.log("Number of words:", total);
    if (!isNaN(numWords)) {
        window.location.href = `/interro/interro-answer?token=${token}&total=${total}&count=${count}&score=${score}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function sendUserAnswer(token, answer, count, numWords, score, content_box1, content_box2) {
    console.log("numWords:", numWords);
    console.log("Count:", count);
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
            if (count < numWords) {
                nextGuess(token, numWords, count, score);
            } else {
                endInterro(token, numWords, count, score);
            }
        } else {
            console.error("Error with user answer acquisition");
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
            count = data.count;
            score = data.score;
            window.location.href = `/interro/interro-question?token=${token}&total=${total}&count=${count}&score=${score}`;
        } else {
            console.error("Error with rattraps creation.");
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    })
}