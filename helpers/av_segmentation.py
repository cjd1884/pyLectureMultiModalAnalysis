"""
"""

###########
# IMPORTS #
###########

import os
import ffmpy
import librosa
import time
from pyAudioAnalysis.audioSegmentation import silenceRemoval as sR
from pyAudioAnalysis.audioBasicIO import read_audio_file


######################
# AUDIO SEGMENTATION #
######################

def segment_audio(audio_fn,
                  audio_dir='./data/audio_wav',
                  st_win=0.05,
                  st_step=0.05,
                  up_bound=20):
    """
    Partition an audio track into smaller segments; the duration of each segment (with the exception of the last one)
    is at most `up_bound`.

    Input:
      audio_fn:         the filename of the audio track, e.g. 'audio_1.wav'
      audio_dir:        the directory of audio tracks (in `wav` format)
      st_win, st_step:  short term window and step
      up_bound:         upper bound on the duration of segments (in seconds)
    Output:
      a list of audio segments of the form [[a0, b0], [a1, b1], ...]
    """
    # audio track duration using `librosa`
    audio_path = os.path.join(audio_dir, audio_fn)
    y, sr = librosa.load(audio_path, sr=None)
    audio_duration = librosa.core.get_duration(y=y, sr=sr)

    # determine start and end points of silent parts using `pyAudioAnalysis`
    fs, x = read_audio_file(audio_path)  # fs: sampling rate, x = audio as `numpy` array
    seg_lims = sR(x=x, fs=fs, st_win=st_win, st_step=st_step)
    seg_num = len(seg_lims)
    # print(seg_num)

    # determine cutoff points: eligible points for segmenting the audio track
    cutoffs = [seg_lims[idx][0] + 0.5 * (seg_lims[idx][1] - seg_lims[idx][0]) for idx in range(seg_num)]
    cutoffs = [0.0] + cutoffs  # appending the start of the audio track

    # determine audio segments: compute the beginning and end points (in seconds) of audio segments
    segments = []
    running_idx = 0

    while True:
        if running_idx == 0:
            start_point = 0.0
        else:
            start_point = cutoffs[running_idx]
        # print('start point', start_point)
        durations = [cutoff for cutoff in cutoffs if 0 <= cutoff - start_point < up_bound]
        # print(durations)
        end_point = durations[-1]
        # print(end_point)
        running_idx += len(durations) - 1
        if running_idx == seg_num:
            break
        segments.append([start_point, end_point])
    # print(segments)

    # regularizations
    # [a] extending to the end of the audio track
    # print(segments[-1])
    if audio_duration - segments[-1][1] < 6:
        segments[-1][1] = audio_duration
    else:
        segments.append([segments[-1][1], audio_duration])
    # print(segments[-1])
    # [b] increment the start point of each segment (except the first one) by 0.01
    offset = 0.01
    # print(segments[0][0], segments[1][0])
    for idx in range(1, len(segments)):
        segments[idx][0] += offset
    # print(segments[0][0], segments[1][0])

    return segments


# RUN
# segments = segment_audio(audio_fn='audio_1.wav', audio_dir='./audio_wav')
# for segment in segments:
#     print(segment)

#######################
# MEDIUM SEGMENTATION #
#######################

def segment_medium(audio_fn,
                   audio_dir='./data/audio_wav',
                   media_dir='./data/media',
                   out_dir='./data/segmented',
                   st_win=0.05,
                   st_step=0.05,
                   up_bound=20):
    """
    Partition a Youtube video into parts of (at most) `up_bound` duration.
    Segments are determined based on the audio track and are stored into folders inside `out_dir`.

    Input:
     audio_fn:        name of the audio track
     audio_dir:       directory of audio tracks
     media_dir:       directory of media
     st_win, st_step: short term window and step
     up_bound:        upper bound on segment duration
    Output:
     None
    """
    # audio segments
    segments = segment_audio(audio_dir=audio_dir, audio_fn=audio_fn,
                             st_win=st_win, st_step=st_step, up_bound=up_bound)

    # match medium (video with audio) to audio track
    media_filenames = os.listdir(media_dir)
    matched_medium = [medium_fn for medium_fn in media_filenames
                      if medium_fn.split('.')[0].split('_')[-1] == audio_fn.split('.')[0].split('_')[-1]]
    matched_medium = matched_medium[0]
    #   print(matched_medium)

    # paths & directories
    medium_path = os.path.join(media_dir, matched_medium)
    medium_ = matched_medium.split('.')[0]
    #    print(medium_)
    dir_ = os.path.join(out_dir, medium_)
    os.makedirs(dir_, mode=0o777, exist_ok=True)

    # segment Video
    for idx in range(len(segments)):
        elapsed = segments[idx][1] - segments[idx][0]
        start = time.strftime('%H:%M:%S', time.gmtime(segments[idx][0]))
#        end = time.strftime('%H:%M:%S', time.gmtime(segments[idx][1]))
        duration = time.strftime('%H:%M:%S', time.gmtime(elapsed))

        # print(start)
        # print(end)
        output_name = 'part' + '_' + str(idx) + '.mp4'
        output = os.path.join(dir_, output_name)

        inp = {medium_path: ['-ss', start]}
        oup = {output: ['-to', duration, '-c', 'copy']}

        ff = ffmpy.FFmpeg(inputs=inp, outputs=oup)
        print(ff.cmd)
        ff.run()


# RUN
# segment_medium(audio_fn='audio_1.wav', audio_dir='./audio_wav', media_dir='./media', out_dir='./segmented')
