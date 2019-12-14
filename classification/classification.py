from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import statistics as st


def evaluate_training(df):
    '''
    Evaluates the algorithm performance on learning the provided
    dataset. Run in rounds - each speaker versus all

    :param df:          dataframe with audio & video data

    '''
    # Unique speakers
    speakers = df['FILE'].unique()

    # Array to hold model accuracy for each round
    acc_array = []

    for speaker in speakers:
        # Split dataframe to train-test based on current speaker
        train_X, train_Y, test_X, test_Y = split_train_test(df, speaker)

        # Create the model
        model = SVC(kernel='rbf')

        # Fit
        model.fit(train_X, train_Y)

        # Predict
        pred_Y = model.predict(test_X)

        # Evaluate and append
        acc_array.append(accuracy_score(test_Y, pred_Y))

    return st.mean(acc_array)


def split_train_test(df, speaker):
    '''
    Splits the provided dataframe (audio & video fetures with
    speakers and labels) to train and test based on speaker 
    (one vs all).

    :param df:          dataframe with audio & video data
    :param speaker:     speaker for the 1 vs all

    '''

    # Dataframe Columns
    c_file = 'FILE'
    c_drop = ['FILE', 'SEG']
    c_label = 'CLASS_1'

    # Train
    train = df[df[c_file] != speaker].drop(c_drop, axis=1)
    train_Y = train[c_label]
    train_X = train[train.columns[1:]]

    # Test
    test = df[df[c_file] == speaker].drop(c_drop, axis=1)
    test_Y = test[c_label]
    test_X = test[test.columns[1:]]

    return train_X, train_Y, test_X, test_Y
