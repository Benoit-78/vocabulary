export { goToInterroSettings, sendUserSettings, showTranslation, sendUserAnswer, launchRattraps };


function goToInterroSettings(token) {
    window.location.href = `/v1/interro/interro-settings?token=${token}`;
}


function sendUserSettings(token, databaseName, testType, numWords) {
    fetch(
        `/v1/interro/save-interro-settings?token=${token}`,
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
    .then(response => response.json())
    .then(data => {
        if (data && data.message === "Settings saved successfully") {
            numWords = data.test_length;
            startTest(token, numWords, data.interro_category)
        } else if (data && data.message === "Empty table") {
            window.location.href = `/v1/interro/interro-settings?token=${token}&errorMessage=${data.message}`;
        } else {
            console.error("Unknown message at interro creation:", data.message);
        }
    })
    .catch(error => {
        console.error("Error with the interro creation:", error);
    });
}


function startTest(token, numWords, interroCategory) {
    var total = parseInt(numWords, 10);
    var count = 0;
    var score = 0;
    // Check if the conversion was successful
    if (!isNaN(numWords)) {
        window.location.href = `/v1/interro/interro-question?token=${token}&interroCategory=${interroCategory}&total=${total}&count=${count}&score=${score}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function showTranslation(token, interroCategory, numWords, count, score) {
    var total = parseInt(numWords, 10);
    var count = parseInt(count, 10);
    var score = parseInt(score, 10);
    if (!isNaN(numWords)) {
        window.location.href = `/v1/interro/interro-answer?token=${token}&interroCategory=${interroCategory}&total=${total}&count=${count}&score=${score}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function sendUserAnswer(token, interroCategory, answer, count, numWords, score, content_box1, content_box2) {
    var total = parseInt(numWords, 10);
    var count = parseInt(count, 10);
    // console.log("Total:", total, "Count:", count);
    fetch(
        `/v1/interro/user-answer?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                interroCategory,
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
            // console.log("Total:", total, "Count:", count);
            // console.log(count < total)
            var score = parseInt(data.score, 10);
            if (count < total) {
                nextGuess(token, interroCategory, total, count, score);
            } else {
                endInterro(token, interroCategory, total, score);
            }
        } else {
            console.error("Error with user answer acquisition");
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(token, interroCategory, numWords, count, score) {
    var total = parseInt(numWords, 10);
    var count = parseInt(count, 10);
    var score = parseInt(score, 10);
    // console.log("Total:", total, "Count:", count);
    window.location.href = `/v1/interro/interro-question?token=${token}&interroCategory=${interroCategory}&total=${total}&count=${count}&score=${score}`;
}


function launchRattraps(token, interroCategory, newTotal, newCount, newScore) {
    fetch(
        `/v1/interro/launch-rattraps?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                interroCategory: interroCategory,
                count: newCount,
                total: newTotal,
                score: newScore,
            }),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "Rattraps created successfully") {
            const interroCategory = data.interroCategory;
            const total = data.total;
            const count = data.count;
            const score = data.score;
            window.location.href = `/v1/interro/interro-question?token=${token}&interroCategory=${interroCategory}&total=${total}&count=${count}&score=${score}`;
        } else {
            console.error("Error with rattraps creation.");
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    })
}


function endInterro(token, interroCategory, numWords, score) {
    var total = parseInt(numWords, 10);
    var score = parseInt(score, 10);
    if (score === total) {
        window.location.href = `/v1/interro/interro-end?token=${token}&interroCategory=${interroCategory}&total=${total}&score=${score}`;
    } else {
        window.location.href = `/v1/interro/propose-rattraps?token=${token}&interroCategory=${interroCategory}&total=${total}&score=${score}`;
    }
}
