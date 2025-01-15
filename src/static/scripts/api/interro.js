export { sendUserSettings, showTranslation, sendUserAnswer, launchRattrap };


function sendUserSettings(token, inputParams) {
    // console.log("InputParams:", inputParams);
    fetch(
        `/v1/interro/save-interro-settings?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(inputParams)
        }
    )
    .then(response => response.json())
    .then(data => {
        // console.log("data.message: ", data.message)
        if (data && data.message === "Settings saved successfully") {
            // console.log("Params:", data)
            startTest(token, data)
        } else if (data && data.message === "Empty table") {
            window.location.href = `/v1/interro/interro-settings?token=${token}&errorMessage=${data.message}`;
        } else {
            console.error("Unknown message at interro creation, data:", data);
        }
    })
    .catch(error => {
        console.error("Error with the interro creation:", error);
    });
}


function startTest(token, inputParams) {
    // console.log("InputParams:", inputParams);
    if (!isNaN(inputParams.testLength)) {
        const urlParams = new URLSearchParams(inputParams);
        urlParams.append("token", token);
        urlParams.append("testCount", 0);
        urlParams.append("testScore", 0);
        window.location.href = `/v1/interro/interro-question?${urlParams.toString()}`;
    } else {
        console.error("Error: testLength is not a number:", inputParams.testLength);
    }
}


function showTranslation(token, inputParams) {
    // console.log("InputParams:", inputParams);
    if (!isNaN(inputParams.testLength)) {
        const urlParams = new URLSearchParams(inputParams);
        urlParams.append("token", token);
        window.location.href = `/v1/interro/interro-answer?${urlParams.toString()}`;
    } else {
        console.error("Invalid testLength:", inputParams.testLength);
    }
}


function sendUserAnswer(token, inputParams) {
    // console.log("InputParams:", inputParams);
    fetch(
        `/v1/interro/user-answer?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(inputParams),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "User response stored successfully") {
            if (data.testCount < data.testLength) {
                nextGuess(token, data);
            } else {
                endInterro(token, data);
            }
        } else {
            console.error("Error with user answer acquisition");
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    });
}


function nextGuess(token, inputParams) {
    // console.log("InputParams:", inputParams);
    const urlParams = new URLSearchParams(inputParams);
    urlParams.append("token", token);
    window.location.href = `/v1/interro/interro-question?${urlParams.toString()}`;
}


function endInterro(token, inputParams) {
    // console.log("InputParams:", inputParams);
    if (inputParams.testScore === inputParams.testLength) {
        const urlParams = new URLSearchParams(inputParams);
        urlParams.append("token", token);
        window.location.href = `/v1/interro/interro-end?${urlParams.toString()}`;
    } else {
        const urlParams = new URLSearchParams(inputParams);
        urlParams.append("token", token);
        window.location.href = `/v1/interro/propose-rattrap?${urlParams.toString()}`;
    }
}


function launchRattrap(token, inputParams) {
    // console.log("InputParams:", inputParams);
    fetch(
        `/v1/interro/launch-rattrap?token=${token}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(inputParams),
        }
    )
    .then(answer => answer.json())
    .then(data => {
        if (data && data.message === "Rattrap created successfully") {
            const urlParams = new URLSearchParams(data);
            urlParams.append("token", token);
            urlParams.append("testPerf", 0);
            window.location.href = `/v1/interro/interro-question?${urlParams.toString()}`;
        } else {
            console.error("Error with rattrap creation.");
        }
    })
    .catch(error => {
        console.error("Error sending user response:", error);
    })
}

