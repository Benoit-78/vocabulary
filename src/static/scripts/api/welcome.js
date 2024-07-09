export { interroGuest, signIn, signUp, aboutTheApp, help };


function interroGuest(token) {
    window.location.href = `/v1/guest/interro-settings?token=${token}`;
}


function signIn(token) {
    window.location.href = `/v1/sign-in?token=${token}`;
}


function signUp(token) {
    window.location.href = `/v1/sign-up?token=${token}`;
}


function aboutTheApp(token) {
    window.location.href = `/v1/about-the-app?token=${token}`;
}


function help(token) {
    window.location.href = `/v1/help?token=${token}`;
}
