import argparse
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

data_path = 'data'
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
    if args.a == 'eval_train':
        print("Action selected: [Training evaluation]")
    if args.a == 'train':
        print("Action selected: [Model training]")
    elif args.a == 'eval_target':
        print("Action selected: [Target evaluation]")

    #################################
    # FEATURE EXTRACTION            #
    #################################
    
    # Read input video(s), and perform segmantation based on silence points
    seg.input2seg(audio_dir=data_path+'/target/audio/', video_dir=data_path+'/target/', output_folder=data_path+'/target/video/')
    print('Segmentation is done.')

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
        # TODO: Load trained model
        # acc = cl.evaluate_target(df)
        ls.df2summary(df=df, folderDATA=data_path ,col_cl='CLASS_1', label=['boring','interesting','neutral'], prc_l=[0.30,0.35,0.35], col_d='DURATION', duration_sec=90, output_folder=data_path, output_name='summary.mp4')
        pass

    #################################
    # RESULTS                       #
    #################################

    # Print results (only in evaluation cases)
    if args.a == 'eval_train':
        print("Accuracy: " + str(acc))



if __name__ == "__main__":
    # execute only if run as a script
    main()
