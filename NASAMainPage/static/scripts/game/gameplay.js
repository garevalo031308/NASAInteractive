document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".class-buttons");
    let timer;
    const startTime = Date.now();

    function startTimer(duration, display) {
        let timer = duration, minutes, seconds;
        const countdown = setInterval(function () {
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
        button.addEventListener("click", function() {
            clearInterval(timer);
            const selectedClass = button.innerText;
            redirectToResults(selectedClass);
        });
    });

    const display = document.createElement('div');
    display.id = 'timer';
    document.body.appendChild(display);
    timer = startTimer(30, display);
});