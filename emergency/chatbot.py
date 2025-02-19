import openai
from aptos_sdk.client import RestClient
from aptos_sdk.account import Account
from aptos_sdk.transactions import Script, TransactionArgument

# Initialize OpenAI API
openai.api_key = 'your-openai-api-key'

# Initialize Aptos Client
APTOS_NODE_URL = "https://fullnode.devnet.aptoslabs.com"
client = RestClient(APTOS_NODE_URL)

# Your Aptos account (replace with your own private key and address)
private_key = "your-private-key"
account = Account.load_key(private_key)

def interact_with_aptos(transaction_type, *args):
    """
    Interact with the Aptos blockchain based on the transaction type.
    """
    if transaction_type == "transfer":
        recipient, amount = args
        payload = {
            "type": "entry_function_payload",
            "function": "0x1::coin::transfer",
            "type_arguments": ["0x1::aptos_coin::AptosCoin"],
            "arguments": [recipient, amount],
        }
        txn_hash = client.submit_transaction(account, payload)
        return f"Transaction submitted with hash: {txn_hash}"
    elif transaction_type == "balance":
        address = args[0]
        balance = client.account_balance(address)
        return f"Balance for address {address}: {balance} APT"
    else:
        return "Unsupported transaction type."

def chat_with_openai(prompt):
    """
    Send a prompt to OpenAI and get a response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def parse_chat_response(response):
    """
    Parse the OpenAI response to determine the action.
    """
    if "transfer" in response.lower():
        # Extract recipient and amount from the response
        parts = response.split()
        recipient = parts[parts.index("to") + 1]
        amount = int(parts[parts.index("amount") + 1])
        return interact_with_aptos("transfer", recipient, amount)
    elif "balance" in response.lower():
        # Extract address from the response
        parts = response.split()
        address = parts[parts.index("balance") + 1]
        return interact_with_aptos("balance", address)
    else:
        return "I don't understand. Please specify a valid action (e.g., 'transfer 10 APT to 0x123...' or 'check balance for 0x123...')."

def main():
    print("Welcome to the Aptos OpenAI Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Get response from OpenAI
        openai_response = chat_with_openai(user_input)
        print(f"AI: {openai_response}")

        # Parse the response and interact with Aptos
        aptos_response = parse_chat_response(openai_response)
        print(f"Aptos: {aptos_response}")

if __name__ == "__main__":
    main()

import requests

APTOS_NODE_URL = "https://fullnode.testnet.aptoslabs.com"

def fetch_transactions(address):
    """
    Fetch transactions for a given address.
    """
    url = f"{APTOS_NODE_URL}/accounts/{address}/transactions"
    response = requests.get(url)
    return response.json()

def fetch_account_balance(address):
    """
    Fetch the balance of a given address.
    """
    url = f"{APTOS_NODE_URL}/accounts/{address}/resource/0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
    response = requests.get(url)
    return int(response.json()["data"]["coin"]["value"])