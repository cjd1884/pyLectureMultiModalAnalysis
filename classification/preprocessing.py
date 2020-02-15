from sklearn import preprocessing as pp
import pandas as pd

def do_preprocessing(df, categorical_columns=None):

    df = standardize(df)

    if categorical_columns is not None:
        df = categorical_2_numeric(df, categorical_columns)

    return df


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


def categorical_2_numeric(df, columns):
    '''
    Converts dataframe category columns to numeric. Currently used only for label column.

    :param df:          the input dataframe
    :param columns:     the columns to be changed to numeric
    :return:            the dataframe with numeric columns (previous were objects)
    '''

    # Update column data types to categorical (previous was object)
    df[columns] = df[columns].astype('category')

    # Select categorical columns
    cat_columns = df.select_dtypes(['category']).columns

    # Convert them to numeric
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

    return df