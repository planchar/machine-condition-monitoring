"""
This module contains helper functions to:
- generate the list of file paths of the audio samples
- extract audio features for each audio sample
- create a dataframe containing the extracted features
"""

import os
from multiprocessing import Pool
# import time  ## uncomment to measure execution time

import librosa
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.curdir, "data")
FRAME_LENGTH = 2048
HOP_LENGTH = 1024


def get_file_paths():
    """
    Returns a dictionary with all the paths to audio files in DATA_DIR.
    """
    
    # extract file names per folder path into a dictionary
    folder_contents = {a: c for a, b, c in os.walk(DATA_DIR) if len(c)>0}
    
    # create a list to collect file paths    
    paths = []

    for path, files in folder_contents.items():
        for file in files:
            paths.append(os.path.join(path, file))
    
    # convert the list of file paths into a dictionary with id's
    file_paths = {idx:path for (idx, path) in enumerate(paths)}

    return file_paths


def calculate_amplitude_envelope(y, frame_size):
    """
    Calculates and returns the amplitude envelope.
    """
    
    amplitude_envelope = []
    
    for i in range (0, len(y), frame_size):
        frame_ae = max(y[i:i+frame_size])
        amplitude_envelope.append(frame_ae)
    
    return np.array(amplitude_envelope)

def calculate_split_frequency(S, split_freq, sr):
    """
    Calculate and return the split frequency.
    """
    
    frange = sr/2
    delta_f_perbin = frange/S.shape[0]
    split_freq_bin = np.floor(split_freq/delta_f_perbin)
    
    return int(split_freq_bin)

def calculate_band_energy_ratio(S, split_freq, sr):
    """
    Calculates and returns the Band Energy Ratio (BER).
    """
    
    split_freq_bin = calculate_split_frequency(S, split_freq, sr)
    
    power = librosa.amplitude_to_db(S).T

    BER = []
    #calculate the energy ratio in each frame
    for frequency in power:
        sum_low_freq = np.sum(frequency[:split_freq_bin])
        sum_high_freq = np.sum(frequency[split_freq_bin:])
        BER_frame = sum_low_freq/sum_high_freq
        BER.append(BER_frame)

    return np.array(BER)

def get_features(file_path):
    """
    This function gets a feature vector for a file on a specified file path.
    
    When extracting features for a collection of audio samples, we want to 
    sequentially access audio files, perform the desired computations, extract the 
    useful information, and close the files to get them out of memory. By combining 
    these steps file by file, we can use multiprocessing to distribute the workload. 
    That is the purpose of this function.
    
    As input, the function takes a tuple of index and file path.
    
    As output, the function returns a one-dimensional array; a feature vector.
    """    
    
    # load the file in librosa
    y, sr = librosa.load(path=file_path[1], sr=None)
    
    # compute time domain features
    # !!! when adding features, also add labels in get_column_labels func !!!
    # Amplitude Envelope
    ae = calculate_amplitude_envelope(y=y, frame_size=FRAME_LENGTH)
    # Root Mean Square Energy
    rms = librosa.feature.rms(y=y)
    # Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y=y)
    
    # apply Short Time Fourier Transform
    spec = np.abs(librosa.stft(y=y))
    
    # compute frequency domain features
    # !!! when adding features, also add labels in get_column_labels func !!!
    # BER
    ber = calculate_band_energy_ratio(S=spec, split_freq=1000, sr=sr)
    # Spectral centroid
    sce = librosa.feature.spectral_centroid(S=spec, sr=sr)
    # Spectral bandwidth
    sbw = librosa.feature.spectral_bandwidth(S=spec, sr=sr)
    # Spectral contrast
    sco = librosa.feature.spectral_contrast(S=spec, sr=sr)
    # Spectral flatness
    sfl = librosa.feature.spectral_flatness(S=spec)
    # Spectral roll-off
    sro = librosa.feature.spectral_rolloff(S=spec, sr=sr)
    sro_99 = librosa.feature.spectral_rolloff(S=spec, sr=sr, roll_percent=0.99)
    sro_01 = librosa.feature.spectral_rolloff(S=spec, sr=sr, roll_percent=0.01)
    
    # list all features
    features = [ae, rms, zcr, ber, sce, sbw, sco, sfl, sro, sro_99, sro_01]
    
    # compute aggregations for features
    aggregations = [(f.mean(), f.min(), f.max(), f.std()) for f in features]
    
    # compose list of features
    audio_features = [file_path[0]]
    audio_features.extend([i for tup in aggregations for i in tup])
    
    # append distributed features
    # append distributed AE
    audio_features.extend(calculate_amplitude_envelope(y=y, frame_size=sr*2))
    # append distributed RMS
    rms_distr = librosa.feature.rms(y=y, hop_length=sr, frame_length=sr*2)[0].tolist()
    audio_features.extend(rms_distr)
    # append distributed ZCR
    zcr_distr = librosa.feature.zero_crossing_rate(y=y, hop_length=sr, frame_length=sr*2)[0].tolist()
    audio_features.extend(zcr_distr)
    
    return audio_features

