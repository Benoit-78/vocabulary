export { interroGuest, signUp, aboutTheApp, help };


function interroGuest(token) {
    window.location.href = `/guest/interro-settings?token=${token}`;
}


function signUp(token) {
    window.location.href = `/sign-up?token=${token}`;
}


function aboutTheApp(token) {
    window.location.href = `/about-the-app?token=${token}`;
}


function help(token) {
    window.location.href = `/help?token=${token}`;
}
