async function generateAndPostTweet() {
    const tweetInput = document.getElementById('tweetInput').value;
    if (!tweetInput) {
        alert('Please enter some text.');
        return;
    }

    const resultDiv = document.getElementById('result');
    resultDiv.textContent = 'Generating and posting tweet...';

    try {
        const response = await fetch('/generate-tweet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: tweetInput })
        });

        const data = await response.json();
        if (data.success) {
            resultDiv.textContent = `Tweet posted successfully: ${data.tweet}`;
        } else {
            resultDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        resultDiv.textContent = 'An error occurred. Please try again.';
        console.error('Error:', error);
    }
}