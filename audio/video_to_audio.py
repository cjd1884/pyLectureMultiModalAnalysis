"""
convert video files to mono-audio wavs
"""

import os
import glob
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

from pyAudioAnalysis import convertToWav as cW

def main(argv):

    sampling_rate = "16000"
    channels = "1"
    input_dir = "../data/video"
    output_dir = "../data/audio"
     
    list_of_dirs = [os.path.join(input_dir, name)
                    for name in os.listdir(input_dir)
                    if os.path.isdir(os.path.join(input_dir, name))]

    print(list_of_dirs)
    for d in list_of_dirs:
        video_files = cW.getVideoFilesFromFolder(d)

        for f in video_files:
            class_dir = os.path.basename(os.path.dirname(f))
            f_name = os.path.basename(f)
            output_name = os.path.splitext(f_name)[0]

            #ffmpeg -i video/videoplayback.mp4 -ar 16000 -ac 1 out.w
            ffmpeg_command = 'ffmpeg -i ' + f + ' -ar ' + sampling_rate + ' -ac ' + channels + ' ' + output_dir + '/' + class_dir + '/' + output_name + '.wav'
            os.system(ffmpeg_command)



if __name__ == '__main__':
    main(sys.argv)
