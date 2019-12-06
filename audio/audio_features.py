"""
segment-based audio feature extraction
"""

import os
import logging
logging.basicConfig(level=logging.DEBUG)

from pyAudioAnalysis import MidTermFeatures as aF
import utilities as ut

"""
It takes a list of paths as inputs and returns a list of feature matrices.

Each resulting feature vector is extracted by long-term averaging the mid-term features.
One feature vector is extracted for each WAV file.


ARGUMENTS:
    list_of_dirs:       list of paths of directories. Each directory
                        contains a single audio class whose samples
                        are stored in seperate WAV files.
    mt_win, mt_step:    mid-term window length and step
    st_win, st_step:    short-term window and step

RETURNS:
    features:
    feature_names:
    class_names:
    file_names:
    
"""
def audio_features_extraction(list_of_dirs,mt_win,mt_step,st_win,st_step,compute_beat):

    class_names = [os.path.basename(d) for d in list_of_dirs]
    features = []
    file_names = []
    for d in list_of_dirs:
        f, file_names, feature_names = \
            aF.directory_feature_extraction(d,mt_win,mt_step,st_win,st_step,compute_beat)
        if f.shape[0] > 0:
            features.append(f)
            file_names.append(feature_names)
            if d[-1] == os.sep:
                class_names.append(d.split(os.sep)[-2])
            else:
                class_names.append(d.split(os.sep)[-1])

    if len(features) == 0:
        logging.error("ERROR: No data found in any input folder!")
        return

    return features, feature_names, class_names, file_names


def main():

    mt_win = 1.0
    mt_step = 1.0
    st_win = 0.050
    st_step  = 0.050
    compute_beat = False

    dir_name = "../data/audio"
    list_of_dirs = [os.path.join(dir_name, name)
                    for name in os.listdir(dir_name)
                    if os.path.isdir(os.path.join(dir_name, name))]

    [features, feature_names, class_names, file_names ] = \
            audio_features_extraction(list_of_dirs,mt_win,mt_step,st_win,st_step,compute_beat)

    # uncomment for plot 
    #ut.plot_feature_histograms(features, feature_names, class_names)

if __name__ == '__main__':
    main(sys.argv)
