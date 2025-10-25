"""

Code by Henry to calculate reference values in order to perform various methods of semitone-based normalization on F0 and F1

We'd like to calculate AvgF0, and then maybe one day Pmin and Pmax.

"""

import parselmouth
from pandas import isnull
import csv

def getPitch(file):
    audio = parselmouth.Sound(f"./wav/{file}.wav") # Parselmouth Sound object
    pitch = audio.to_pitch_cc(time_step = 0.001, pitch_floor = 50, pitch_ceiling = 400, very_accurate = True) # TODO consider changing the default variables here, e.g. octave jump cost
    return pitch

def getF1(file):
    audio = parselmouth.Sound(f"./wav/{file}.wav") # Parselmouth Sound object
    formants = audio.to_formant_burg()
    return formants

# Getting AvgF0 (and F1) for a speaker
def getAverageF0andF1forSpeaker(speaker, stories = ['1', '2', '3']):
    f0_vals = []
    f1_vals = []

    for story in stories:
        file = f'{speaker}Story{story}'

        pitch = getPitch(file)
        formants = getF1(file)
        duration = pitch.get_end_time()
        t = pitch.get_start_time()
        while t < duration:
            f0 = pitch.get_value_at_time(t)
            f1 = formants.get_value_at_time(1, t)
            if not isnull(f0):
                f0_vals.append(f0)
            if not isnull(f1):
                f1_vals.append(f1)
            
            t += 0.001

    avgF0 = sum(f0_vals) / len(f0_vals)
    avgF1 = sum(f1_vals) / len(f1_vals)
    return avgF0, avgF1


if __name__ == "__main__":
    speakers = ['Cha', 'Chingla', 'Ellina', 'Gozong', 'Long', 'MaiXee', 'MaiXor', 'Ma']
    data = [['Speaker', 'AvgF0', 'AvgF1']]
    for speaker in speakers:
        f0, f1 = getAverageF0andF1forSpeaker(speaker = speaker)
        data.append([speaker, f0, f1])
    with open(f'hmong_semitone_references.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)