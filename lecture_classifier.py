import argparse
import pandas as pd
import classification.classification as cl

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
        print("Training evaluation action selected.")
    if args.a == 'train':
        print("Model training action selected.")
    elif args.a == 'eval_target':
        print("Target evaluation action selected.")

    #################################
    # FEATURE EXTRACTION            #
    #################################

    # TODO: Extract audio features

    # TODO: Extract video features

    # TODO: Combine features



    #################################
    # MODEL TRAINING/EVALUATION     #
    #################################

    # Load Data
    df = pd.read_pickle("data/Video2Features.pkl")

    # Train or evaluate model
    if args.a == 'eval_train':
        acc = cl.evaluate_training(df)
    elif args.a == 'train':
        # cl.train(df)
        # TODO: Save trained model
        pass
    elif args.a == 'eval_target':
        # TODO: Load trained model
        # acc = cl.evaluate_target(df)
        pass

    #################################
    # RESULTS                       #
    #################################

    # Print results (only in evaluation cases)
    if args.a != 'train':
        print("Accuracy: " + str(acc))



if __name__ == "__main__":
    # execute only if run as a script
    main()