let questionsCount = 1;


document.addEventListener("DOMContentLoaded", function () {
    const progressBar = document.getElementById("progress-bar");
    progressBar.style.width = `${progress_percent}%`;
});


function startTest() {
    window.location.href = '/interro_question';
}


function goToRoot() {
    window.location.href = '/';
}


function showTranslation() {
    window.location.href = '/interro_answer';
}


function nextGuess() {
    window.location.href = '/interro_question';
}


// ================================================================
// Yes / No buttons
// ================================================================
document.getElementById("yes-button").addEventListener(
    "click",
    function() {
        sendUserResponse("Yes", document.getElementById("progress-bar").style.width);
    }
);

document.getElementById("no-button").addEventListener(
    "click",
    function() {
        sendUserResponse("No", document.getElementById("progress-bar").style.width);
    }
);

function sendUserResponse(response, progressBar) {
    questionsCount++; // Increment the counter
    if (questionsCount < 5) {
        // Send the response and progress_percent to the server (FastAPI)
        fetch("/user-response", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ response: response, progress_percent: progressBar }),
        })
        .then(response => response.json())
        .then(data => {
            // console.log("Server response:", data);
        })
        .catch(error => {
            console.error("Error sending user response:", error);
        });
    } else {
        // Link to a different function or page after 100 clicks
        window.location.href = "/";
    }
}
