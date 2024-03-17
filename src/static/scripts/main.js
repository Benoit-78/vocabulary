
function goToRoot() {
    window.location.href = '/';
}


function interroGuest(token) {
    window.location.href = `/guest/interro-settings?token=${token}`;
}
