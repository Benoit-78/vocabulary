export { sendGuestSettings, showTranslation, sendUserAnswer, nextGuess, launchRattrap };


function sendGuestSettings(token, testLanguage) {
    fetch(
        `/v1/guest/save-interro-settings?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                testLanguage: testLanguage
            })
        }
    )
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        startTest(token, testLanguage.toLowerCase(), data.interroCategory)
    })
    .catch(error => {
        console.error("Error sending guest settings:", error);
    });
}


function startTest(token, testLanguage, interroCategory) {
    var testLength = 10;
    var testCount = 0;
    var testScore = 0;
    window.location.href = `/v1/guest/interro-question?token=${token}&interroCategory=${interroCategory}&testLength=${testLength}&testCount=${testCount}&testScore=${testScore}&testLanguage=${testLanguage.toLowerCase()}`;
}


function showTranslation(token, interroCategory, testLength, testCount, testScore, testLanguage) {
    var testLength = parseInt(testLength, 10);
    var testCount = parseInt(testCount, 10);
    var testScore = parseInt(testScore, 10);
    console.log("Test length:", testLength, "Count:", testCount, "Score:", testScore);
    console.log("Test language:", testLanguage);
    if (!isNaN(testLength)) {
        window.location.href = `/v1/guest/interro-answer?token=${token}&interroCategory=${interroCategory}&testLength=${testLength}&testCount=${testCount}&testScore=${testScore}&testLanguage=${testLanguage.toLowerCase()}`;
    } else {
        console.error("Invalid testLength:", testLength);
    }
}


function sendUserAnswer(token, interroCategory, userAnswer, testCount, testLength, testScore, contentBox1, contentBox2, testLanguage) {
    var testLength = parseInt(testLength, 10);
    var testCount = parseInt(testCount, 10);
    var testScore = parseInt(testScore, 10);
    var testLanguage = String(testLanguage);
    fetch(
        `/v1/guest/user-answer?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                interroCategory,
                userAnswer: userAnswer,
                testCount: testCount,
                testLength: testLength,
                testScore: testScore,
                foreignWord: contentBox1,
                nativeWord: contentBox2
            }),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        const testScore = data.testScore;
        const testLength = data.testLength;
        if (testCount < testLength) {
            nextGuess(token, interroCategory, testLength, testCount, testScore, testLanguage.toLowerCase());
        } else {
            endInterro(token, interroCategory, testLength, testScore, testLanguage.toLowerCase());
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(token, interroCategory, testLength, testCount, testScore, testLanguage) {
    var testLength = parseInt(testLength, 10);
    var testCount = parseInt(testCount, 10);
    var testScore = parseInt(testScore, 10);
    window.location.href = `/v1/guest/interro-question?token=${token}&interroCategory=${interroCategory}&testLength=${testLength}&testCount=${testCount}&testScore=${testScore}&testLanguage=${testLanguage.toLowerCase()}`;
}


function launchRattrap(token, interroCategory, newLength, newCount, newScore, testLanguage) {
    var testLength = parseInt(newLength, 10);
    var testCount = parseInt(newCount, 10);
    var testScore = parseInt(newScore, 10);
    console.log("New length:", newLength, "Count:", testCount, "Score:", testScore);
    fetch(
        `/v1/guest/launch-guest-rattrap?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                interroCategory: interroCategory,
                testCount: testCount,
                testLength: testLength,
                testScore: testScore,
            }),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "Guest rattrap created successfully") {
            const interroCategory = data.interroCategory;
            const testLength = data.testLength;
            const testCount = data.testCount;
            const testScore = data.testScore;
            window.location.href = `/v1/guest/interro-question?token=${token}&interroCategory=${interroCategory}&testLength=${testLength}&testCount=${testCount}&testScore=${testScore}&testLanguage=${testLanguage}`;
        } else {
            console.error("Error with guest rattrap creation.");
        }
    })
    .catch(error => {
        console.error("Error sending guest response:", error);
    })
}


function endInterro(token, interroCategory, testLength, testScore, testLanguage) {
    var testLength = parseInt(testLength, 10);
    var testScore = parseInt(testScore, 10);
    if (testScore === testLength) {
        window.location.href = `/v1/guest/interro-end?token=${token}&testLength=${testLength}&testScore=${testScore}`;
    } else {
        window.location.href = `/v1/guest/propose-rattrap?token=${token}&interroCategory=${interroCategory}&testLength=${testLength}&testScore=${testScore}&testLanguage=${testLanguage.toLowerCase()}`;
    }
}
