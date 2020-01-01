'''
Short description: Script for segmenting a YouTube Video.
 The segmentation process relies on librosa's 'split on non-silent' audio parts functionality
'''

import librosa
import ffmpy
import os
import time

def segment_audio(audio_dir,
                  audio_fn,
                  top_db=50,
                  thres_duration=100):
    '''
    Determining the cutoff points in an audio track.
    Using `librosa.effects.split()` we determine the non-silent intervals in an audio track based on
    a threshold value `top_db`.
    The end points of the concurrent intervals may be merged if the duration of the associated
    non-silent audio parts do not exceed a reference threshold value `thes_duration`.

    Input:
      audio_fn: the filename of the audio track, e.g. audio_1.mp4
      top_db:   the threshold (in decibels) below reference to consider as silence
      duration: the threshold duration (in seconds) of a part between cutoff points;
                if None no merging of cutoff points takes place
    Output:
      a list of cutoff points (in seconds)
    '''
    # load audio track
    audio_path = os.path.join(audio_dir, audio_fn)
    audio_track, sr = librosa.load(audio_path, sr=None)
    audio_len = len(audio_track)

    # split on silence
    parts = librosa.effects.split(audio_track, top_db=top_db)
    parts_no = len(parts)

    if thres_duration != None and parts_no > 1:
        # duration of each non-silent parts
        parts_duration = []
        for part in parts:
            w = list(range(part[0], part[1] + 1))  # find samples of audio track covered by a part
            # alternatively,
            # w = [idx for idx in range(audio_len) if segment[0] <= idx <= segment[1]]
            track = audio_track[w]  # restrict audio track to desired samples
            dur = librosa.core.get_duration(track, sr=sr)  # get duration of cropped track
            # print(dur)
            parts_duration.append(dur)  # update: append to list
        # print(parts_duration)

        # breakpoints
        parts_ = list(range(parts_no))
        breakpoints = []
        sample = 0  # start at the beginning of the list
        while sample in parts_:
            duration = parts_duration[sample]       # initialize: duration of current sample
            if duration > thres_duration:           # if the duration of a sample is larger than the threshold value
                sample += 1                         # move to the next sample - this will be a breakpoint
            while duration <= thres_duration:       # while the threshold duration is not exceeded - breakpoints can be merged
                if sample == parts_[-1]:            # we have reached the last element of the list
                    break                           # break inner while
                sample += 1                         # update sample index
                duration += parts_duration[sample]  # update duration
            breakpoints.append(sample - 1)          # append breakpoint
            if sample == parts_[-1]:                # we have reached the last element of the list
                break                               # break outer while
        # print(breakpoints)

        # duration of concurrent parts (parts inbetween breakpoints)
        breakpoints_ = [breakpoint + 1 for breakpoint in breakpoints]
        aug_breakpoints_ = [0] + breakpoints_ + [parts_no]
        # print(aug_breakpoints_)
        bps_len = len(aug_breakpoints_)
        durations_count = []

        for idx in range(1, bps_len):  # for all elements of `breakpoints`
            count = 0
            # print(aug_breakpoints_[idx - 1], aug_breakpoints_[idx])
            for jdx in range(aug_breakpoints_[idx - 1], aug_breakpoints_[idx]):
                count += parts_duration[jdx]
            durations_count.append(count)
        # print(durations_count)

        # is the last breakpoint legit?
        if durations_count[-2] + durations_count[-1] <= thres_duration:  # if not legit
            # print(durations_count[-2] + durations_count[-1])
            # print(durations_count[-2], durations_count[-1])
            breakpoints = breakpoints[:-1]  # remove it
        # print(breakpoints)

        # find the segmentation points: the indices of the `audio_track` where we can cut it
        segmentation_points = []
        for breakpoint in breakpoints:
            segmentation_points.append(parts[breakpoint][1])  # the right-hand extremity of the part
        aug_segmentation_points = [0] + segmentation_points + [audio_len]
        # print(aug_segmentation_points)

        # now we can determine the breakpoints in seconds (or minutes)
        cutoffs = [librosa.core.samples_to_time(elem, sr=sr) for elem in aug_segmentation_points]
        return cutoffs

    elif thres_duration != None and parts_no == 1:
        print('There are no cutoff points. Consider lowering the top_db variable.')
    else:
        for idx in range(1, parts_no):
            # if idx == 0:
            #    parts[idx][0] = 0
            # if idx == parts_no - 1:
            #    parts[idx][0] = parts[idx-1][1] + 1
            #    part[idx][1] = audio_track[-1]
            # else:
            #    part[idx][0] = parts[idx][1] + 1
            parts[idx][0] = parts[idx - 1][1] + 1
        breakpoints = [parts[idx][1] for idx in range(parts_no)]
        aug_breakpoints = [0] + breakpoints + [audio_len]
        cutoffs = [librosa.core.samples_to_time(elem, sr=sr) for elem in aug_breakpoints]
        return cutoffs

def merge_medium(audio_fn,
                 audio_dir='./data/audio',
                 media_dir='./data/media',
                 out_dir='./data/segmented',
                 top_db=50,
                 thres_duration=100):
    '''
    Segment a YouTube Video to parts , where the endpoints (start/stop points) are determined by `segment_audio()` fubction.
    The segmented Videos are stored locally in the `out_dir` directory.

    Input:
      audio_fn:       see `segment_audio()`
      media_path:     path to where the media files (Video files) are located
      top_db:         see `segment_audio()`
      thres_duration: see `segment_audio()`
    Output:
      None
    '''
    # cutoff points of audio track
    cutoffs = segment_audio(audio_dir=audio_dir, audio_fn=audio_fn, top_db=top_db, thres_duration=thres_duration)

    # match medium (Video) to audio track
    media_filenames = os.listdir(media_dir)
    matched_medium = [medium_fn for medium_fn in media_filenames
                     if medium_fn.split('.')[0].split('_')[-1] == audio_fn.split('.')[0].split('_')[-1]]
    matched_medium = matched_medium[0]
    # print(matched_medium)

    # paths & directories
    medium_path = os.path.join(media_dir, matched_medium)
    medium_ = matched_medium.split('.')[0]
    os.makedirs(out_dir, mode=0o777, exist_ok=True)

    # segment Video
    for idx in range(1, len(cutoffs)):
        start = time.strftime('%H:%M:%S', time.gmtime(cutoffs[idx - 1]))
        end = time.strftime('%H:%M:%S', time.gmtime(cutoffs[idx]))
        output_name = medium_ + '_' + str(idx) + '.mp4'
        output = os.path.join(out_dir, output_name)

        inp = {medium_path: ['-ss', start]}
        oup = {output: ['-to', end, '-c', 'copy']}

        ff = ffmpy.FFmpeg(inputs=inp, outputs=oup)
        # print(ff.cmd)
        ff.run()

# run
aud_path = './data/audio'
aud_filenames = os.listdir(aud_path)
print(aud_filenames)
aud_filenames = [aud_fn for aud_fn in aud_filenames if 'ipynb' not in aud_fn]
print(aud_filenames)
aud_no = len(aud_filenames)

for idx in range(aud_no):
    merge_medium(audio_fn=aud_filenames[idx])