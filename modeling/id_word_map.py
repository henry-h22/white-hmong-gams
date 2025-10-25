import pandas as pd

class IdWordMap:
    def __init__(self, csv_path: str = 'hmongData-v-ST_AVG.csv'):
        dataFrame = pd.read_csv(csv_path)
        normWordList = dataFrame['NormalizedWord']
        wordList = dataFrame['Word']
        self.ids, self.wordMap = [], {}
        for i in range(len(normWordList)):
            if normWordList[i] != 'X':
                markers = wordList[i].split('_')
                if not ('p' in markers or 'df' in markers):
                    self.ids.append(i)
                    self.wordMap[i] = normWordList[i]

    def __getitem__(self, i: int):
        """"
        Takes in a file index 0, 1, ..., and returns the word. 
        If you need the intermediate index to the data frame, use .ids[i]
        """
        return self.wordMap[self.ids[i]]
