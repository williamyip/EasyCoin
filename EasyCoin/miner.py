import time
import hashlib
import json
import requests
import base64
import flask import Flask, request
import multiprocessing import Process, Pipe
import ecdsa

from miner_config import MINER_ADDRESS, MINER_NODE_URL, PEER_NODES

node = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        """Returns a new Block object. Each block is "chained" to its previous
        by calling its unique hash.
        Args:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (str): Data to be sent.
            previous_hash(str): String representing previous block unique hash.
        Attrib:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (str): Data to be sent.
            previous_hash(str): String representing previous block unique hash.
            hash(str): Current block unique hash.
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        """Creates the unique hash for the block. It uses sha256."""
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

def create_genesis_block():
    """To create each block, it needs the hash of the previous one. First
    block has no previous, so it must be created manually (with index zero
     and arbitrary previous hash)"""
    return Block(0, time.time(), {
        "proof-of-work": 9,
        "transactions": None},
        "0")

# Node's blockchain copy
BLOCKCHAIN = [create_genesis_block()]

""" Stores the transactions that this node has in a list.
If the node you sent the transaction adds a block
it will get accepted, but there is a chance it gets
discarded and your transaction goes back as if it was never
processed"""
NODE_PENDING_TRANSACTIONS = []

def proof_of_work(last_proof, blockchain):
    # Creates a variable that we will use to find our next proof of work
    incrementer = last_proof + 1
    # Keep incrementing the incrementer until it's equal to a number divisible by 7919
    # and the proof of work of the previous block in the chain
    start_time = time.time()
    while not (incrementer % 7919 == 0 and incrementer % last_proof == 0):
        incrementer += 1
        # Check if any node found the solution every 60 seconds
        if int((time.time()-start_time) % 60) == 0:
            # If any other node got the proof, stop searching
            new_blockchain = consensus(blockchain)
            if new_blockchain:
                # (False: another node got proof first, new blockchain)
                return False, new_blockchain
    # Once that number is found, we can return it as a proof of our work
    return incrementer, blockchain

def mine(a, blockchain, node_pending_transactions):
    BLOCKCHAIN = blockchain
    NODE_PENDING_TRANSACTIONS = node_pending_transactions
    while True:
        """Mining is the only way that new coins can be created.
        In order to prevent too many coins to be created, the process
        is slowed down by a proof of work algorithm.
        """
        # Get the last proof of work
        last_block = BLOCKCHAIN[-1]
        last_proof = last_block.data['proof-of-work']
        # Find the proof of work for the current block being mined
        # Note: The program will hang here until a new proof of work is found
        proof = proof_of_work(last_proof, BLOCKCHAIN)
        # If we didn't guess the proof, start mining again
        if not proof[0]:
            # Update blockchain and save it to file
            BLOCKCHAIN = proof[1]
            a.send(BLOCKCHAIN)
            continue

        else:
            # Once we find a valid proof of work, we know we can mine a block so
            # ...we reward the miner by adding a transaction
            # First we load all pending transactions sent to the node server
            NODE_PENDING_TRANSACTIONS = requests.get(url = MINER_NODE_URL + '/txion', params = {'update':MINER_ADDRESS}).content
            NODE_PENDING_TRANSACTIONS = json.loads(NODE_PENDING_TRANSACTIONS)
            # Then we add the mining reward
            NODE_PENDING_TRANSACTIONS.append({
                "from": "network",
                "to": MINER_ADDRESS,
                "amount": 1})
            # Now we can gather the data needed to create the new block
            new_block_data = {
                "proof-of-work": proof[0],
                "transactions": list(NODE_PENDING_TRANSACTIONS)
            }
            new_block_index = last_block.index + 1
            new_block_timestamp = time.time()
            last_block_hash = last_block.hash
            # Empty transaction list
            NODE_PENDING_TRANSACTIONS = []
            # Now create the new block
            mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
            BLOCKCHAIN.append(mined_block)
            # Let the client know this node mined a block
            print(json.dumps({
              "index": new_block_index,
              "timestamp": str(new_block_timestamp),
              "data": new_block_data,
              "hash": last_block_hash
            }, sort_keys=True) + "\n")
            a.send(BLOCKCHAIN)
            requests.get(url = MINER_NODE_URL + '/blocks', params = {'update':MINER_ADDRESS})