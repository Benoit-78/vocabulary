export { goToRoot };


function goToRoot(token) {
    window.location.href = `/?token=${token}`;
}
