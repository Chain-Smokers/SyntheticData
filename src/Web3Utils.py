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
            CommonUtils.consoleLog(
                f"Candidate added : {os.environ['CANDIDATE_NAME']}",
                f"N{int(os.environ['PORT_END']) - int(os.environ['PORT_BEGIN'])}V{os.environ['NUMBER_OF_VOTERS']}/{os.environ['CONSOLEFILE']}",
            )
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
            CommonUtils.consoleLog(
                f"Voter added : {voterIndex}",
                f"N{int(os.environ['PORT_END']) - int(os.environ['PORT_BEGIN'])}V{os.environ['NUMBER_OF_VOTERS']}/{os.environ['CONSOLEFILE']}",
            )
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
                and not voters[voterIndex][2]  # Check if logged in
            ):
                txReceipt = ElectoralContract.login(voterIndex, voters[voterIndex][3])
                CommonUtils.consoleLog(
                    f"Voter logged in : {voterIndex}",
                    f"N{int(os.environ['PORT_END']) - int(os.environ['PORT_BEGIN'])}V{os.environ['NUMBER_OF_VOTERS']}/{os.environ['CONSOLEFILE']}",
                )
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
        for voterIndex in range(len(voters)):
            if (
                not voters[voterIndex][1]  # Check if previously voted
                and voters[voterIndex][2]  # Check if logged in
                and (random.random() < float(os.environ["VOTE_CAST_PROBABILITY"]))
            ):
                voteTimestamp = int(os.environ["VOTING_START_TIME"]) + random.randint(
                    0,
                    int(os.environ["VOTING_WINDOW_IN_HOURS"])
                    * MINUTES_IN_HOUR
                    * SECONDS_IN_MINUTE,
                )
                txReceipt = ElectoralContract.vote(voterIndex, 0, voteTimestamp)
                CommonUtils.consoleLog(
                    f"Vote cast : {voterIndex}",
                    f"N{int(os.environ['PORT_END']) - int(os.environ['PORT_BEGIN'])}V{os.environ['NUMBER_OF_VOTERS']}/{os.environ['CONSOLEFILE']}",
                )
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
                CommonUtils.consoleLog(
                    f"Voter logged out : {voterIndex}",
                    f"N{int(os.environ['PORT_END']) - int(os.environ['PORT_BEGIN'])}V{os.environ['NUMBER_OF_VOTERS']}/{os.environ['CONSOLEFILE']}",
                )
                CommonUtils.addLog(
                    {
                        "operation": "Web3Utils.logoutAllVoters",
                        "voterIndex": voterIndex,
                        "txReceipt": txReceipt.__dict__,
                    }
                )
