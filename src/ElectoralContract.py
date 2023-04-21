import os
import random
import json

from web3 import Web3
from web3.middleware import geth_poa_middleware


class ElectoralContract:
    web3 = []
    contracts = []

    @staticmethod
    def initContract():
        jsonFile = open('src/ElectoralContract.json')
        abiJson = json.load(jsonFile)
        if (len(ElectoralContract.web3) == 0):
            ElectoralContract.web3 = [Web3(Web3.HTTPProvider(f'{os.environ["HOST_ADDRESS"]}:{port}'))
                                      for port in range(int(os.environ["PORT_BEGIN"]), int(os.environ["PORT_END"]))]
            for i in range(len(ElectoralContract.web3)):
                ElectoralContract.web3[i].eth.default_account = ElectoralContract.web3[i].eth.accounts[0]
                ElectoralContract.web3[i].middleware_onion.inject(
                    geth_poa_middleware, layer=0)
        if (len(ElectoralContract.contracts) == 0):
            ElectoralContract.contracts = [ElectoralContract.web3[i].eth.contract(
                address=os.environ["CONTRACT_ADDRESS"], abi=abiJson['abi']) for i in range(len(ElectoralContract.web3))]

    @staticmethod
    def getNodeAddresses():
        return [ElectoralContract.web3[i].eth.default_account for i in range(len(ElectoralContract.web3))]

    @staticmethod
    def addCandidate(candidateName):
        nodeIndex = random.randint(0, len(ElectoralContract.contracts)-1)
        tx_hash = ElectoralContract.contracts[nodeIndex].functions.addCandidate(
            candidateName).transact()
        ElectoralContract.web3[nodeIndex].eth.wait_for_transaction_receipt(
            tx_hash)

    @staticmethod
    def addVoter(voterName, voterPassword):
        nodeIndex = random.randint(0, len(ElectoralContract.contracts)-1)
        tx_hash = ElectoralContract.contracts[nodeIndex].functions.addVoter(
            voterName, voterPassword).transact()
        ElectoralContract.web3[nodeIndex].eth.wait_for_transaction_receipt(
            tx_hash)

    @staticmethod
    def login(voterId, password):
        nodeIndex = random.randint(0, len(ElectoralContract.contracts)-1)
        tx_hash = ElectoralContract.contracts[nodeIndex].functions.login(
            voterId, password).transact()
        ElectoralContract.web3[nodeIndex].eth.wait_for_transaction_receipt(
            tx_hash)

    @staticmethod
    def logout(voterId):
        nodeIndex = random.randint(0, len(ElectoralContract.contracts)-1)
        tx_hash = ElectoralContract.contracts[nodeIndex].functions.logout(
            voterId).transact()
        ElectoralContract.web3[nodeIndex].eth.wait_for_transaction_receipt(
            tx_hash)

    @staticmethod
    def getResult():
        nodeIndex = random.randint(0, len(ElectoralContract.contracts)-1)
        return ElectoralContract.contracts[nodeIndex].functions.getResult().call()

    @staticmethod
    def getVotersDetailed():
        nodeIndex = random.randint(0, len(ElectoralContract.contracts)-1)
        return ElectoralContract.contracts[nodeIndex].functions.getVotersDetailed().call()

    @staticmethod
    def vote(voterId, candidateId, timestamp):
        nodeIndex = random.randint(0, len(ElectoralContract.contracts)-1)
        tx_hash = ElectoralContract.contracts[nodeIndex].functions.vote(
            voterId, candidateId, timestamp).transact()
        ElectoralContract.web3[nodeIndex].eth.wait_for_transaction_receipt(
            tx_hash)
