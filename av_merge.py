'''
Short description: Script for merging associated video and audio files into a single medium using FFMPEG.
 It expects that audio files are stored as `in_dir/audio/audio_k.mp4`
 (and similarly for video) and stores the newly created file as `out_dir/media/medium_k.mp4`
'''

import ffmpy
import os

def main(in_dir='./data',
         out_dir='./data'):
    '''
    Merges a video file with its associated audio file creating a single medium, which it is
    stored in a directory `out_dir/media/`

    Input:
      in_dir:  the directory containing the `audio` and `video` folders
      out_dir: the directory containing the `media` folder where the merged media will be stored
    Output:
      None
    '''
    # [1] match associated audio and video
    # e.g. audio_k is matched with video_k

    audio_path = os.path.join(in_dir, 'audio', '')
    video_path = os.path.join(in_dir, 'video', '')

    audio_files = os.listdir(audio_path)
    video_files = os.listdir(video_path)

    matched_pairs = [(video_name, audio_name)
                     for video_name in video_files for audio_name in audio_files
                     if video_name.split('.')[0].split('_')[-1] ==
                     audio_name.split('.')[0].split('_')[-1]]

    print(matched_pairs)

    # [2] preparing the output folder and merging audio and video into a single medium

    path_name = os.path.join(out_dir, 'media', '')
    os.makedirs(path_name, mode=0o777, exist_ok=True)

    for idx in range(len(matched_pairs)):
        video = os.path.join(in_dir, 'video', matched_pairs[idx][0])
        audio = os.path.join(in_dir, 'audio', matched_pairs[idx][1])
        output_name = 'medium_' + str(idx) + '.mp4'
        output = os.path.join(path_name, output_name)

        inp = {audio: None, video: None}
        oup = {output: ['-c', 'copy']}

        ff = ffmpy.FFmpeg(inputs=inp, outputs=oup)
        # print(ff.cmd)
        ff.run()

if __name__=='__main__':
    main()