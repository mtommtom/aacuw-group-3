import pandas as pd
from bs4 import BeautifulSoup as bs

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


def main():
    '''
    main method to run operations
    '''
    save_gpu(source_file='gpu.html', new_file='gpu.csv')


if __name__ == '__main__':
    main()