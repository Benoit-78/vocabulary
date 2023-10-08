function createWord(english, french) {
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
