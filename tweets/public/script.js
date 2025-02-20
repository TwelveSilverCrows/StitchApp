document.getElementById('generateTweet').addEventListener('click', async () => {
    const userInput = document.getElementById('userInput').value;
    const output = document.getElementById('output');

    if (!userInput) {
        output.textContent = 'Please enter a prompt.';
        return;
    }

    output.textContent = 'Generating tweet...';

    try {
        const response = await fetch('/generate-tweet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: userInput }),
        });

        const data = await response.json();

        if (response.ok) {
            output.textContent = 'Transfer confirmed!';

    
        } else {
            output.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        output.textContent = 'An error occurred. Please try again.';
        console.error(error);
    }
});