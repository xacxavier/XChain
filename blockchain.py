# Importing libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

#==================================================================
#                   Blockchain Class
#==================================================================

class Blockchain:

    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, previousHash = '0')

    def createBlock(self, proof, previousHash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previousHash': previousHash}
        self.chain.append(block)
        return block

    def getPreviousBlock(self):
        return self.chain[-1]

    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False
        while checkProof is False:
            hashOperation = hashlib.sha256(str(newProof**3 - previousProof**3).encode()).hexdigest()
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof += 1
        return newProof
    
    def hash(self, block):
        encodedBlock = json.dumps(block, sortKeys = True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['previousHash'] != self.hash(previousBlock):
                return False
            previousProof = previousBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(str(proof**3 - previousProof**3).encode()).hexdigest()
            if hashOperation[:4] != '0000':
                return False
            previousBlock = block
            blockIndex += 1
        return True


#==================================================================
#                   Mining
#==================================================================


# Web app
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()


        # Mining a new block
@app.route('/mineBlock', methods = ['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    block = blockchain.createBlock(proof, previousHash)
    response = {'message': 'Block Mined!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previousHash': block['previousHash']}
    return jsonify(response), 200

# Getting the Blockchain
@app.route('/getChain', methods = ['GET'])
def getChain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Valid Blockchain'}
    else:
        response = {'message': 'Invalid Blockchain.'}
    return jsonify(response), 200

# Running the web app
app.run(host = '0.0.0.0', port = 5000)
