import asyncio
import os

import aptos_sdk.transactions
import dotenv
from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.async_client import RestClient, FaucetClient
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import TransactionArgument, TransactionPayload

# this will load the environment variables from the .env file
dotenv.load_dotenv(".env")


async def main():
    # `3. Create aptos instance and set it to testnet`

    # create a client to interact with the Aptos blockchain
    aptos_client = RestClient(
        "https://api.testnet.aptoslabs.com/v1"
    )

    # `4. Wallet Account`
    # load the private key from the environment variable
    # Please dont hard code your private key in any way (dev/prod)
    # use a .env :)
    account = Account.load_key(
        os.getenv("APTOS_PRIVATE_KEY")
    )

    # Get the account address
    account_address = account.address()
    print(f"Account address: {account_address}")

    # `5. Check balance`
    account_balance = await aptos_client.account_balance(account_address)

    # print the balance
    print(f"Account balance: {account_balance} APT")

    # `6. Build the transaction`
    tba_tx = aptos_sdk.transactions.EntryFunction.natural(
        "0x777b93e13ff2a1bc872eb4d099ae15a52fb70f2f01dd18d7c809e217fb0e543e::tba_exam",
        "add_participant",
        [],
        [
            TransactionArgument(
                AccountAddress.from_str("0x539f880b3da2bc33d98b5efbf611eb76b6a980b0fdb15badb537767e0767d6e3"),
                Serializer.struct),
            TransactionArgument("Tabby", Serializer.str),
            TransactionArgument("t3bby", Serializer.str),
            TransactionArgument("iamtabbynoodles@gmail.com", Serializer.str),
            TransactionArgument("realtabby", Serializer.str),
        ]
    )

    # `7. Sign the transaction`
    signed_tx = await aptos_client.create_bcs_signed_transaction(
        account,
        TransactionPayload(tba_tx)
    )

    # `8. Send the transaction to APTOS BLOCKCHAINNNN`
    print("Waiting for transaction to propagate...")
    tx_id = await aptos_client.submit_and_wait_for_bcs_transaction(
        signed_tx
    )

    # `9. Wait for the transaction to propagate`
    print(f"Transaction ID: {tx_id}")
    print("Transaction propagated successfully!")


if __name__ == "__main__":
    # check if the .env file exists
    if not os.path.exists(".env"):
        print("Please create a .env file with the required environment variables.")
        exit(1)

    # check if the required environment variables are set
    if not os.getenv("APTOS_PRIVATE_KEY"):
        print("Please set the APTOS_PRIVATE_KEY environment variable in the .env file.")
        exit(1)

    # run the main function
    asyncio.run(main())
