import pandas as pd

def merge_features(video_df, audio_df, data_dir='data'):
    '''
    Merging the video & audio dataframe into one single dataframe to be ready for training.

    :param video_df: the video features dataframe
    :param audio_df: the audio features dataframe
    :return: the merged features dataframe
    '''

    # Merge (join) dataframes
    df = pd.merge(video_df, audio_df, on=['FILE', 'SEG', 'CLASS_1'], how='inner', suffixes=['_v', '_a'])

    # Save merged features dataframe
    df.to_pickle(data_dir + '/' + 'Features.pkl')

    return df


