from aptos_sdk.account import Account
from aptos_sdk.client import FaucetClient, RestClient
from aptos_sdk.transactions import ScriptArgument, Script, TransactionPayload
from aptos_sdk.bcs import Serializer

# Aptos testnet configurations
NODE_URL = "https://fullnode.testnet.aptoslabs.com/v1"
FAUCET_URL = "https://faucet.testnet.aptoslabs.com"

# Initialize clients
rest_client = RestClient(NODE_URL)
faucet_client = FaucetClient(FAUCET_URL, rest_client)

def create_and_fund_wallet():
    """Create a new wallet and fund it using the faucet."""
    # Create a new wallet
    wallet = Account.generate()
    #"Created wallet with address

    # Fund the wallet with the faucet
    faucet_client.fund_account(wallet.address(), 100_000_000)  # 100 APT
    #Funded wallet with 100 APT

    return wallet

def transfer_apt(sender, receiver, amount):
    """Transfer APT tokens from sender to receiver."""
    # Create a transfer payload
    payload = {
        "type": "entry_function_payload",
        "function": "0x1::coin::transfer",
        "type_arguments": ["0x1::aptos_coin::AptosCoin"],
        "arguments": [receiver.address(), amount],
    }

    # Submit the transaction
    txn_hash = rest_client.submit_transaction(sender, payload)
    rest_client.wait_for_transaction(txn_hash)

    print(f"Transferred {amount} APT from {sender.address()} to {receiver.address()}")

def main():
    # Step 1: Create and fund two wallets
    print("Creating and funding wallets...")
    wallet1 = create_and_fund_wallet()
    wallet2 = create_and_fund_wallet()

    # Step 2: Transfer APT from wallet1 to wallet2
    print("Initiating transfer...")
    transfer_apt(wallet1, wallet2, 50_000_000)  # Transfer 50 APT

    print("Script execution completed.")

if __name__ == "__main__":
    main()