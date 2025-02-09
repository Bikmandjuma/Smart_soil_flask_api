import pandas as pd

# Define the function that returns the dataset
def dataset():
    return pd.read_csv('dataset/Crop_recommendation.csv')
    # return pd.read_csv('dataset/Plant_Parameters.csv')