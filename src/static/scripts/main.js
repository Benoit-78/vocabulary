
function goToRoot() {
    window.location.href = '/';
}


function interroGuest() {
    fetch(`/token`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = `/interro-settings-guest?token=${data.access_token}`;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}