
function goToRoot() {
    window.location.href = '/';
}


function interroGuest(token) {
    window.location.href = `/guest/interro-settings?token=${token}`;
}


function signUp(token) {
    window.location.href = `/sign-up?token=${token}`;
}