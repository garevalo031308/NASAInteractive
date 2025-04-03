document.addEventListener('DOMContentLoaded', () => {
    // Select all buttons
    const buttons = document.querySelectorAll('button');

    // Create a waiting screen element
    const waitingScreen = document.createElement('div');
    waitingScreen.id = 'waiting-screen';
    waitingScreen.style.position = 'fixed';
    waitingScreen.style.top = '0';
    waitingScreen.style.left = '0';
    waitingScreen.style.width = '100%';
    waitingScreen.style.height = '100%';
    waitingScreen.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    waitingScreen.style.color = 'white';
    waitingScreen.style.display = 'flex';
    waitingScreen.style.justifyContent = 'center';
    waitingScreen.style.alignItems = 'center';
    waitingScreen.style.fontSize = '2em';
    waitingScreen.innerText = 'Waiting for the other player to guess...';
    waitingScreen.style.display = 'none'; // Initially hidden
    document.body.appendChild(waitingScreen);

    // Create a countdown timer element
    const countdownTimer = document.createElement('div');
    countdownTimer.id = 'countdown-timer';
    countdownTimer.style.position = 'fixed';
    countdownTimer.style.top = '10px';
    countdownTimer.style.right = '10px';
    countdownTimer.style.fontSize = '2em';
    countdownTimer.style.color = 'black';
    document.body.appendChild(countdownTimer);

    let userGuess = null;

    // Add click event listener to each button
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Store the user's guess
            userGuess = button.innerText;

            // Show the waiting screen
            waitingScreen.style.display = 'flex';

            // Here you would typically send the user's guess to the server
            // and wait for the response indicating the other player's guess
        });
    });
});