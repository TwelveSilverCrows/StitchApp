require('dotenv').config();
const express = require('express');
const axios = require('axios');
const { TwitterApi } = require('twitter-api-v2');

const app = express();
app.use(express.json());

// OpenAI API configuration
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions';

// Twitter API configuration
const twitterClient = new TwitterApi({
    appKey: process.env.TWITTER_API_KEY,
    appSecret: process.env.TWITTER_API_SECRET,
    accessToken: process.env.TWITTER_ACCESS_TOKEN,
    accessSecret: process.env.TWITTER_ACCESS_SECRET
});

// Function to generate a tweet using OpenAI API
async function generateTweet(prompt) {
    const response = await axios.post(
        OPENAI_API_URL,
        {
            model: 'gpt-3.5-turbo', // Use the GPT-3.5 model
            messages: [
                { role: 'system', content: 'You are a helpful assistant that generates tweets.' },
                { role: 'user', content: prompt }
            ],
            max_tokens: 100 // Limit the length of the generated tweet
        },
        {
            headers: {
                'Authorization': `Bearer ${OPENAI_API_KEY}`,
                'Content-Type': 'application/json'
            }
        }
    );
    return response.data.choices[0].message.content;
}

// Function to post a tweet using Twitter API
async function postTweet(tweet) {
    try {
        const { data } = await twitterClient.v2.tweet(tweet);
        return data.id;
    } catch (error) {
        console.error('Error posting tweet:', error);
        throw error;
    }
}

// API endpoint to generate and post a tweet
app.post('/generate-tweet', async (req, res) => {
    const { prompt } = req.body;
    if (!prompt) {
        return res.status(400).json({ success: false, error: 'No prompt provided.' });
    }

    try {
        // Step 1: Generate a tweet using OpenAI API
        const tweet = await generateTweet(prompt);
        console.log('Generated Tweet:', tweet);

        // Step 2: Post the tweet to Twitter
        const tweetId = await postTweet(tweet);
        console.log('Tweet ID:', tweetId);

        res.json({ success: true, tweet });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Serve static files (HTML, CSS, JS)
app.use(express.static('public'));

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});