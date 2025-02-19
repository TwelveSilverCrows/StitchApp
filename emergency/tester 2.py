import requests
import asyncio
from openai import OpenAI
# Constants
APTOS_NODE_URL = "https://fullnode.testnet.aptoslabs.com"  # Replace with your full node URL
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Replace with the actual DeepSeek API endpoint
DEEPSEEK_API_KEY = "sk-fb5b9e4d18ab4d268c89895e80587111"  # Replace with your DeepSeek API key


client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
def fetch_all_transactions(start_version=None, limit=100):
    """
    Fetch all transactions from the Aptos blockchain using the Full Node API.
    """
    url = f"{APTOS_NODE_URL}/transactions"
    params = {"start_version": start_version, "limit": limit}
    response = None

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)
    except requests.exceptions.RequestException as e:
        print(f"API Request Failed: {e}")
        return []

    try:
        return response.json()  # Parse JSON
    except requests.exceptions.JSONDecodeError:
        print("API did not return valid JSON. Response:", response.text)
        return []

def preprocess_all_transactions(transactions):
    """
    Preprocess all transactions to extract relevant data.
    """
    processed = []
    for tx in transactions:
        if "payload" in tx and "arguments" in tx["payload"]:
            processed.append({
                "sender": tx["sender"],
                "receiver": tx["payload"]["arguments"][0],
                "amount": int(tx["payload"]["arguments"][1]),
                "timestamp": tx["timestamp"],
            })
    return processed

def aggregate_transactions(transactions):
    """
    Aggregate transactions by sender/receiver.
    """
    aggregated = {}
    for tx in transactions:
        sender = tx["sender"]
        receiver = tx["receiver"]
        amount = tx["amount"]

        # Aggregate by sender
        if sender not in aggregated:
            aggregated[sender] = {"sent": 0, "received": 0}
        aggregated[sender]["sent"] += amount

        # Aggregate by receiver
        if receiver not in aggregated:
            aggregated[receiver] = {"sent": 0, "received": 0}
        aggregated[receiver]["received"] += amount

    return aggregated

def detect_whale_movements(aggregated, threshold=1000000000):  # Threshold: 1000 APT
    """
    Detect whale movements (large token transfers).
    """
    whales = []
    for address, data in aggregated.items():
        if data["sent"] > threshold or data["received"] > threshold:
            whales.append({
                "address": address,
                "sent": data["sent"],
                "received": data["received"],
            })
    return whales

def detect_token_accumulation(aggregated, threshold=1000000000):  # Threshold: 1000 APT
    """
    Detect token accumulation (large net inflows).
    """
    accumulators = []
    for address, data in aggregated.items():
        net_inflow = data["received"] - data["sent"]
        if net_inflow > threshold:
            accumulators.append({
                "address": address,
                "net_inflow": net_inflow,
            })
    return accumulators

def analyze_trends_with_deepseek(trends):
    """
    Use DeepSeek API to analyze blockchain trends and generate insights.
    """
    prompt = (
        "The following trends were detected on the Aptos blockchain. "
        "Provide insights on potential whale movements, token accumulation, or other anomalies:\n"
        f"{trends}"
    )

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat",  # Replace with the correct DeepSeek model name
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"DeepSeek API Request Failed: {e}")
        return "Failed to generate insights."

def visualize_trends(trends):
    """
    Visualize trends (e.g., print or plot).
    """
    print("Detected Trends:")
    for trend in trends:
        print(f"Address: {trend['address']}, Net Inflow: {trend['net_inflow']} APT")

def generate_report(insights):
    """
    Generate a report based on DeepSeek insights.
    """
    print("DeepSeek Insights:")
    print(insights)

async def main():
    # Fetch all transactions (paginated)
    all_transactions = []
    start_version = None
    while True:
        transactions = fetch_all_transactions(start_version=start_version, limit=100)
        if not transactions:
            break
        all_transactions.extend(transactions)
        start_version = transactions[-1]["version"] + 1  # Use the last transaction's version for pagination

    # Preprocess and aggregate transactions
    processed_transactions = preprocess_all_trans