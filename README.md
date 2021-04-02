# Machine Condition Monitoring

This repository contains a solution to a use-case for [Codit](https://www.codit.eu) that was part of an AI bootcamp at [BeCode.org](https://becode.org).

The goal was to train a supervised machine learning model that can predict when a machine will fail based on audio recordings of the machine. 

The provided dataset was the [MIMII Dataset](https://zenodo.org/record/3384388): a sound dataset for Malfunctioning Industrial Machine Investigation and Inspection. It contains a set of labeled audio files with recordings of four types of machines in normal and anomalous condition.

The project had the following phases:
1. Exploring the digital signal processing domain
2. Getting the dataset
3. Extracting features from the audio to train the model on
4. Evaluating and finetuning
5. Presenting the results

## Getting Started

### Repository Outline

The repository contains some tools we used during each phase.

#### 1. Exploring the digital signal processing domain

The information resources we used to gain more insight into the project are further elaborated on in the [resources](#Resources) section below.

#### 2. Getting the dataset

As stated above, we worked with the [MIMII Dataset](https://zenodo.org/record/3384388).

To help download the complete dataset, some scripts and guidance is provided in the [preparation.md file](./setup/preparation.md) in the setup folder.

#### 3. Extracting features from the audio to train the model on

We chose to save the features we extracted into a csv file to be able to easily import them in a Pandas DataFrame later on.

An [example csv output](./data/dataset.zip) can be found as a zip archive in the data folder.

To calculate the features on the unzipped data, we used a python script that can be found in the setup folder as [audioparser.py](./setup/audioparser.py).

Initially, we imported audioparser.py in a Jupyter notebook to create the dataframe. Our final goal was to make the file able to produce a csv output file by itself, but due to time constraints we weren't able to implement that improvement.

#### 4. Evaluating and finetuning

For this step we used a Jupyter notebook that is to be included.

#### 5. Presenting the results

Our final presentation is not included in this repository.

### Software Requirements

Software:
* Python 3.9

Python packages:
* numpy
* pandas
* librosa
* sklearn

## Citations

Harsh Purohit, Ryo Tanabe, Kenji Ichige, Takashi Endo, Yuki Nikaido, Kaori Suefusa, and Yohei Kawaguchi, “MIMII Dataset: Sound Dataset for Malfunctioning Industrial Machine Investigation and Inspection,” arXiv preprint arXiv:1909.09347, 2019. URL: https://arxiv.org/abs/1909.09347

<!-- add librosa -->

## Resources

To explore the digital signal processing domain and the dataset, we found a couple of resources helpful. It would be a long list if we had to include all of them, but the main ones were:

* [The research paper describing the dataset](https://arxiv.org/abs/1909.09347)
* [Librosa Audio and Music Signal Analysis in Python](https://youtu.be/MhOdbtPhbLU)
* [Audio Signal Processing for Machine Learning](https://youtube.com/playlist?list=PL-wATfeyAMNqIee7cH3q1bh4QJFAaeNv0)
* [Music Information Retrieval using Scikit-learn](https://youtu.be/oGGVvTgHMHw)
* [Intuitive Understanding of the Fourier Transform and FFTs](https://youtu.be/FjmwwDHT98c)

## About

### Contributors

* [Mohammad Khodery](https://github.com/medokhodeery)
* [Philippe Planchar](https://github.com/planchar)

### Notes

* Collaboration on the project happened mostly as remote [pair programming](https://en.wikipedia.org/wiki/Pair_programming) in [Jupyter](https://jupyter.org/) notebooks. Near the end of the project, the code was reviewed and edited, and only the final solution was uploaded to GitHub.