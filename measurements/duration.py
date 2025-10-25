import tgt # TextGridTools, helps parsing text grids https://github.com/hbuschme/TextGridTools
from tgt import TextGrid
import csv

def textgrid(file) -> TextGrid:
    """
    :returns: tgt TextGrid object
    """
    text = tgt.read_textgrid(f"./textgrid/{file}.TextGrid") # tgt TextGrid object
    return text

# Function to arrange the information into a data line
def arrangeDataLine(speaker_info, tone, interval_text, previous_tone, f0_values, f1_values):
    """
    :param speaker_info: is as described in the docstring of processFile below
    """

    filename, speaker = speaker_info

    currentIntervalTextList = interval_text.split('_') 
    # The above line gives a list of strings, where index 0 has the word, and index 1+ has phrase information, if given

    # Encode phrase info as binary 0/1
    ui = 1 if 'ui' in currentIntervalTextList else 0
    uf = 1 if 'uf' in currentIntervalTextList else 0
    p = 1 if 'p' in currentIntervalTextList else 0
    df = 1 if 'df' in currentIntervalTextList else 0

    # Headers: token_id, FileName, Speaker, tone, TextGrid text (w/ phrase info e.g. _ui), ui?, uf?, p?, df?, PreviousTone, F0_values (list), F1_values (list)
    # (^ from write to csv cell)
    return [filename, speaker, tone, interval_text, ui, uf, p, df, previous_tone, f0_values, f1_values]


def processFile(text : TextGrid, tone):
    """
    :param speaker_info: is a size-2 tuple of strings containing (file, speaker), TO BE EXPANDED LATER WITH: age, gender, etc.
    """
    dataForCurrentFile = []
    for interval in text.tiers[0]:
        interval_text = interval.text
        interval_text_list = interval_text.split('_')
        currentWord = interval_text_list[0]
        currentTone = currentWord[-1:]
        if currentTone not in ['b', 's', 'j', 'v', 'm', 'g', 'd']:
            currentTone = '0'

        if currentTone == tone:
            dataForCurrentFile.append(interval.duration())

    return dataForCurrentFile

def hmongCSV_duration(data, tone, dir = 'duration_csvs'):
    with open(f'{dir}/hmongData-{tone}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['token_id', 'Duration'])
        writer.writerows(data)


if __name__ == '__main__':
    tones = ['b', 's', 'j', 'v', 'm', 'g', 'd', '0']
    for tone in tones:

        # Code that works through every given file for each speaker and story
        speakers = ['Cha', 'Chingla', 'Ellina', 'Gozong', 'Long', 'MaiXee', 'MaiXor', 'Ma']
        stories = ['1', '2', '3']

        data = []
        token_id = 0
        for speakerIndex in range(len(speakers)):
            speaker = speakers[speakerIndex]
            print(f'Doing speaker {speaker} for tone {tone}')
            for story in stories:
                file = f'{speaker}Story{story}'
                text = textgrid(file)
                for durationValue in processFile(text, tone):
                    data.append([token_id, durationValue])
                    token_id += 1

        hmongCSV_duration(data = data, tone = tone)
                
                