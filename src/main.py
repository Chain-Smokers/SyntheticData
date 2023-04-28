import os

from dotenv import load_dotenv
from CommonUtils import CommonUtils
from DSUtils import DSUtils

from ElectoralContract import ElectoralContract
from Web3Utils import Web3Utils


load_dotenv()


if __name__ == "__main__":
    # Initialize contract in program
    ElectoralContract.initContract()

    # Generate synthetic data
    CommonUtils.startTimer()
    Web3Utils.addCandidate()
    Web3Utils.addVoters(int(os.environ["NUMBER_OF_VOTERS"]))
    Web3Utils.loginAllVoters()
    Web3Utils.castAllVotes()
    Web3Utils.logoutAllVoters()
    CommonUtils.stopTimer()
    print(f"Execution time : {CommonUtils.getExecutionTime()}")

    # Get results and create DataFrame
    result = ElectoralContract.getResult()
    votersDetailed = ElectoralContract.getVotersDetailed()
    nodeAddresses = ElectoralContract.getNodeAddresses()
    df = DSUtils.createDatasetForVoterData(votersDetailed, nodeAddresses)
    df.to_csv("data.csv")

    # Plot graphs from results
    DSUtils.nodewiseVotingGraph(df).savefig("nodewiseVotingGraph.png")
    DSUtils.percentageVotingGraph(df).savefig("percentageVotingGraph.png")
    DSUtils.timewiseVotingGraph(df).savefig("timewiseVotingGraph.png")

    CommonUtils.dumpLogs(os.environ["LOGFILE"])
