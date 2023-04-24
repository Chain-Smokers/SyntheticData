import os
import random
from CommonUtils import CommonUtils

from ElectoralContract import ElectoralContract

MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60


class Web3Utils:
    @staticmethod
    def addCandidate():
        if (len(ElectoralContract.getResult()) == 0):
            txReceipt = ElectoralContract.addCandidate(
                os.environ["CANDIDATE_NAME"])
            CommonUtils.addLog({
                "operation": "Web3Utils.addCandidate",
                "candidateName": os.environ["CANDIDATE_NAME"],
                "txReceipt": txReceipt.__dict__
            })

    @staticmethod
    def addVoters(numberOfVoters):
        for voterIndex in range(numberOfVoters):
            txReceipt = ElectoralContract.addVoter(
                CommonUtils.getRandomName(), os.environ["PASSWORD"])
            CommonUtils.addLog({
                "operation": "Web3Utils.addVoters",
                "voterIndex": voterIndex,
                "txReceipt": txReceipt.__dict__
            })

    @staticmethod
    def castAllVotes():
        voters = ElectoralContract.getVotersDetailed()
        for voterIndex in range(len(voters)):
            try:
                if (voters[voterIndex][2]):
                    txReceipt = ElectoralContract.logout(voterIndex)
                    CommonUtils.addLog({
                        "operation": "Web3Utils.castAllVotes.logout",
                        "voterIndex": voterIndex,
                        "txReceipt": txReceipt.__dict__
                    })
                if (not voters[voterIndex][1] and (random.random() < float(os.environ["VOTE_CAST_PROBABILITY"]))):
                    txReceipt = ElectoralContract.login(
                        voterIndex, voters[voterIndex][3])
                    CommonUtils.addLog({
                        "operation": "Web3Utils.castAllVotes.login",
                        "voterIndex": voterIndex,
                        "txReceipt": txReceipt.__dict__
                    })
                    txReceipt = ElectoralContract.vote(
                        voterIndex, 0, int(os.environ["VOTING_START_TIME"]) + random.randint(0, int(os.environ["VOTING_WINDOW_IN_HOURS"]) * MINUTES_IN_HOUR * SECONDS_IN_MINUTE))
                    CommonUtils.addLog({
                        "operation": "Web3Utils.castAllVotes.vote",
                        "voterIndex": voterIndex,
                        "txReceipt": txReceipt.__dict__
                    })
            except:
                print(f"Log : Error in voterId {voterIndex}")
