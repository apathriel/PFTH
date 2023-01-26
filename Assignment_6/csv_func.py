import pandas as pd

def pruning_csv(dataset, data_format, columns_to_tokenize=[], remove_punctuation=True):
    """
    Returns trimmed / modified pandas df, df is modified based on parameters, non-destructrive change.

        Parameters:
                dataset(str): Name of dataset file
                data_format(str): Format of dataset file
                columns_to_tokenize(list): Specifies which columns to tokenize
                remove_punctuation(bool): Specifies whether to remove punctuation from ['desc'] column. (specific to goodreads dataset)
    """
    df = pd.read_csv(f'data/{dataset}.{data_format}')

    # drop row if cell empty in 'genre' or 'desc'
    df = drop_row_by_empty_cell(df=df, columns=['genre', 'desc'])

    # make strings from csv cells pertaining to 'genre' and 'desc' columns lowercase
    df['genre'] = df['genre'].str.lower()
    df['desc'] = df['desc'].str.lower()

     # fix encoding error for terminal visualization
    df['desc'].replace({"â€™": "'"}, regex=True, inplace=True)
    
    # tokenize genres in given column
    for item in columns_to_tokenize:
        df[item['column']] = df[item['column']].str.split(pat=item['split'])

    # remove punctuation from desc for nlp
    if remove_punctuation:
        df['desc'] = df['desc'].str.replace(r'[^\w\s]+', '', regex=True)

    print(f'[INFO] {dataset}.{data_format} was succesfully pruned.')

    return df

def drop_row_by_empty_cell(df, columns):
    """Returns pandas df with rows dropped based on empty cells in specificed columns."""
    for column in columns:
        df = df.drop(df[df[column].isnull()].index)
    return df

def drop_row_by_value_count(df, column, drop_count):
    """Gets value counts for given, and returns df with only rows within the given threshhold"""
    counts = df[column].value_counts()
    return df.loc[df[column].isin(counts.index[counts > drop_count])]

def get_column_values(df, column):
    """Returns list of values for given column"""
    return list(set(df[column].values))
    
def get_only_first_element_from_list(df, column):
    """Returns pandas df with specified column (dtype list) only containing the first list item."""
    return df[column].apply(lambda x: x[0])

def get_corpus_from_column(df, column):
    """Returns all values of specified column."""
    return df[column].values  

def get_corpus_from_genre_index(df, genre, column):
    """Returns corpus from dataframed located by mask (bool array)."""
    mask = df['genre'].apply(lambda x: genre in x)
    corpus = df[column].loc[mask].values
    return corpus

def create_underscore_string(str):
    """Returns copy of string with all with spaces replaced with underscores."""
    return str.lower().replace(' ', '_')