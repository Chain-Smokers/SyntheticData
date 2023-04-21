import os
import random

from ElectoralContract import ElectoralContract

MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60


class Web3Utils:
    fNames = ["Emory", "Donovan", "Ray", "Floyd", "Scott", "Ruby", "Blanca", "Wes", "Ila", "Norma", "Liza", "Jerrold", "Rosie", "Bennie", "Otto", "Cory", "Rigoberto", "Latisha", "Louisa", "Lamont", "Lonnie", "Barney", "Andres", "Peggy", "Collin", "Billie", "Laurel", "Yesenia", "Dennis", "Agustin", "Marion", "Larry", "Amos", "Keenan", "Pierre", "Thelma", "April", "Diann", "Francis", "Kurt", "Jeff", "Lakeisha", "Darren", "Lesley", "Marcos", "Felipe", "Rodney", "Jolene", "Lynda", "Erica",
              "Rhea", "Chelsea", "Jesse", "Myron", "Beryl", "Raleigh", "Hong", "Dustin", "Rosa", "Marci", "Beatriz", "Chauncey", "Marva", "Omer", "Carey", "Elisha", "Raquel", "Mara", "Hugh", "Toney", "Katina", "Tanner", "Jae", "Chandra", "Lidia", "Cristobal", "Hollie", "Andrea", "Teddy", "Garfield", "Raul", "Jan", "Lynwood", "Rosella", "Omar", "Amado", "Sarah", "Dante", "Francisca", "Buck", "Flossie", "Lacy", "Britney", "Kelvin", "Rosanne", "Lorene", "Jacqueline", "Garland", "Leanna", "Morgan"]
    lNames = ["Miles", "Salinas", "Stout", "Caldwell", "Hodges", "Calhoun", "Hines", "Floyd", "Hart", "Stokes", "Pittman", "Mccann", "Sims", "Crosby", "Christensen", "Joyce", "White", "Downs", "Davidson", "Park", "Hurst", "Sharp", "Hernandez", "Leon", "Turner", "Church", "Mooney", "Bullock", "Vang", "Greer", "Mcguire", "Fisher", "Forbes", "Castaneda", "Perry", "Larson", "Meza", "Little", "Bush", "Cantu", "Howell", "Spencer", "Potter", "Washington", "Barajas", "Erickson", "Macdonald", "Kerr", "Cooke", "Atkinson",
              "Burnett", "Zamora", "Schaefer", "Huber", "Mcintosh", "Leon", "Lawson", "Sheppard", "Herrera", "Schwartz", "Sims", "Floyd", "Nixon", "Poole", "Mcneil", "Andersen", "Shea", "Whitehead", "Simpson", "Curry", "Cooley", "Wilkins", "Schmidt", "Bean", "Bartlett", "Mitchell", "Blankenship", "Richard", "Patton", "Clark", "Knox", "Hartman", "Jones", "Cooke", "Copeland", "Roach", "Hendricks", "Richardson", "Austin", "Barrera", "Watson", "Calhoun", "Murray", "Deleon", "Compton", "Ochoa", "Farrell", "Dawson", "Pham", "Brown"]

    @ staticmethod
    def getRandomName():
        return f'{random.choice(Web3Utils.fNames)} {random.choice(Web3Utils.lNames)}'

    @staticmethod
    def addCandidate():
        if (len(ElectoralContract.getResult()) == 0):
            ElectoralContract.addCandidate(os.environ["CANDIDATE_NAME"])

    @staticmethod
    def addVoters(numberOfVoters):
        for i in range(numberOfVoters):
            ElectoralContract.addVoter(
                Web3Utils.getRandomName(), os.environ["PASSWORD"])

    @staticmethod
    def castAllVotes():
        voters = ElectoralContract.getVotersDetailed()
        currentTime = 1681984800
        for voterIndex in range(len(voters)):
            if (not voters[voterIndex][1] and (random.random() < float(os.environ["VOTE_CAST_PROBABILITY"]))):
                ElectoralContract.login(voterIndex, voters[voterIndex][3])
                ElectoralContract.vote(
                    voterIndex, 0, currentTime + random.randint(0, 5 * MINUTES_IN_HOUR * SECONDS_IN_MINUTE))
            if (voters[voterIndex][2]):
                ElectoralContract.logout(voterIndex)
