"""
segment-based audio feature extraction
"""

import os
import sys
import glob
import time
import numpy as np
import pandas as pd
import logging
import progressbar
#logging.basicConfig(level=logging.DEBUG)

#from pyAudioAnalysis import utilities
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import MidTermFeatures as aF
# import utilities as ut

from . import video_to_audio as v2a


"""
This function extracts the mid-term features of the WAVE files from the index CSV.

It takes a list of audio files as inputs and returns a list of feature matrices.

Each resulting feature vector is extracted by long-term averaging the mid-term features.
One feature vector is extracted for each WAV file.


ARGUMENTS:
    dir_name:           Directory that contains the audio files
    mt_win, mt_step:    mid-term window length and step (in seconds)
    st_win, st_step:    short-term window and step (in seconds)

RETURNS:
    features:
    feature_names:
    file_names:
    
"""
def audio_features_extraction(dir_name="../data", mt_win=1.0, mt_step=1.0, st_win=0.050, st_step=0.050, features_audio_file='Audio2Features.pkl'):

    audio_dir = dir_name + '/'+ 'audio'

    # first, extract audio from video
    v2a.video2audio(dir_name)

    features = []
    file_names = []

    mid_term_features = np.array([])
    process_times = []

    # type is WAVE file, convert using the function video_to_audio.py
    suffix = ".wav"
    index_df = pd.read_csv(dir_name+'/'+'index.csv', sep=';')

    wav_file_list, mid_feature_names = [], []

    # iterate each audio file
    print('Extracting features from audio files...')

    bar = progressbar.ProgressBar(maxval=len(index_df), \
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    bar_index = 0
    for ind in index_df.index:
        name = index_df['FILE'][ind]
        seg = str(index_df['SEG'][ind])

        file_path = audio_dir + '/' + name + '/' + seg + suffix
        # print("Analyzing file {0:d} of {1:d}: {2:s}".format(ind+1,len(index_df),file_path))

        if os.stat(file_path).st_size == 0:
            logging.warning("WARNING: EMPTY FILE -- SKIPPING")
            continue
        [sampling_rate, signal] = audioBasicIO.read_audio_file(file_path)
        if sampling_rate == 0:
            logging.warning("WARNING: NO SAMPLING RATE -- SKIPPING")
            continue

        t1 = time.clock()
        signal = audioBasicIO.stereo_to_mono(signal)
        if signal.shape[0] < float(sampling_rate)/5:
            logging.warning("WARNING: AUDIO FILE TOO SMALL -- SKIPPING")
            continue
        wav_file_list.append(file_path)

        mid_features, _, mid_feature_names = \
            aF.mid_feature_extraction(signal, sampling_rate,
                                    round(mt_win * sampling_rate),
                                    round(mt_step * sampling_rate),
                                    round(st_win * sampling_rate),
                                    round(st_step * sampling_rate))
        mid_features = np.transpose(mid_features)
        mid_features = mid_features.mean(axis=0)
        # long term averaging of mid-term statistics
        if (not np.isnan(mid_features).any()) and \
                (not np.isinf(mid_features).any()):
            if len(mid_term_features) == 0:
                # append feature vector
                mid_term_features = mid_features
            else:
                mid_term_features = np.vstack((mid_term_features,mid_features))

        t2 = time.clock()
        duration = float(len(signal)) / sampling_rate
        process_times.append((t2 - t1) / duration)

        # update progress bar index
        bar_index += 1
        bar.update(bar_index)

    bar.finish()

    if len(process_times) > 0:
        print("Audio feature extraction completed. Complexity ratio: "
                "{0:.1f} x realtime".format((1.0 /
                                            np.mean(np.array(process_times)))))

    print('Shape: ' + str(mid_term_features.shape))

    ftr_df = pd.DataFrame(data=mid_term_features)
    df=index_df.copy()
    df=pd.concat([df,ftr_df], axis=1)
    if True:
        df.to_pickle(dir_name + '/' + features_audio_file)

    return mid_term_features, wav_file_list, mid_feature_names

def main(argv):

    f, fn, feature_names = \
        audio_features_extraction()

    #print(f,fn,feature_names)

if __name__ == '__main__':
    main(sys.argv)
