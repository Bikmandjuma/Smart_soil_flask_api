import pandas as pd

def dataset():
    return pd.read_csv('Crop_data/dataset/Crop_recommendation.csv')
    # return pd.read_csv('Crop_data/dataset/Plant_Parameters.csv')

# import pandas as pd

# class Dataset:
#     def __init__(self):

#         self.data = pd.read_csv("Crop_data/dataset/Crop_recommendation.csv")

#     def get_data(self):
#         return self.data
