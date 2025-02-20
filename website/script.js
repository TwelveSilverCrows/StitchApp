document.addEventListener("DOMContentLoaded", function () {
    const getStartedBtn = document.getElementById("getStarted");
    if (getStartedBtn) {
        getStartedBtn.addEventListener("click", function () {
            window.location.href = "login.html"; // Redirect to login page
        });
    }
});