def get_column_labels():
    """
    This function generates a list of column names for the extracted features 
    that are returned by the get_features function.

    """

    # list the names of the extracted features
    feature_labels = ["amplitude_envelope", 
                      "root_mean_square_energy", 
                      "zero_crossing_rate", 
                      "band_energy_ratio",
                      "spectral_centroid", 
                      "spectral_bandwidth", 
                      "spectral_contrast", 
                      "spectral_flatness", 
                      "spectral_rolloff", 
                      "spectral_rolloff_99", 
                      "spectral_rolloff_01"]
    
    # list the names of the used descriptive statistics
    measure_suffixes = ["_mean", "_min", "_max", "_std"]
    
    # create a list to append the generated column names to
    columns = ["row_index"]

    # generate some labels and append them to the list
    columns.extend([l+s for l in feature_labels for s in measure_suffixes])
    
    # append labels for the distributed AE
    columns.extend(["amplitude_envelope_f1", 
                    "amplitude_envelope_f2", 
                    "amplitude_envelope_f3", 
                    "amplitude_envelope_f4", 
                    "amplitude_envelope_f5"])
    
    # append labels for the distributed RMS
    columns.extend(["root_mean_square_energy_f0", 
                    "root_mean_square_energy_f1", 
                    "root_mean_square_energy_f2", 
                    "root_mean_square_energy_f3", 
                    "root_mean_square_energy_f4", 
                    "root_mean_square_energy_f5", 
                    "root_mean_square_energy_f6", 
                    "root_mean_square_energy_f7", 
                    "root_mean_square_energy_f8", 
                    "root_mean_square_energy_f9", 
                    "root_mean_square_energy_f10"])
    
    # append labels for the distributed ZCR
    columns.extend(["zero_crossing_rate_f0", 
                    "zero_crossing_rate_f1", 
                    "zero_crossing_rate_f2", 
                    "zero_crossing_rate_f3", 
                    "zero_crossing_rate_f4", 
                    "zero_crossing_rate_f5", 
                    "zero_crossing_rate_f6", 
                    "zero_crossing_rate_f7", 
                    "zero_crossing_rate_f8", 
                    "zero_crossing_rate_f9", 
                    "zero_crossing_rate_f10"])
    
    return columns

def get_features_data(file_paths):
    """
    This function creates and returns a dictionary containing:
    - a list of column labels
    - an array of data with all the extracted features
    
    With the dictionary we'll create a dataframe in pandas.

    To speed up the process multiprocessing has been used.
    """
    
    # start_time = time.time()  ## uncomment to measure execution time
    
    # create a dictionary and store the column labels
    features = {"columns": get_column_labels()}
    
    # create a process pool (for multiprocessing)
    p = Pool()
    
    # get features for each file path and store in dictionary
    features["data"] = p.map(get_features, file_paths.items())
    
    p.close()
    p.join()
    
    # duration = time.time() - start_time  ## uncomment to measure execution time
    # print(f"Processing {len(file_paths)} samples took {duration:.0f} seconds.")  ## uncomment to measure execution time
    
    return features

def get_base_df(file_paths):
    """
    *FIXME* to check and test
    """

    # use the file_paths to create a list of info per file
    for path in file_paths.values():
        # split folder paths
        parts = path.split(sep=os.sep)
    
    # deduce information by combining folder names and the level
    # of the folder in the folder hierarchy
    is_defect = True if folder_names[-1] == "abnormal" else False
    machine_id = folder_names[-2]
    machine_type = folder_names[-3].capitalize()
    snr = folder_names[-4].split("_dB_")[0]
    
    # create a list of features that apply to files in this folder
    file_features = [machine_type, machine_id, snr, is_defect]
    
    # loop over files
    for file_name in file_names:
        # construct the file_path and store it in a list
        file_info = [os.path.join(folder_path, file_name)]
        
        # extend the list with file_features
        file_info.extend(file_features)
        
        # append file_info list to audio_samples list
        audio_samples.append(file_info)

def get_df(features, file_paths):

    # get df_base
    df_base = get_base_df(file_paths)

    # get df_extra
    df_extra = pd.DataFrame(data=features["data"], columns=features["columns"])

if __name__ == '__main__':
    #goal: get filepaths, calculate features, construct dataframe, export to csv
    # get filepaths
    file_paths = get_file_paths()
    # get features
    features = get_features_data(file_paths)
    # construct dataframe
    df = get_df(features, file_paths)
    # write to output
    print("Still under construction.")