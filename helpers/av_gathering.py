###########
# IMPORTS #
###########

import os
import pytube
import ffmpy

##########################
# DOWNLOAD YOUTUBE VIDEO #
##########################

'''
Short description: Leveraging on `pytube`, this script downloads and stores locally
 the audio and video files associated with a YouTube object.
 Audio and video files are stored in separate folders.
 '''


def get_audio_itag(stream_lst,
                   abr='128kbps',
                   subtype='mp4'):
    """
    Return the `itag` of a YouTube video with specified audio bitrate (`abr`) and subtype.
    If the desired `arb` does not exist, the user is prompt to input a new one from a list.

    Input:
      stream_lst:  list of available media formats
      abr:         desired bit rate, string of the form `xxxkpbs`, where `x` is a number
      subtype:     desired subtype, string -- available options are `mp4` (default) and `webm`
    Output:
      `itag` of YouTube object
    """
    audio_streams = [stream for stream in stream_lst if stream.includes_audio_track == True
                     and stream.includes_video_track == False]
    audio_abrs = [stream.abr for stream in audio_streams if stream.subtype == subtype]
    if abr not in audio_abrs:
        print('Select a new abr variable from the following list: ', audio_abrs)
        new_abr = input()
        return get_audio_itag(stream_lst, new_abr, subtype)
    itag = [stream.itag for stream in audio_streams if stream.abr == abr]
    audio_itag = itag[0]
    return audio_itag


def get_video_itag(stream_lst,
                   res='360p',
                   subtype='mp4'):
    """
    Return the `itag` of a YouTube video with specified resolution and subtype.
    If the desired resolution does not exist, the user is prompt to input a new one from a list.

    Input:
      stream_lst:  a list of available media formats
      res:         desired resolution, string of the form `xxxp`, where `x` is a number
      subtype:     desired subtype, string -- available options are `mp4` (default) and `webm`
    Output:
      `itag` of YouTube video
    """
    video_streams = [stream for stream in stream_lst if stream.includes_audio_track == False]
    resolutions = [stream.resolution for stream in video_streams
                   if stream.resolution != None and stream.subtype == subtype]
    if res not in resolutions:
        print('Select a new video resolution from the list: ', resolutions)
        new_res = input()
        return get_video_itag(stream_lst, new_res, subtype)
    itag = [stream.itag for stream in video_streams if stream.resolution == res
            and stream.subtype == subtype]
    video_itag = itag[0]
    return video_itag


def download_medium(youtube_url,
                    out_dir,
                    audio_filename,
                    video_filename,
                    res='360p',
                    abr='128kbps',
                    subtype='mp4'):
    """
    Download audio and video from a requested YouTube object.
    Audio and video are downloaded separately and stored in separate folders.

    Input:
      youtube_url:       url address of requested YouTube video
      out_dir:           parent directory where audio and video files will be stored
      audio_name:        output audio name
      video_name:        output video name
      res, abr, subtype: arguments of `get_audio_itag()` and `get_video_itag()` functions
    Output:
      None
    """
    yt_obj = pytube.YouTube(youtube_url)  # YouTube object
    streams = yt_obj.streams.all()  # list of available media formats
    # [a] video
    # create path
    path_name = os.path.join(out_dir, 'video')
    os.makedirs(path_name, mode=0o777, exist_ok=True)
    # get `itag`
    video_itag = get_video_itag(stream_lst=streams, res=res, subtype=subtype)
    # download video
    yt_obj.streams.get_by_itag(video_itag).download(output_path=path_name, filename=video_filename,
                                                    filename_prefix=None)
    # [b] audio
    # create path
    path_name = os.path.join(out_dir, 'audio_mp4')
    os.makedirs(path_name, mode=0o777, exist_ok=True)
    # get `itag`
    audio_itag = get_audio_itag(stream_lst=streams, abr=abr, subtype='mp4')
    # download audio
    yt_obj.streams.get_by_itag(audio_itag).download(output_path=path_name, filename=audio_filename,
                                                    filename_prefix=None)


# RUN
# URL0 = 'https://www.youtube.com/watch?v=OJ_qg23orFM'
# download_medium(youtube_url=URL0, out_dir='./', audio_filename='audio_0', video_filename='video_0',
#                res='360p', abr='128kbps', subtype='mp4')

# URL1 = 'https://www.youtube.com/watch?v=2Hc2_jY4KhY'
# download_medium(youtube_url=URL1, out_dir='./', audio_filename='audio_1', video_filename='video_1',
#                res='360p', abr='128kbps', subtype='mp4')

##########
# TO WAV #
##########

def to_wav(audio_path):
    """
    Convert an audio track to a `.wav` file
    Converted audio file is stored in './data/audio_wav/audio_fn.wav'
    (Essentially replace 'mp4' by 'wav' in the `audio_path`)

    Input:
      audio_path: path to the audio track, e.g., './data/audio_mp4/audio_fn.mp4'

    Output:
      None
    """
    inp = audio_path
    oup = inp.replace('mp4', 'wav')

    dir_ = oup.rpartition('/')
    dir_ = dir_[0]
    os.makedirs(dir_, mode=0o777, exist_ok=True)

    ff = ffmpy.FFmpeg(inputs={inp: None}, outputs={oup: None})
    # print(f.cmd)
    ff.run()

# RUN
# to_wav('./audio_mp4/audio_0.mp4')
# to_wav('./audio_mp4/audio_1.mp4')
# to_wav('./audio_mp4/audio_2.mp4')
# to_wav('./audio_mp4/audio_3.mp4')
# to_wav('./audio_mp4/audio_4.mp4')
# to_wav('./audio_mp4/audio_5.mp4')
# to_wav('./audio_mp4/audio_6.mp4')
# to_wav('./audio_mp4/audio_7.mp4')


#########################
# AUDIO & VIDEO MERGING #
#########################

def av_merge(audio_path='./data/audio_mp4',
             video_path='./data/video',
             media_path='./data/media'):
    """
    Merges a video file with its associated audio file creating a single medium
    The medium is stored in `media_path`

    Input:
      audio_path: path to audio files
      video_path: path to video files
      media_path: path to media (video with audio)
    Output:
      None
    """
    # [1] match associated audio and video
    # e.g. audio_k is matched with video_k

    audio_files = os.listdir(audio_path)
    video_files = os.listdir(video_path)

    matched_pairs = [(video_name, audio_name)
                     for video_name in video_files for audio_name in audio_files
                     if video_name.split('.')[0].split('_')[-1] == audio_name.split('.')[0].split('_')[-1]]

    print(matched_pairs)

    # [2] preparing the output folder and merging audio and video into a single medium

    path_name = os.path.join(media_path, '')
    os.makedirs(path_name, mode=0o777, exist_ok=True)

    for idx in range(len(matched_pairs)):
        video = os.path.join(video_path, matched_pairs[idx][0])
        audio = os.path.join(audio_path, matched_pairs[idx][1])
        output_name = 'medium_' + str(idx) + '.mp4'
        output = os.path.join(path_name, output_name)

        inp = {audio: None, video: None}
        oup = {output: ['-c', 'copy']}

        ff = ffmpy.FFmpeg(inputs=inp, outputs=oup)
        # print(ff.cmd)
        ff.run()


# RUN
# av_merge(audio_path='./audio_mp4', video_path='./video', media_path='./media')