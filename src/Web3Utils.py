import os
import random
from CommonUtils import CommonUtils

from ElectoralContract import ElectoralContract

MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60


class Web3Utils:
    @staticmethod
    def addCandidate():
        if len(ElectoralContract.getResult()) == 0:
            txReceipt = ElectoralContract.addCandidate(os.environ["CANDIDATE_NAME"])
            print(f"Candidate added : {os.environ['CANDIDATE_NAME']}")
            CommonUtils.addLog(
                {
                    "operation": "Web3Utils.addCandidate",
                    "candidateName": os.environ["CANDIDATE_NAME"],
                    "txReceipt": txReceipt.__dict__,
                }
            )

    @staticmethod
    def addVoters(numberOfVoters):
        for voterIndex in range(numberOfVoters):
            txReceipt = ElectoralContract.addVoter(
                CommonUtils.getRandomName(), os.environ["PASSWORD"]
            )
            print(f"Voter added : {voterIndex}")
            CommonUtils.addLog(
                {
                    "operation": "Web3Utils.addVoters",
                    "voterIndex": voterIndex,
                    "txReceipt": txReceipt.__dict__,
                }
            )

    @staticmethod
    def loginAllVoters():
        voters = ElectoralContract.getVotersDetailed()
        for voterIndex in range(len(voters)):
            if (
                not voters[voterIndex][1]  # Check if previously voted
                and not voters[voterIndex][2]  # Check if looged in
            ):
                txReceipt = ElectoralContract.login(voterIndex, voters[voterIndex][3])
                print(f"Voter logged in : {voterIndex}")
                CommonUtils.addLog(
                    {
                        "operation": "Web3Utils.loginAllVoters",
                        "voterIndex": voterIndex,
                        "txReceipt": txReceipt.__dict__,
                    }
                )

    @staticmethod
    def castAllVotes():
        voters = ElectoralContract.getVotersDetailed()
        voteTimestamp = int(os.environ["VOTING_START_TIME"]) + random.randint(
            0,
            int(os.environ["VOTING_WINDOW_IN_HOURS"])
            * MINUTES_IN_HOUR
            * SECONDS_IN_MINUTE,
        )
        for voterIndex in range(len(voters)):
            if (
                not voters[voterIndex][1]  # Check if previously voted
                and voters[voterIndex][2]  # Check if looged in
                and (random.random() < float(os.environ["VOTE_CAST_PROBABILITY"]))
            ):
                txReceipt = ElectoralContract.vote(voterIndex, 0, voteTimestamp)
                print(f"Vote cast : {voterIndex}")
                CommonUtils.addLog(
                    {
                        "operation": "Web3Utils.castAllVotes.vote",
                        "voterIndex": voterIndex,
                        "txReceipt": txReceipt.__dict__,
                    }
                )

    @staticmethod
    def logoutAllVoters():
        voters = ElectoralContract.getVotersDetailed()
        for voterIndex in range(len(voters)):
            if voters[voterIndex][2]:  # Check if logged in
                txReceipt = ElectoralContract.logout(voterIndex)
                print(f"Voter logged out : {voterIndex}")
                CommonUtils.addLog(
                    {
                        "operation": "Web3Utils.logoutAllVoters",
                        "voterIndex": voterIndex,
                        "txReceipt": txReceipt.__dict__,
                    }
                )
