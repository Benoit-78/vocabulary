function createWord() {
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
    .then(proposeInput)
    .catch(error => {
        console.error("Error sending user answer:", error);
    });
}


function proposeInput() {
    window.location.href = '/database';
}