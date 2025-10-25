# white-hmong-gams

This repository contains the code used for a project done by Henry Heyden and Zuoyu Tian at Macalester College, during Summer and Fall of 2025. This project looked at tonal realization in White Hmong. Using Generalized Additive Models (GAMs), we examined the effect of linguistic factors (e.g. duration, previous tone, utterance position, etc.) on the realization of the low-rising (-v) tone. The data examined for this project was collected by Garellek and Esposito for their 2023 paper *Phonetics of White Hmong vowel and tonal contrasts*. This data is not released here in any way.

# Organization

There are four folders in this repository, which each folder containing the code for one part of the project.

## measurements

The first step of this project was to measure F0 across the speech material. This was done using Parselmouth and Praat. We normalized F0 to semitones using a reference value of each speaker's average F0 (in Hz). We also had to do some calculation for duration and utterance position, and the code for those calculations is also included in this folder.

## GAMs

The measurements taken in `measurements` were brought into R and we created two GAMs built to predict F0 over time using the mgcv package. The GAMs folder has the summary tables for those GAMs, as well as the code to create the plots seen in `plots`, and the form vectors used in `modeling`.

## plots

The plots seen in `plots` are the main results of this study. They present the changes in tonal contours of the low-rising tone as linguistic factors are changed, and were made using predictions from the GAMs. The code for these plots is presented in `GAMs`.

## context_embeddings

The last main part of our study was to examine if a feed forward neural network could predict word meaning from tonal contour alone. Before performing such an experiment, some mathematical representation of "meaning" needed to be constructed. We did so using OpenAI's [text-embedding-3-large](https://platform.openai.com/docs/models/text-embedding-3-large) model, averaging the embedding of a context window with that of the word itself. This folder contains the code with which those embeddings were created. It also contains `PCA_norm.png`, which is a plot of the relative position of embeddings based on NormalizedWord, using PCA to go from 3072 dimensions to 2.

## modeling

In `modeling`, the neural network was trained to predict the embeddings from `context_embeddings` from pitch contours (constructed using the GAMs in `GAMs`). As no data is presented alongside this code, this folder is mostly given to show details of our architecture and workflow. There is also a subfolder, `results`, which presents a number of visualizations of the results of this portion of the study:

- `accuracy_comparison.png` lets us compare accuracy accross models trained with word-agnostic predicted contours, and those which were predicted using word information. The values shown were made using cross-validation, meaning for each type of input vector, 5 models were trained (40 epochs each), each using a different 20% split of the data as the held-out test set. Accuracy was then calculated for both seen and unseen data by having the model run inference on an input, and then counting a success whenever the word type of the closest vector in the output space had the same word type as the correct output. Then accuracy was averaged over the 5 models to create the values shown on `accuracy_comparison.png`.

- `confusion_matrix_{non-word, word}.png` show confusion matrices for unseen data. This allows us to see how many times the model trained on tonal contours from the game that {did not, did} have access to word type information predict, e.g. *qav* when it should have predicted *kuv*.

- `word_distribution.png` is a natural companion to `confusion_matrix_{non-word, word}.png`, as both models clearly decided predicting *qav* and *tsov* was the best course of action to minimize loss, which is a problem that could easily be caused by class imbalance.