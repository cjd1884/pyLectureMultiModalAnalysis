'''
Short description: Leveraging on `pytube`, this script downloads and stores locally
 the audio and video files associated with a YouTube object.
 Audio and video files are stored in seperate folders.
 '''

import pytube
import os

def get_audio_itag(stream_lst,
                   abr,
                   subtype='mp4'):
    '''Return the `itag` of a YouTube video with specified audio bitrate (`abr`) and subtype.
    If the desired `arb` does not exist, the user is prompt to input a new one from a list.

    Input:
      stream_lst:  list of available media formats
      abr:         desired bit rate, string of the form `xxxkpbs`, where `x` is a number
      subtype:     desired subtype, string -- available options are `mp4` (default) and `webm`
    Output:
      `itag` of YouTube object
    '''
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
                   res,
                   subtype='mp4'):
    '''Return the `itag` of a YouTube video with specified resolution and subtype.
    If the desired resolution does not exist, the user is prompt to input a new one from a list.

    Input:
      stream_lst:  a list of available media formats
      res:         desired resolution, string of the form `xxxp`, where `x` is a number
      subtype:     desired subtype, string -- available options are `mp4` (default) and `webm`
    Output:
      `itag` of YouTube video
    '''
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
                    res,
                    abr,
                    subtype='mp4'):
    '''Download audio and video from a requested YouTube object.
    Audio and video are downloaded seperately and stored in seperate folders.

    Input:
      youtube_url:       url address of requested YouTube video
      out_dir:           parent directory where audio and video files will be stored
      audio_name:        output audio name
      video_name:        output video name
      res, abr, subtype: arguments of `get_audio_itag` and `get_video_itag` functions
    Output:
      None
    '''
    yt_obj = pytube.YouTube(youtube_url)  # YouTube object
    streams = yt_obj.streams.all()        # list of available media formats
    # [a] video
    # create path
    path_name = os.path.join(out_dir, 'video')
    os.makedirs(path_name, mode=0o777, exist_ok=True)
    # get `itag`
    video_itag = get_video_itag(stream_lst=streams, res=res, subtype='mp4')
    # download video
    yt_obj.streams.get_by_itag(video_itag).download(output_path=path_name, filename=video_filename,
                                                    filename_prefix=None)
    # [b] audio
    # create path
    path_name = os.path.join(out_dir, 'audio')
    os.makedirs(path_name, mode=0o777, exist_ok=True)
    # get `itag`
    audio_itag = get_audio_itag(stream_lst=streams, abr=abr, subtype='mp4')
    # download audio
    yt_obj.streams.get_by_itag(audio_itag).download(output_path=path_name, filename=audio_filename,
                                                    filename_prefix=None)


def main(doc_path,
        out_dir,
        res='360p',
        abr='128kpbs',
        subtype='mp4'
        ):
    '''Download audio and video from a YouTube object; url addresses are provided by a text file

    Input:
      doc_path:          text file containg url addresses--each line is a single address
      out_dir:           parent directory where audio and video files will be stored
      res, abr, subtype: see `get_audio_itag` and `get_video_itag` functions
    Output
      None
    '''
    with open(doc_path, 'r') as f:
        yt_urls = f.read().splitlines()

    # print(yt_urls)

    for idx, url in enumerate(yt_urls):
        audio_name = 'audio_' + str(idx)
        video_name = 'video_' + str(idx)
        download_medium(youtube_url=url, out_dir=out_dir, audio_filename=audio_name, video_filename=video_name,
                       res='360p', abr='128kbps', subtype='mp4')

if __name__=='__main__':
    # test run with dummy dataset
    main(doc_path='./yt_dummy.txt',
        out_dir='./data')