document.addEventListener("DOMContentLoaded", function() {
    const nextbutton = document.getElementById('NextRound');

    function nextRound() {
        if (round_number === 5) {
            const url = new URL("NASAMainPage/game/game_results", window.location.origin)
            url.searchParams.append('gameid', gameid)
            window.location.href = url.toString()
        } else{
            const url = new URL('NASAMainPage/game/gameplay', window.location.origin);
            url.searchParams.append('gameid', gameid)
            window.location.href = url.toString();
        }
    }

    nextbutton.addEventListener('click', function() {
        nextRound();
    });
})