import random
import time
import json

from hexbytes import HexBytes
from web3 import Web3


class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


class CommonUtils:
    __fNames = ["Emory", "Donovan", "Ray", "Floyd", "Scott", "Ruby", "Blanca", "Wes", "Ila", "Norma", "Liza", "Jerrold", "Rosie", "Bennie", "Otto", "Cory", "Rigoberto", "Latisha", "Louisa", "Lamont", "Lonnie", "Barney", "Andres", "Peggy", "Collin", "Billie", "Laurel", "Yesenia", "Dennis", "Agustin", "Marion", "Larry", "Amos", "Keenan", "Pierre", "Thelma", "April", "Diann", "Francis", "Kurt", "Jeff", "Lakeisha", "Darren", "Lesley", "Marcos", "Felipe", "Rodney", "Jolene", "Lynda", "Erica",
                "Rhea", "Chelsea", "Jesse", "Myron", "Beryl", "Raleigh", "Hong", "Dustin", "Rosa", "Marci", "Beatriz", "Chauncey", "Marva", "Omer", "Carey", "Elisha", "Raquel", "Mara", "Hugh", "Toney", "Katina", "Tanner", "Jae", "Chandra", "Lidia", "Cristobal", "Hollie", "Andrea", "Teddy", "Garfield", "Raul", "Jan", "Lynwood", "Rosella", "Omar", "Amado", "Sarah", "Dante", "Francisca", "Buck", "Flossie", "Lacy", "Britney", "Kelvin", "Rosanne", "Lorene", "Jacqueline", "Garland", "Leanna", "Morgan"]
    __lNames = ["Miles", "Salinas", "Stout", "Caldwell", "Hodges", "Calhoun", "Hines", "Floyd", "Hart", "Stokes", "Pittman", "Mccann", "Sims", "Crosby", "Christensen", "Joyce", "White", "Downs", "Davidson", "Park", "Hurst", "Sharp", "Hernandez", "Leon", "Turner", "Church", "Mooney", "Bullock", "Vang", "Greer", "Mcguire", "Fisher", "Forbes", "Castaneda", "Perry", "Larson", "Meza", "Little", "Bush", "Cantu", "Howell", "Spencer", "Potter", "Washington", "Barajas", "Erickson", "Macdonald", "Kerr", "Cooke", "Atkinson",
                "Burnett", "Zamora", "Schaefer", "Huber", "Mcintosh", "Leon", "Lawson", "Sheppard", "Herrera", "Schwartz", "Sims", "Floyd", "Nixon", "Poole", "Mcneil", "Andersen", "Shea", "Whitehead", "Simpson", "Curry", "Cooley", "Wilkins", "Schmidt", "Bean", "Bartlett", "Mitchell", "Blankenship", "Richard", "Patton", "Clark", "Knox", "Hartman", "Jones", "Cooke", "Copeland", "Roach", "Hendricks", "Richardson", "Austin", "Barrera", "Watson", "Calhoun", "Murray", "Deleon", "Compton", "Ochoa", "Farrell", "Dawson", "Pham", "Brown"]
    __startTime = 0
    __endTime = 0
    __executionTime = 0
    __logsList = []

    @ staticmethod
    def getRandomName():
        return f'{random.choice(CommonUtils.__fNames)} {random.choice(CommonUtils.__lNames)}'

    @staticmethod
    def startTimer():
        CommonUtils.__startTime = time.time()

    @staticmethod
    def stopTimer():
        CommonUtils.__endTime = time.time()
        CommonUtils.__executionTime = CommonUtils.__endTime - CommonUtils.__startTime

    @staticmethod
    def getExecutionTime():
        return CommonUtils.__executionTime

    @staticmethod
    def addLog(log):
        CommonUtils.__logsList.append(log)

    @staticmethod
    def getLogs():
        return CommonUtils.__logsList

    @staticmethod
    def dumpLogs(filename):
        json_object = json.dumps(
            CommonUtils.getLogs(), indent=2, cls=HexJsonEncoder)
        with open(filename, "w") as outfile:
            outfile.write(json_object)
