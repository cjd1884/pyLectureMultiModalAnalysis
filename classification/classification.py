from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn import preprocessing as pp
import pandas as pd
import statistics as st
import pickle

# Dataframe Columns
c_file = 'FILE'
c_drop = ['FILE', 'SEG']
c_label = 'CLASS_1'

# Model default name
model_name ='svm_model.sav'

def save_model(model, data_dir='data'):
    '''
    Merely saves the provided ML model to a pickle file.
    
    :param model:       the trained model 
    :param data_dir:    the data directory
    '''

    filename = data_dir + '/' + model_name
    pickle.dump(model, open(filename, 'wb'))

    print('SVM model saved in "' + filename + '"')


def load_model(data_dir='data'):
    '''
    
    :param data_dir: 
    :return:            the loaded model 
    '''
    filename = data_dir + '/' + model_name
    model = pickle.load(open(filename, 'rb'))

    print('SVM model successfully loaded.')

    return model


def evaluate_training(df):
    '''
    Evaluates the algorithm performance on learning the provided
    dataset. Run in rounds - each speaker versus all

    :param df:          the dataframe with audio & video data

    '''

    # Standardize dataframe
    df = standardize(df)

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


def train(df, data_dir='data'):
    '''
    Trains an SVM model in the provided dataset.

    :param df:          the dataframe with audio & video data
    :param data_dir:    the data directory
    :return:            the trained model
    '''

    # Standardize dataframe
    df = standardize(df)

    # Get train data (features and labels)
    train = df.drop(c_drop, axis=1)
    train_Y = train[c_label]
    train_X = train[train.columns[1:]]

    # Create the model
    model = SVC(kernel='rbf')

    # Fit
    model.fit(train_X, train_Y)

    print('SVM model trained.')

    # Save model
    save_model(model, data_dir)

    return model


def evaluate_target(model, target_df):

    # Standardize dataframe
    df = standardize(target_df)

    # Predict
    pred_Y = model.predict(test_X)

    # Evaluate and append
    acc = accuracy_score(test_Y, pred_Y)



def split_train_test(df, speaker):
    '''
    Splits the provided dataframe (audio & video fetures with
    speakers and labels) to train and test based on speaker 
    (one vs all).

    :param df:          the dataframe with audio & video data
    :param speaker:     the speaker for the 1 vs all

    '''

    # Train
    train = df[df[c_file] != speaker].drop(c_drop, axis=1)
    train_Y = train[c_label]
    train_X = train[train.columns[1:]]

    # Test
    test = df[df[c_file] == speaker].drop(c_drop, axis=1)
    test_Y = test[c_label]
    test_X = test[test.columns[1:]]

    return train_X, train_Y, test_X, test_Y


def standardize(df):
    '''
    Standardizes the provided dataframe.

    :param df:  the input dataframe 
    :return:    the standardized dataframe
    '''

    # Get only float columns (containing data)
    float_columns = df.select_dtypes(include=['float64']).columns.to_list()
    string_columns = df.select_dtypes(exclude=['float64']).columns.to_list()

    # Create the Scaler object
    scaler = pp.StandardScaler()

    # Fit your data on the scaler object
    scaled_df = scaler.fit_transform(df[float_columns])
    scaled_df = pd.DataFrame(scaled_df, columns=float_columns)

    # Concat with non float columns (removed before standardization)
    scaled_df = pd.concat([df[string_columns], scaled_df], axis=1, join='inner')

    return scaled_df