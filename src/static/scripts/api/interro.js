export { goToInterroSettings, sendUserSettings, showTranslation, sendUserAnswer, launchRattraps };


function goToInterroSettings(token) {
    var errorMessage = ''
    window.location.href = `/v1/interro/interro-settings?token=${token}&errorMessage=${errorMessage}`;
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
            startTest(
                data.token,
                data.message,
                data.interro_category,
                data.interro_dict,
                data.test_length,
                data.index,
                data.faults_dict,
                data.perf
            )
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


function startTest(token, message, interroCategory, interroDict, numWords, index, faultsDict, perf) {
    var testLength = parseInt(numWords, 10);
    var count = 0;
    var score = 0;
    if (!isNaN(testLength)) {
        const params = new URLSearchParams({
            token: token,
            message: message,
            interroCategory: interroCategory,
            interroDict: interroDict,
            testLength: testLength,
            index: index,
            faultsDict: faultsDict,
            perf: perf,
            count: count,
            score: score
        });
        window.location.href = `/v1/interro/interro-question?${params.toString()}`;
    } else {
        console.error('Error:', error);
    }
}


function showTranslation(token, interroCategory, interroDict, testLength, index, faultsDict, perf, count, score) {
    var testLength = parseInt(testLength, 10);
    var count = parseInt(count, 10);
    var score = parseInt(score, 10);
    console.log(interroDict)
    if (!isNaN(testLength)) {
        const params = new URLSearchParams({
            token: token,
            interroCategory: interroCategory,
            interroDict: interroDict,
            testLength: testLength,
            index: index,
            faultsDict: faultsDict,
            perf: perf,
            count: count,
            score: score
        });
        window.location.href = `/v1/interro/interro-answer?${params.toString()}`;
    } else {
        console.error("Invalid testLength:", testLength);
    }
}


function sendUserAnswer(token, answer, interroCategory, interroDict, testLength, index,  faultsDict, perf, count, score) {
    console.log(interroDict)
    fetch(
        `/v1/interro/user-answer?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                interroCategory,
                answer: answer,
                interroDict: interroDict,
                testLength: testLength,
                index: index,
                faultsDict: faultsDict,
                perf: perf,
                count: count,
                score: score,
            }),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "User response stored successfully") {
            var score = parseInt(data.score, 10);
            if (count < total) {
                nextGuess(token, interroCategory, data.interroDict, testLength, index, data.faultsDict, perf, count, score);
            } else {
                endInterro(token, interroCategory, interroDict, testLength, faultsDict, perf, count, score);
            }
        } else {
            console.error("Error with user answer acquisition");
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(token, interroCategory, interroDict, testLength, index,  faultsDict, perf, count, score) {
    const params = new URLSearchParams({
        token: token,
        interroCategory: interroCategory,
        interroDict: interroDict,
        testLength: testLength,
        index: index,
        faultsDict: faultsDict,
        perf: perf,
        count: count,
        score: score
    });
    window.location.href = `/v1/interro/interro-question?${params.toString()}`;
    // window.location.href = `/v1/interro/interro-question?token=${token}&interroCategory=${interroCategory}&total=${total}&count=${count}&score=${score}`;
}


function endInterro(token, interroCategory, interroDict, testLength, faultsDict, perf, count, score) {
    var testLength = parseInt(testLength, 10);
    var score = parseInt(score, 10);
    if (score === testLength) {
        const params = new URLSearchParams({
            token: token,
            interroCategory: interroCategory,
            interroDict: interroDict,
            testLength: testLength,
            faultsDict: faultsDict,
            perf: perf,
            count: count,
            score: score
        });
        window.location.href = `/v1/interro/interro-end?${params.toString()}`;
        // window.location.href = `/v1/interro/interro-end?token=${token}&interroCategory=${interroCategory}&total=${total}&score=${score}`;
    } else {

        window.location.href = `/v1/interro/propose-rattraps?token=${token}&interroCategory=${interroCategory}&total=${total}&score=${score}`;
    }
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

