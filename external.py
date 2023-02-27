
import pickle

class Log():
    def __init__(self):
        pass


class Sound():
    def __init__(self):
        pass
    def playMusic(self,id):
        pass
    def playEffect(self,id):
        pass

class File():
    def __init__(self):
        self.dataFile = "kai.sa"
    def saveData(self,character,environment):
        with open(self.dataFile, 'wb') as output:
            pickle.dump(character, output, pickle.HIGHEST_PROTOCOL)
            pickle.dump(environment, output, pickle.HIGHEST_PROTOCOL)
    def loadData(self):
        return
        with open(self.dataFile, 'rb') as input:
            character = pickle.load(input)
            environment = pickle.load(input)
            return [environment,character]
