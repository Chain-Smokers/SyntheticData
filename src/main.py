import os
import shutil

from dotenv import load_dotenv
from CommonUtils import CommonUtils
from DSUtils import DSUtils

from ElectoralContract import ElectoralContract
from Web3Utils import Web3Utils


load_dotenv()


if __name__ == "__main__":
    directory = f"N{int(os.environ['PORT_END']) - int(os.environ['PORT_BEGIN'])}V{os.environ['NUMBER_OF_VOTERS']}"
    if not os.path.exists(directory):
        os.mkdir(directory)
    pass
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
    CommonUtils.consoleLog(
        f"Execution time : {CommonUtils.getExecutionTime()}",
        f"{directory}/{os.environ['CONSOLEFILE']}",
    )

    # Get results and create DataFrame
    result = ElectoralContract.getResult()
    votersDetailed = ElectoralContract.getVotersDetailed()
    nodeAddresses = ElectoralContract.getNodeAddresses()
    df = DSUtils.createDatasetForVoterData(votersDetailed, nodeAddresses)
    df.to_csv(f"{directory}/data.csv")

    # Plot graphs from results
    DSUtils.nodewiseVotingGraph(df).savefig(f"{directory}/nodewiseVotingGraph.png")
    DSUtils.percentageVotingGraph(df).savefig(f"{directory}/percentageVotingGraph.png")
    DSUtils.timewiseVotingGraph(df).savefig(f"{directory}/timewiseVotingGraph.png")

    CommonUtils.dumpLogs(f"{directory}/{os.environ['LOGFILE']}")
