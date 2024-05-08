export { sendGuestSettings, showTranslation, sendUserAnswer, nextGuess };


function sendGuestSettings(token, language) {
    fetch(
        `/guest/save-interro-settings?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                language: language
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
        startTest(token, language.toLowerCase())
    })
    .catch(error => {
        console.error("Error sending guest settings:", error);
    });
}


function startTest(token, language) {
    window.location.href = `/guest/interro-question/10/0/0?token=${token}&language=${language.toLowerCase()}`;
}


function showTranslation(numWords, count, score, token, language) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    console.log("numWords:", numWords)
    console.log("count:", count)
    console.log("score:", score)
    if (!isNaN(numWords)) {
        window.location.href = `/guest/interro-answer/${numWords}/${count}/${score}?token=${token}&language=${language.toLowerCase()}`;
    } else {
        console.error("Invalid numWords:", numWords);
    }
}


function sendUserAnswer(answer, numWords, count, score, content_box1, content_box2, token, language) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
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
            nextGuess(numWords, count, score, token, language.toLowerCase());
        } else {
            endInterro(numWords, count, score, token, language.toLowerCase());
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(numWords, count, score, token, language) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    window.location.href = `/guest/interro-question/${numWords}/${count}/${score}?token=${token}&language=${language.toLowerCase()}`;
}


function endInterro(numWords, count, score, token, language) {
    numWords = parseInt(numWords, 10);
    count = parseInt(count, 10);
    score = parseInt(score, 10);
    if (score === numWords) {
        window.location.href = `/guest/interro-end/${numWords}/${score}?token=${token}`;
    } else {
        window.location.href = `/guest/propose-rattraps/${numWords}/${count}/${score}?token=${token}&language=${language.toLowerCase()}`;
    }
}
