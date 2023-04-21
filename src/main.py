import os
from dotenv import load_dotenv
from DSUtils import DSUtils

from ElectoralContract import ElectoralContract
from Web3Utils import Web3Utils

load_dotenv()


if __name__ == "__main__":
    ElectoralContract.initContract()
    Web3Utils.addCandidate()
    Web3Utils.addVoters(int(os.environ["NUMBER_OF_VOTERS"]))
    Web3Utils.castAllVotes()

    result = ElectoralContract.getResult()
    votersDetailed = ElectoralContract.getVotersDetailed()
    nodeAddresses = ElectoralContract.getNodeAddresses()
    df = DSUtils.createDatasetForVoterData(votersDetailed, nodeAddresses)
    df.to_csv("data.csv")

    DSUtils.nodewiseVotingGraph(df).savefig("nodewiseVotingGraph.png")
    DSUtils.percentageVotingGraph(df).savefig("percentageVotingGraph.png")
    DSUtils.timewiseVotingGraph(df).savefig("timewiseVotingGraph.png")
