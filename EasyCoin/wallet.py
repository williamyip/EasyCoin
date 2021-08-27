""" This is going to be your wallet. You can do several cool things:
- Generate a new address (public & private key). You are going to use this address (public key) to send and/or receive any transactions. You can have as many addresses as you wish,
but keep in mind that if you lose its credential data, you will not be able to retrieve it :( 
- Send coins to another address
- Retrieve the entire blockchain and check your balance

If this iss your first time using this script, dont forget to generate a new address and edit miner config file with it (only if you are going to mine)

Timestamp in hashed message. When you send your transaction it will be received by several nodes. If any node mine a block, your transaction will get adaded to the blockchain but other 
nodes will still have it pending. If any node sees that your transaction with same timestamp was added, they should remove it from the node_pending_transactions list to avoid it get processed more than 1 time
"""

import requests
import time
import base64
import ecdsa


def wallet():
    response = None
    while response not in ["1", "2", "3","4"]:
        response = input("""What do you want to do?
        1. Generate new wallet
        2. Send coins to another wallet
        3. Check transactions
        4. Quit\n""")

    if response == "1"
        # Generate new wallet
        print("""=========================================\n
IMPORTANT: save this credentials or you won't be able to recover your wallet\n
=========================================\n""")
        generate_ECDSA_keys()

    elif response == "2":
        addr_from = input("From: introduce your wallet address (public key)\n")
        private_key = input("Introduce your private key\n")
        addr_to = input("To: introduce destination wallet address\n")
        amount = input("Amount: number stating how much do you want to send\n")
        print("=========================================\n\n")
        print("Is everything correct?\n")
        print(F"From: {addr_from}\nPrivate Key: {private_key}\nTo: {addr_to}\nAmount: {amount}\n")
        response = input("y/n\n")
        if response.lower() == "y":
            send_transaction(addr_from, private_key, addr_to, amount)
        elif response.lower() == "n":
            return wallet()  # return to menu
    elif response == "3":  # Will always occur when response == 3.
        check_transactions()
    else:
        quit()

    
def send_transaction(addr_from, private_key, addr_to, amount):

def check_transactions():

def generate_ECDSA_keys():

def sign_ECDSA_msg(private_key):


if __name__ == '__main__':
    print("""       =========================================\n
        EasyCoin v1.0.0 - BLOCKCHAIN SYSTEM\n
       =========================================\n\n
        You can find more help at: https://github.com/williamyip/EasyCoin.git\n
        Make sure you are using the latest version or you may end in
        a parallel chain.\n\n\n""")
    wallet()
    input("Press ENTER to exit...")

