document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".class-buttons");
    const mainContent = document.getElementById("main-content");
    let gameplayTimer;
    const startTime = Date.now();

    // Hide the main content initially
    mainContent.style.display = "none";

    function startPreGameCountdown(duration, display, callback) {
        let timer = duration, seconds;
        const countdown = setInterval(function() {
            seconds = parseInt(timer % 60, 10);
            display.textContent = "Starting in: " + seconds;

            if (--timer < 0) {
                clearInterval(countdown);
                display.textContent = ""; // Clear the countdown display
                callback(); // Show the main content and start the gameplay timer
            }
        }, 1000);
    }

    function startGameplayTimer(duration, display) {
        display.id = 'gameplay-timer'; // Assign a unique ID for styling
        let timer = duration, minutes, seconds;
        const countdown = setInterval(function() {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                clearInterval(countdown);
                redirectToResults();
            }
        }, 1000);
    return countdown;
}

    function redirectToResults(selectedClass = null) {
        const endTime = Date.now();
        const timeTaken = endTime - startTime;
        const url = new URL('NASAMainPage/game/round_results', window.location.origin);
        url.searchParams.append('selectedClass', selectedClass);
        url.searchParams.append('gameid', gameid);
        url.searchParams.append('timeTaken', timeTaken);
        window.location.href = url.toString();
    }

    buttons.forEach(button => {
        button.disabled = true; // Disable buttons during pre-game countdown
        button.addEventListener("click", function() {
            clearInterval(gameplayTimer);
            const selectedClass = button.innerText;
            redirectToResults(selectedClass);
        });
    });

    const display = document.createElement('div');
    display.id = 'timer';
    document.body.appendChild(display);

    // Start the pre-game countdown
    startPreGameCountdown(5, display, function() {
        // Show the main content and enable buttons after pre-game countdown
        mainContent.style.display = "block";
        buttons.forEach(button => button.disabled = false);
        gameplayTimer = startGameplayTimer(30, display);
    });
});