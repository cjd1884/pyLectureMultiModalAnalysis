from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
from .preprocessing import do_preprocessing
import statistics as st
import pickle

# Dataframe Columns
c_file = 'FILE'
c_drop = ['FILE', 'SEG']
c_label = 'CLASS_1'

# Model default name
model_name ='svm_model.sav'

#############################
# CLASSIFICATION METHODS    #
#############################

def evaluate_training(df):
    '''
    Evaluates the algorithm performance on learning the provided
    dataset. Run in rounds - each speaker versus all

    :param df:          the dataframe with audio & video data

    '''

    # Preprocessing (standardisation and conversion of categorical values to numeric)
    df = do_preprocessing(df)

    # Unique speakers
    speakers = df['FILE'].unique()

    # Array to hold model accuracy for each round
    acc_array = []

    print('---------------------------')
    print('    Confusion matrices     ')
    print('---------------------------')
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

        # Print confusion matrix
        cf = confusion_matrix(y_pred=pred_Y, y_true=test_Y, labels=['boring', 'neutral', 'interesting'])
        print('Speaker: ' + speaker)
        print('---------------------------')
        print(cf)

    return st.mean(acc_array)


def train(df, data_dir='data'):
    '''
    Trains an SVM model in the provided dataset.

    :param df:          the dataframe with audio & video data
    :param data_dir:    the data directory
    :return:            the trained model
    '''

    # Preprocessing (standardisation and conversion of categorical values to numeric)
    df = do_preprocessing(df)

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

    # Preprocessing (standardisation and conversion of categorical values to numeric)
    df = do_preprocessing(target_df)

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


#############################
# SAVE/LOAD MODEL METHODS   #
#############################

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