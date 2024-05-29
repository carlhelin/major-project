import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories
DATA_DIR = 'benchmark data'

# Directories inside Data
DIRTY_DIR = 'dirty'
STRUCTURED_DIR = 'structured'
TEXTUAL_DIR = 'textual'

# Datasets folders
DBLP_ACM_DIR = 'DBLP-ACM'
DBLP_GOOGLESCHOLAR_DIR = 'DBLP-GoogleScholar'
ITUNES_AMAZON_DIR = 'iTunes-Amazon'
WALMART_AMAZON_DIR = 'Walmart-Amazon'
AMAZON_GOOGLE_DIR = 'Amazon-Google'
BEER_DIR = 'Beer'
FODORS_ZAGATS_DIR = 'Fodors-Zagats'
ABT_BUY_DIR = 'Abt-Buy'

# Datasets rows
DBLP_ACM_DIR_ROW = 'id,title,authors,venue,year'
DBLP_GOOGLESCHOLAR_DIR_ROW = 'id,title,authors,venue,year'
ITUNES_AMAZON_DIR_ROW = 'id,Song_Name,Artist_Name,Album_Name,Genre,Price,CopyRight,Time,Released'
WALMART_AMAZON_DIR_ROW = 'id,title,category,brand,modelno,price'
AMAZON_GOOGLE_DIR_ROW = 'id,title,manufacturer,price'
BEER_DIR_ROW = 'id,Beer_Name,Brew_Factory_Name,Style,ABV'
FODORS_ZAGATS_DIR_ROW = 'id,name,addr,city,phone,type,class'
ABT_BUY_DIR_ROW = 'id,name,description,price'

# General files for all datasets folders
TABLE_A = 'tableA.csv'
TABLE_B = 'tableB.csv'
TEST = 'test.csv'
TRAINING = 'train.csv'
VALIDATION = 'valid.csv'
   
def get_base_dir():
    """
    Returns the base directory.
    """
    return BASE_DIR

def get_data_dir():
    """
    Returns the path to the data directory.
    """
    return os.path.join(get_base_dir(), DATA_DIR)

def get_dataset_dir(dataset_type, dataset_name):
    """
    Returns the path to a specific dataset directory.
    """
    return os.path.join(get_data_dir(), dataset_type, dataset_name)

def get_file_path(dataset_type, dataset_name, file_name):
    """
    Returns the path to a specific file in a specific dataset directory.
    """
    return os.path.join(get_dataset_dir(dataset_type, dataset_name), file_name)

def get_table_a_path(dataset_type, dataset_name):
    """
    Returns the path to the table A file in a specific dataset directory.
    """
    return get_file_path(dataset_type, dataset_name, TABLE_A)

def get_table_b_path(dataset_type, dataset_name):
    """
    Returns the path to the table B file in a specific dataset directory.
    """
    return get_file_path(dataset_type, dataset_name, TABLE_B)

def get_test_path(dataset_type, dataset_name):
    """
    Returns the path to the test file in a specific dataset directory.
    """
    return get_file_path(dataset_type, dataset_name, TEST)

def get_training_path(dataset_type, dataset_name):
    """
    Returns the path to the training file in a specific dataset directory.
    """
    return get_file_path(dataset_type, dataset_name, TRAINING)

def get_validation_path(dataset_type, dataset_name):
    """
    Returns the path to the validation file in a specific dataset directory.
    """
    return get_file_path(dataset_type, dataset_name, VALIDATION)

def load_datasets(dataset_type, dataset_name):
    """
    Load train, validation, and test datasets from the given directory path.
    """
    train = pd.read_csv(get_training_path(dataset_type, dataset_name))
    valid = pd.read_csv(get_validation_path(dataset_type, dataset_name))
    test = pd.read_csv(get_test_path(dataset_type, dataset_name))
    return train, valid, test

def tableA_tableB(dataset_type, dataset_name):
    """
    Load table A and table B from the given directory path.
    """
    table_A = pd.read_csv(get_table_a_path(dataset_type, dataset_name))
    table_B = pd.read_csv(get_table_b_path(dataset_type, dataset_name))
    return table_A, table_B
    