from web3 import Web3
from web3.middleware import geth_poa_middleware
import random
import pandas as pd
import time

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60
VOTE_CAST_PROBABILITY = 0.8
HOST_ADDRESS = "http://localhost"
PORT_BEGIN = 8545
PORT_END = 8550

CONTRACT_ADDRESS = "0xA497eBa83A3b4ecEe1718bEDaCD0b9f2b97625F8"

ABI = [
    {
        "inputs": [
            {
                "internalType": "string[]",
                "name": "_candidateNames",
                                "type": "string[]"
            },
            {
                "internalType": "string[]",
                "name": "_voterNames",
                                "type": "string[]"
            },
            {
                "internalType": "string[]",
                "name": "_password",
                                "type": "string[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "candidateName",
                                "type": "string"
            }
        ],
        "name": "addCandidate",
        "outputs": [],
        "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "voterName",
                                "type": "string"
            },
            {
                "internalType": "string",
                "name": "voterPassword",
                                "type": "string"
            }
        ],
        "name": "addVoter",
        "outputs": [],
        "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "inputs": [],
        "name": "getCandidates",
                "outputs": [
            {
                "internalType": "string[]",
                "name": "",
                "type": "string[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getResult",
                "outputs": [
            {
                "components": [
                    {
                        "internalType": "string",
                        "name": "candidateName",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "voteCount",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct ElectoralContract.Candidate[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getVoters",
                "outputs": [
            {
                "internalType": "string[]",
                "name": "",
                "type": "string[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getVotersDetailed",
                "outputs": [
            {
                "components": [
                    {
                        "internalType": "string",
                        "name": "voterName",
                        "type": "string"
                    },
                    {
                        "internalType": "bool",
                        "name": "hasVoted",
                        "type": "bool"
                    },
                    {
                        "internalType": "bool",
                        "name": "isLoggedIn",
                        "type": "bool"
                    },
                    {
                        "internalType": "string",
                        "name": "voterPassword",
                        "type": "string"
                    },
                    {
                        "internalType": "address",
                        "name": "nodeAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct ElectoralContract.Voter[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "voterId",
                                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_password",
                                "type": "string"
            }
        ],
        "name": "login",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "voterId",
                                "type": "uint256"
            }
        ],
        "name": "logout",
        "outputs": [],
        "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "voterId",
                                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "candidateId",
                                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "timestamp",
                                "type": "uint256"
            }
        ],
        "name": "vote",
        "outputs": [],
        "stateMutability": "nonpayable",
                "type": "function"
    }
]


CANDIDATE_NAME = "Tony Stark"
PASSWORD = "password"


class ElectoralContract:
    web3 = []
    contracts = []

    @staticmethod
    def initContract():
        if (len(ElectoralContract.web3) == 0):
            ElectoralContract.web3 = [Web3(Web3.HTTPProvider(f'{HOST_ADDRESS}:{port}'))
                                      for port in range(PORT_BEGIN, PORT_END)]
            for i in range(len(ElectoralContract.web3)):
                ElectoralContract.web3[i].eth.default_account = ElectoralContract.web3[i].eth.accounts[0]
                ElectoralContract.web3[i].middleware_onion.inject(
                    geth_poa_middleware, layer=0)
        if (len(ElectoralContract.contracts) == 0):
            ElectoralContract.contracts = [ElectoralContract.web3[i].eth.contract(
                address=CONTRACT_ADDRESS, abi=ABI) for i in range(len(ElectoralContract.web3))]

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


class Utils:
    fNames = ["Emory", "Donovan", "Ray", "Floyd", "Scott", "Ruby", "Blanca", "Wes", "Ila", "Norma", "Liza", "Jerrold", "Rosie", "Bennie", "Otto", "Cory", "Rigoberto", "Latisha", "Louisa", "Lamont", "Lonnie", "Barney", "Andres", "Peggy", "Collin", "Billie", "Laurel", "Yesenia", "Dennis", "Agustin", "Marion", "Larry", "Amos", "Keenan", "Pierre", "Thelma", "April", "Diann", "Francis", "Kurt", "Jeff", "Lakeisha", "Darren", "Lesley", "Marcos", "Felipe", "Rodney", "Jolene", "Lynda", "Erica",
              "Rhea", "Chelsea", "Jesse", "Myron", "Beryl", "Raleigh", "Hong", "Dustin", "Rosa", "Marci", "Beatriz", "Chauncey", "Marva", "Omer", "Carey", "Elisha", "Raquel", "Mara", "Hugh", "Toney", "Katina", "Tanner", "Jae", "Chandra", "Lidia", "Cristobal", "Hollie", "Andrea", "Teddy", "Garfield", "Raul", "Jan", "Lynwood", "Rosella", "Omar", "Amado", "Sarah", "Dante", "Francisca", "Buck", "Flossie", "Lacy", "Britney", "Kelvin", "Rosanne", "Lorene", "Jacqueline", "Garland", "Leanna", "Morgan"]
    lNames = ["Miles", "Salinas", "Stout", "Caldwell", "Hodges", "Calhoun", "Hines", "Floyd", "Hart", "Stokes", "Pittman", "Mccann", "Sims", "Crosby", "Christensen", "Joyce", "White", "Downs", "Davidson", "Park", "Hurst", "Sharp", "Hernandez", "Leon", "Turner", "Church", "Mooney", "Bullock", "Vang", "Greer", "Mcguire", "Fisher", "Forbes", "Castaneda", "Perry", "Larson", "Meza", "Little", "Bush", "Cantu", "Howell", "Spencer", "Potter", "Washington", "Barajas", "Erickson", "Macdonald", "Kerr", "Cooke", "Atkinson",
              "Burnett", "Zamora", "Schaefer", "Huber", "Mcintosh", "Leon", "Lawson", "Sheppard", "Herrera", "Schwartz", "Sims", "Floyd", "Nixon", "Poole", "Mcneil", "Andersen", "Shea", "Whitehead", "Simpson", "Curry", "Cooley", "Wilkins", "Schmidt", "Bean", "Bartlett", "Mitchell", "Blankenship", "Richard", "Patton", "Clark", "Knox", "Hartman", "Jones", "Cooke", "Copeland", "Roach", "Hendricks", "Richardson", "Austin", "Barrera", "Watson", "Calhoun", "Murray", "Deleon", "Compton", "Ochoa", "Farrell", "Dawson", "Pham", "Brown"]

    @ staticmethod
    def getRandomName():
        return f'{random.choice(Utils.fNames)} {random.choice(Utils.lNames)}'

    @staticmethod
    def addCandidate():
        if (len(ElectoralContract.getResult()) == 0):
            ElectoralContract.addCandidate(CANDIDATE_NAME)

    @staticmethod
    def addVoters(numberOfVoters):
        for i in range(numberOfVoters):
            ElectoralContract.addVoter(Utils.getRandomName(), PASSWORD)

    @staticmethod
    def castAllVotes():
        voters = ElectoralContract.getVotersDetailed()
        # currentTime = int(time.time())
        currentTime = 1681984800
        for voterIndex in range(len(voters)):
            if (not voters[voterIndex][1] and (random.random() < VOTE_CAST_PROBABILITY)):
                ElectoralContract.login(voterIndex, voters[voterIndex][3])
                ElectoralContract.vote(
                    voterIndex, 0, currentTime + random.randint(0, 5 * MINUTES_IN_HOUR * SECONDS_IN_MINUTE))
            if (voters[voterIndex][2]):
                ElectoralContract.logout(voterIndex)


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d} ({p:.0f}%)'.format(p=pct, v=val)
    return my_autopct


if __name__ == "__main__":
    ElectoralContract.initContract()
    nodeAddresses = ElectoralContract.getNodeAddresses()
    # Utils.addCandidate()
    # Utils.addVoters(50)
    # Utils.castAllVotes()
    result = ElectoralContract.getResult()
    votersDetailed = ElectoralContract.getVotersDetailed()
    dict = {"name": [voter[0] for voter in votersDetailed], "has_cast_vote": [voter[1] for voter in votersDetailed], "is_logged_in": [voter[2] for voter in votersDetailed],
            "password": [voter[3] for voter in votersDetailed], "node_address": [voter[4] for voter in votersDetailed], "timestamp": [voter[5] for voter in votersDetailed]}
    df = pd.DataFrame.from_dict(dict).set_index('name')
    df.to_csv("data.csv")
    df['node_address'].replace(['0x0000000000000000000000000000000000000000']+nodeAddresses, [
                               None]+[f'Norm{i}' for i in range(1, len(nodeAddresses)+1)], inplace=True)

    df['timestamp'].replace(0, np.NaN, inplace=True)

    df['Date/Time'] = pd.to_datetime(df['timestamp'], unit='s')
    df['HourOfDay'] = df['Date/Time'].dt.hour

    fig, ax = plt.subplots()

    df2 = df.groupby(['node_address'])[
        'node_address'].count().reset_index(name='votes')

    patches, texts, autotexts = plt.pie(
        df2['votes'], labels=df2['node_address'], autopct=make_autopct(df2['votes']))
    plt.legend(patches, df2['node_address'], loc="center right",
               title='nodes', bbox_to_anchor=(1.35, 0.5))
    ax.set_title("Node-wise voting")
    plt.savefig("graph1.png")

    fig, ax = plt.subplots()
    df3 = df.groupby(['HourOfDay'])[
        'HourOfDay'].count().reset_index(name='votes')
    df3['HourOfDay'] = [int(x) for x in df3['HourOfDay']]

    ax.hist(df3['HourOfDay'], weights=df3['votes'], bins=range(
        min(df3['HourOfDay']), max(df3['HourOfDay'])+2, 1))
    ax.set_xlabel('Time (Hours)')
    ax.set_ylabel('Votes')
    ax.set_title("Time v/s votes")
    plt.savefig("graph2.png")

    fig, ax = plt.subplots()
    df4 = df.groupby(['has_cast_vote'])[
        'has_cast_vote'].count().reset_index(name='votes')

    patches, texts, autotexts = plt.pie(
        df4['votes'], labels=df4['has_cast_vote'], autopct=make_autopct(df4['votes']))
    plt.legend(patches, df4['has_cast_vote'], loc="center right",
               title='has cast vote?', bbox_to_anchor=(1.35, 0.5))
    ax.set_title("Percentage voting")
    plt.savefig("graph3.png")
