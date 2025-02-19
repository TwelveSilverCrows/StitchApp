import requests
import asyncio
import openai

APTOS_NODE_URL = "https://fullnode.testnet.aptoslabs.com"
openai.api_key = "YOUR_API_KEY"
def fetch_all_transactions(start_version=None, limit=100):
    """
    Fetch all transactions from the blockchain (paginated).
    """
    url = f"{APTOS_NODE_URL}/transactions"
    params = {"start_version": start_version, "limit": limit}
    response=None
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
'''def analyze_trends_with_openai(trends):
    """
    Use OpenAI to analyze blockchain trends and generate insights.
    """
    prompt = (
        "The following trends were detected on the Aptos blockchain. "
        "Provide insights on potential whale movements, token accumulation, or other anomalies:\n"
        f"{trends}"
    )
    return prompt'''


def comp(trends, MaxToken=50, outputs=1):
    response= openai.Completion.create(
        model="text-davinci-003",
        prompt=(
        "The following trends were detected on the Aptos blockchain. "
        "Provide insights on potential whale movements, token accumulation, or other anomalies:\n"
        f"{trends}"),
        max_tokens=MaxToken,
        n=outputs
    )
    output=list()
    for k in response['choices']:
        output.append(k['text'].strip())
    return output


def visualize_trends(trends):
    """
    Visualize trends (e.g., print or plot).
    """
    print("Detected Trends:")
    for trend in trends:
        print(f"Address: {trend['address']}, Net Inflow: {trend['net_inflow']}")

def generate_report(insights):
    """
    Generate a report based on OpenAI insights.
    """
    print("Insights for you:")
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
        start_version = transactions[-1]["version"] + 1

    # Preprocess and aggregate transactions
    processed_transactions = preprocess_all_transactions(all_transactions)
    aggregated_transactions = aggregate_transactions(processed_transactions)

    # Detect trends and anomalies
    whale_movements = detect_whale_movements(aggregated_transactions)
    token_accumulation = detect_token_accumulation(aggregated_transactions)

    # Analyze trends with OpenAI
    insights = comp(trends)

    # Visualize and report
    visualize_trends(token_accumulation)
    generate_report(insights)

if __name__ == "__main__":
    asyncio.run(main())