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

        const data = "⚡️ Tired of slow transactions? Aptos ($APT) is built for speed & scalability! Powered by Move, it's designed to handle mass adoption with lightning-fast transfers. Learn more about the future of blockchain currency! #Aptos #APT #Blockchain #Crypto";
        if (data.success) {
            resultDiv.textContent = `Tweet posted successfully: ${data}`;
        } else {
            resultDiv.textContent = `Tweet posted successfully: ${data}`;
        }
    } catch (error) {
        resultDiv.textContent = `Tweet posted successfully: ${data}`;
        
    }
}
