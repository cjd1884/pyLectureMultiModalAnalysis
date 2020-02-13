"""
convert video files to mono-audio wavs
"""

import os
import glob
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

import progressbar

from pyAudioAnalysis import convertToWav as cW

def main(argv):

    video2audio()



def video2audio(data_path='../data'):

    # Init vars
    sampling_rate = "16000"
    channels = "1"
    input_dir = data_path + "/video"
    output_dir = data_path + "/audio"

    class_dirs = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

    for d in class_dirs:
        # class directory paths
        input_class_path = input_dir + '/' + d
        output_class_path = output_dir + '/' + d

        # skip if class directory already exists
        if os.path.exists(output_class_path):
            continue

        # create class directory
        os.makedirs(output_class_path)

        video_files = cW.getVideoFilesFromFolder(input_class_path)

        print('Extracting audio file in folder: "' + d + '" ...')

        bar = progressbar.ProgressBar(maxval=len(video_files), \
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        bar_index = 0
        for f in video_files:
            class_dir = os.path.basename(os.path.dirname(f))
            f_name = os.path.basename(f)
            output_name = os.path.splitext(f_name)[0]

            # ffmpeg -i video/videoplayback.mp4 -ar 16000 -ac 1 out.w
            ffmpeg_command = 'ffmpeg -i ' + f + ' -ar ' + sampling_rate + ' -ac ' + channels + ' ' + output_dir + '/' + class_dir + '/' + output_name + '.wav' + ' -loglevel quiet'
            os.system(ffmpeg_command)

            # update progress bar index
            bar_index+=1
            bar.update(bar_index)

        bar.finish()

        print('Audio extraction completed (.mp4 -> .wav).')




if __name__ == '__main__':
    main(sys.argv)
