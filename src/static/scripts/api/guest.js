export { sendGuestSettings, showTranslation, sendUserAnswer, nextGuess, launchRattraps };


function sendGuestSettings(token, language) {
    fetch(
        `/v1/guest/save-interro-settings?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                language: language
            })
        }
    )
    .then(response => {
        // Check if the response status is NOK (outside the range 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        startTest(token, language.toLowerCase(), data.interro_category)
    })
    .catch(error => {
        console.error("Error sending guest settings:", error);
    });
}


function startTest(token, language, interroCategory) {
    var total = 10;
    var count = 0;
    var score = 0;
    window.location.href = `/v1/guest/interro-question?token=${token}&interroCategory=${interroCategory}&total=${total}&count=${count}&score=${score}&language=${language.toLowerCase()}`;
}


function showTranslation(token, interroCategory, numWords, count, score, language) {
    var total = parseInt(numWords, 10);
    var count = parseInt(count, 10);
    var score = parseInt(score, 10);
    if (!isNaN(total)) {
        window.location.href = `/v1/guest/interro-answer?token=${token}&interroCategory=${interroCategory}&total=${total}&count=${count}&score=${score}&language=${language.toLowerCase()}`;
    } else {
        console.error("Invalid numWords:", total);
    }
}


function sendUserAnswer(token, interroCategory, answer, count, numWords, score, content_box1, content_box2, language) {
    var total = parseInt(numWords, 10);
    var count = parseInt(count, 10);
    var score = parseInt(score, 10);
    var language = String(language);
    fetch(
        `/v1/guest/user-answer?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                interroCategory,
                answer: answer,
                count: count,
                total: total,
                score: score,
                english: content_box1,
                french: content_box2
            }),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        const score = data.score;
        const total = data.total;
        // console.log("Score:", score, "Total:", total, "Count:", count);
        if (count < total) {
            nextGuess(token, interroCategory, total, count, score, language.toLowerCase());
        } else {
            endInterro(token, interroCategory, total, score, language.toLowerCase());
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(token, interroCategory, numWords, count, score, language) {
    var total = parseInt(numWords, 10);
    var count = parseInt(count, 10);
    var score = parseInt(score, 10);
    window.location.href = `/v1/guest/interro-question?token=${token}&interroCategory=${interroCategory}&total=${total}&count=${count}&score=${score}&language=${language.toLowerCase()}`;
}


function launchRattraps(token, interroCategory, newWords, newCount, newScore, language) {
    var total = parseInt(newWords, 10);
    var count = parseInt(newCount, 10);
    var score = parseInt(newScore, 10);
    console.log("Total:", total, "Count:", count, "Score:", score);
    fetch(
        `/v1/guest/launch-guest-rattraps?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                interroCategory: interroCategory,
                count: count,
                total: total,
                score: score,
            }),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "Guest rattraps created successfully") {
            const interroCategory = data.interroCategory;
            const total = data.total;
            const count = data.count;
            const score = data.score;
            // console.log("Total:", total, "Count:", count, "Score:", score);
            window.location.href = `/v1/guest/interro-question?token=${token}&interroCategory=${interroCategory}&total=${total}&count=${count}&score=${score}&language=${language}`;
        } else {
            console.error("Error with guest rattraps creation.");
        }
    })
    .catch(error => {
        console.error("Error sending guest response:", error);
    })
}


function endInterro(token, interroCategory, numWords, score, language) {
    var total = parseInt(numWords, 10);
    var score = parseInt(score, 10);
    if (score === total) {
        window.location.href = `/v1/guest/interro-end?token=${token}&total=${total}&score=${score}`;
    } else {
        window.location.href = `/v1/guest/propose-rattraps?token=${token}&interroCategory=${interroCategory}&total=${total}&score=${score}&language=${language.toLowerCase()}`;
    }
}
