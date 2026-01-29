import pandas as pd
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import re
import numpy as np

def save_gpu(source_file, new_file, QUERY='div.center tbody tr', FIELD_QUERY='td', column_names=['video_card_name', 'pasmark_gd3_mark', 'rank', 'videocard_value', 'price_usd']):
    '''
    Docstring for save_gpu
    
    :param source_file: the html file that contains all gpu's in html format
    :param new_file: the name of resulting csv file to be created
    :param QUERY: a query to get all rows in a data_frame
    :param FIELD_QUERY: a query to get each column in the row of the data frame
    '''
    column_length = len(column_names)

    # read the file
    data = ''
    with open(source_file, 'r') as file:
        data = file.read()

    # create the html parser
    document = bs(data, features='html.parser')
    elements = document.select(QUERY)

    # start building a dataframe as a list of lists
    dataframe = [[] for i in range(column_length)]
    for element in elements:
        fields = element.select(FIELD_QUERY)
        i = 0
        for field in fields:
            dataframe[i].append(field.text)
            i += 1
    
    # make the data frame panda format!
    c = {}
    i = 0
    for column in column_names:
        c[column] = dataframe[i]
        i += 1

    df = pd.DataFrame(c)
    df.to_csv(new_file)


def plot_distributions(df, bin_number = 50):
    '''
    plot the distributions of all the columns

    :param df: dataframe of housing price per block (given longitude and latitude) features to be plotted with a histogram
    '''
    for column_name in df.columns:
        if pd.api.types.is_numeric_dtype(df[column_name].dtype) and column_name != "rank" and column_name != "Unnamed: 0":
            df[df[column_name].notna()][column_name].hist(bins=bin_number)
            plt.ylabel(f"count")
            plt.xlabel(f"{column_name}")
            plt.title(f"{column_name} distribution (bin size = 50)")
            plt.savefig(f"plot/distributions/{column_name}.png")
            plt.clf() # clear the plot


def preprocesss(csv = 'gpu.csv'):
    '''
    return a clead version of the data set by making numeric numerics and ect
    '''
    def make_num(element):
        '''
        if not null convert element to a float
        
        :param element: either null or a string and hs format "$888.88*"
        '''
        if type(element) == type(''):
            digits = re.findall(r'\d+', element)
            num = float(digits[0]) + float(digits[1]) * .01
            return num
        
        return element

    df = pd.read_csv(csv)
    df['price_usd'] = df['price_usd'].apply(make_num)

    return df


def plot_background(df):
    '''
    plot basic data including possible correlations and general distributions
    
    :param df: Description
    '''
    plot_distributions(df)
    print(df[df['price_usd'].notna()])
    fig, ax = plt.subplots()



def main():
    '''
    main method to run operations
    '''
    df = preprocesss()
    plot_background(df)
    # save_gpu(source_file='gpu.html', new_file='gpu.csv')



if __name__ == '__main__':
    main()