# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from dataset import dataset

# # Load the data using the dataset function
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
# y = data['label']

# # Split the data into training and testing sets
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (these are the input values for which you want the prediction)
# new_data = pd.DataFrame({
#     'N': [20],
#     'P': [32],
#     'K': [53],
#     'temperature': [20.8],
#     'humidity': [82.0],
#     'ph': [6.5],
#     'rainfall': [150.9]
# })

# # Make a prediction for the new data
# predicted_crop = model.predict(new_data)

# # Display the predicted crop
# print(f"The predicted crop for the given conditions is: {predicted_crop[0]}")

#=============================================================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from dataset import dataset

# # Load the data using the dataset function
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
# y = data['label']

# # Split the data into training and testing sets
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (these are the input values for which you want the prediction)
# new_data = pd.DataFrame({
#     'N': [20],
#     'P': [32],
#     'K': [53],
#     'temperature': [20.8],
#     'humidity': [82.0],
#     'ph': [6.5],
#     'rainfall': [150.9]
# })

# # Get the predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Display the predicted probabilities for each crop
# print(f"Predicted probabilities for each crop:\n{predictions_df}")

# # Get the top 3 most likely crops based on the predicted probabilities
# top_crops = predictions_df.T.sort_values(by=0, ascending=False).head(3)
# print(f"\nTop 3 predicted crops for the given conditions:\n{top_crops}")

# # Optionally, you can display the most probable crop:
# most_probable_crop = predictions_df.idxmax(axis=1)
# print(f"\nThe most probable crop for the given conditions is: {most_probable_crop[0]}")

#======================================================================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from dataset import dataset  # Assuming your dataset function is in the "dataset.py" file

# # Load the data using the dataset function
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['pH', 'Soil EC', 'Phosphorus', 'Potassium', 'Urea', 'T.S.P', 'M.O.P', 'Moisture', 'Temperature']]
# y = data['Plant Type']

# # Split the data into training and testing sets
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (new soil conditions)
# new_data = pd.DataFrame({
#     'pH': [6.5],  # example pH value
#     'Soil EC': [0.3],  # example soil electrical conductivity
#     'Phosphorus': [12.5],  # example phosphorus content
#     'Potassium': [150],  # example potassium content
#     'Urea': [45],  # example urea value
#     'T.S.P': [18],  # example TSP value
#     'M.O.P': [22],  # example MOP value
#     'Moisture': [75],  # example moisture level
#     'Temperature': [52]  # example temperature
# })

# # Get the predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Display the predicted probabilities for each crop
# print(f"Predicted probabilities for each crop:\n{predictions_df}")

# # Get the top 3 most likely crops based on the predicted probabilities
# top_crops = predictions_df.T.sort_values(by=0, ascending=False).head(3)
# print(f"\nTop 3 predicted crops for the given conditions:\n{top_crops}")

# # Optionally, you can display the most probable crop:
# most_probable_crop = predictions_df.idxmax(axis=1)
# print(f"\nThe most probable crop for the given conditions is: {most_probable_crop[0]}")

#=================================================================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from dataset import dataset  # Assuming your dataset function is in the "dataset.py" file

# # Load the data using the dataset function
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['pH', 'Soil EC', 'Phosphorus', 'Potassium', 'Urea', 'T.S.P', 'M.O.P', 'Moisture', 'Temperature']]
# y = data['Plant Type']

# # Split the data into training and testing sets
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (new soil conditions)
# new_data = pd.DataFrame({
#     'pH': [3.5],  # example pH value
#     'Soil EC': [0.1],  # example soil electrical conductivity
#     'Phosphorus': [5.5],  # example phosphorus content
#     'Potassium': [200],  # example potassium content
#     'Urea': [35],  # example urea value
#     'T.S.P': [28],  # example TSP value
#     'M.O.P': [20],  # example MOP value
#     'Moisture': [75],  # example moisture level
#     'Temperature': [52]  # example temperature
# })

# # Get the predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Display the predicted probabilities for each crop
# print(f"Predicted probabilities for each crop:\n{predictions_df}")

# # Define how many top crops you want to predict, e.g., top 3, top 4, etc.
# top_n = 3  # Change this to the number of top crops you want (1, 2, 3, 4, 5, etc.)

# # Get the top N most likely crops based on the predicted probabilities
# top_crops = predictions_df.T.sort_values(by=0, ascending=False).head(top_n)
# print(f"\nTop {top_n} predicted crops for the given conditions:\n{top_crops}")

# # Optionally, you can display the most probable crop:
# most_probable_crop = predictions_df.idxmax(axis=1)
# print(f"\nThe most probable crop for the given conditions is: {most_probable_crop[0]}")


#============================================================================================

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from dataset import dataset  # Assuming your dataset is being loaded via this function

# Load the dataset
data = dataset()

# Prepare feature columns (X) and target column (y)
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]  # Update with correct column names
y = data['label']  # Crop label (target column)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the RandomForestClassifier model
model = RandomForestClassifier(random_state=0)
model.fit(X_train, y_train)

# Define the new data for prediction (environmental conditions for prediction)
new_data = pd.DataFrame({
    'N': [30],
    'P': [22],
    'K': [33],
    'temperature': [10.8],
    'humidity': [62.0],
    'ph': [3.5],
    'rainfall': [200.9]
})

# Get predicted probabilities for each crop
predicted_probabilities = model.predict_proba(new_data)

# Create a DataFrame with the predicted probabilities for each crop
predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# Display the predicted probabilities for each crop
print(f"Predicted probabilities for each crop:\n{predictions_df}\n")

# Function to get top N crops based on predicted probabilities
def get_top_crops(predictions_df, top_n=3):
    # Sort crops based on probability, in descending order
    top_crops = predictions_df.T.sort_values(by=0, ascending=False).head(top_n)
    return top_crops

# Get the top N most likely crops (you can adjust top_n as needed)
top_n = 5  # Change this number to predict top N crops (e.g., 3, 5, or even 10)
top_crops = get_top_crops(predictions_df, top_n)

# Display the top N crops
print(f"\nTop {top_n} predicted crops for the given conditions:\n{top_crops}")

# Optionally, display the most probable crop
most_probable_crop = predictions_df.idxmax(axis=1)
print(f"\nThe most probable crop for the given conditions is: {most_probable_crop[0]}")

#==============================================================================
