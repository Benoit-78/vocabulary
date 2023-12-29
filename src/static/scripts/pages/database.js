

function createWord(userName) {
    var english = document.getElementById("input1").value;
    var french = document.getElementById("input2").value;
    fetch("/create-word", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            english: english,
            french: french
        }),
    })
    .then(answer => answer.json())
    .then(proposeInput(userName))
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function proposeInput(userName) {
    var encodedUserName = encodeURIComponent(userName)
    window.location.href = "/database/" + encodedUserName;
}
