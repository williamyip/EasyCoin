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
