import argparse
import os
import os.path as path
import pandas as pd
import classification.classification as cl
import audio.audio_features as af
import Video2Features.Video2Features as vf
import helpers.helpers as helpers
import Labels2Summary.Labels2Summary as ls
import helpers.av_segmentation as seg


import matplotlib
matplotlib.use('TkAgg')

data_path_source = 'data'
# data_path_target = 'data/target'
# data_path_target = 'data/target_1m'
data_path_target = 'data/target_5m'

features_audio_file = 'Audio2Features.pkl'
features_video_file = 'Video2Features.pkl'

def main():
    '''
    Main method. Lecture classifier is going to be used for the following:
        - Training evaluation: Accuracy is calculated using leave-one-video-out cross 
         validation (different video is same as different speaker - we assume one video
         per speaker).
        - Training: Model is trained on the entire dataset and is saved on disk.
        - Target evaluation: The trained model (loaded from disk) is used to evaluate 
         external dataset.
    
    Annotated datasets are assumed to be available in 'data' folder.    
    '''

    #################################
    # PROGRAM INPUT                 #
    #################################

    # Parser
    parser = argparse.ArgumentParser(description = "Lecture Classifier v0.1")
    parser.add_argument('-a', choices=['eval_train', 'train', 'eval_target'], required=False, help='Select action. Available: Training evaluation, Model training, Target evaluation', default='eval_train')

    # Parameters
    args = parser.parse_args()
    print("=================================")
    if args.a == 'eval_train':
        print("    [TRAINING-EVALUATION MODE]")
        data_path = data_path_source
    if args.a == 'train':
        print("    [MODEL TRAINING MODE]")
        data_path = data_path_source
    elif args.a == 'eval_target':
        print("    [TARGET EVALUATION MODE]")
        data_path = data_path_target
    print("=================================")


    #################################
    # SEGMENTATION - ONLY TARGET    #
    #################################

    # Make video segmentation based on silence
    if args.a == 'eval_target':
        seg.input2seg(audio_dir=data_path + '/audio/', video_dir=data_path, output_folder=data_path + '/video/')
        print('Target video segmentation is complete.')


    #################################
    # FEATURE EXTRACTION            #
    #################################

    # Extract video features (if not already extracted)
    if not path.exists(data_path + '/' + features_video_file):
        vf.Video2feature(pathIn=data_path+'/', frameRate=4, save=True, trainmode=False)
    video_df = pd.read_pickle(data_path + '/' + features_video_file)
    print('Video features loaded.')

    # Extract audio features (if not already extracted)
    if not path.exists(data_path + '/' + features_audio_file):
        af.audio_features_extraction(dir_name=data_path, features_audio_file=features_audio_file)
    audio_df = pd.read_pickle(data_path + '/' + features_audio_file)
    print('Audio features loaded.')

    # Combine features
    df = helpers.merge_features(video_df, audio_df, data_path)
    print('Video and audio features merged successfully.')


    #################################
    # MODEL TRAINING/EVALUATION     #
    #################################

    # Train or evaluate model
    if args.a == 'eval_train':
        print('Evaluation started.')
        acc = cl.evaluate_training(df)
        print('Evaluation completed.')
    elif args.a == 'train':
        cl.train(df)
    elif args.a == 'eval_target':
        fit_model = cl.load_model(data_path)
        final_df = cl.evaluate_target(fit_model, df)
        print('Video prediction complete. Summarization process should follow.')


    #################################
    # RESULTS - ONLY IN EVALUATION  #
    #################################

    # Print results (only in evaluation cases)
    if args.a == 'eval_train':
        print("Accuracy: " + str(acc))


    #################################
    # RESULTS - TARGET EVALUATION   #
    #################################

    # Make the summarisation video
    if args.a == 'eval_target':
        ls.df2summary(df=final_df, folderDATA=data_path+'/' ,col_cl='CLASS_1', label=['boring','interesting','neutral'], prc_l=[0.30,0.34,0.36], col_d='DURATION', duration_sec=90, output_folder=data_path, output_name='summary.mp4')



if __name__ == "__main__":
    # execute only if run as a script
    main()
