# EasyCoin
My attempt at a cryptocurrency implementation in less than 2000 lines of code

### Motivation
Cryptocurrencies and smart-contracts aren't the most trivial concepts to understand. Terms such as wallets, addresses, block proof-of-work, transactions and signatures make more senese when they are in a broad context. This project is my humble attempt at implementing a concise and simple implementation of cryptocurrency.

### What is a Cryptocurrency?
[According to Wikipedia,](https://en.wikipedia.org/wiki/Cryptocurrency) A cryptocurrency is a binary data designed to work as a medium of exchange wherein individual coin ownership records are stored in a leedger existing in the form of a computerized database using strong cryptography to secure transaction records, to control the creation of additional coins, and to verify the transfer of coin ownership.

### What is a blockchain?
Taking a look at the [Bitcoin Organization wiki website](https://en.bitcoin.it/wiki/Main_Page), a blockchain is a transaction database shared by all nodes participating in a system based on the Bitcoin protocol. A full copy of a currency's blockchain contains every transaction ever executed in the currency. With this information, one can find out how much value belonged to each address at any point in history. More details on [Bitcoin Paper](https://bitcoin.org/bitcoin.pdf)

## Instructions
First, install ```requirements.txt```.

```
pip install -r requirements.txt
```

Then you can either:

- Run ```miner.py``` - to become a node and start mining
- Run ```wallet.py``` - to become a user and send transactions (to send transactions you must run a node, in other words, you must run ```miner.py``` too)

> Important: DO NOT run it in the python IDLE, run it in your console. The ```miner.py``` uses parallel processing that doesn't work in the python IDLE.

## How does this code work?

There are 2 main scripts:

- ```miner.py```
- ```wallet.py```

### Miner.py

This file is probably the most important. Running it will create a node (like a server). From here you can connect to the blockchain and process transactions (that other users send) by mining. As a reward for this work, you recieve some coins. The more nodes exist, the more secure the blockchain gets.

```miner.py``` has 2 processes running in parallel:

1. The first process takes care of mining, updating new blockchains and finding the proof of work.

2. The second process runs the flask server where peer nodes and users can connect to ask for the entire blockchain or submit new transactions.


### Wallet.py

This file is for those who don't want to be nodes but simple users. Running this file allows you to generate a new address, send coins and check your transaction history (keep in mind that if you are running this in a local server, you will need a "miner" to process your transaction).
When creating a wallet address, a new file will be generated with all your security credentials. You are supposed to keep it safe.


## Disclaimer

By no means should this project be used for real purposes, it lacks security and may contain several bugs.
