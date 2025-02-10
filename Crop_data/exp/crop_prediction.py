import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from dataset import dataset

# Load the dataset
data = dataset()

# Prepare feature columns (X) and target column (y)
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the RandomForestClassifier model
model = RandomForestClassifier(random_state=0)
model.fit(X_train, y_train)

# Define the new data for prediction
new_data = pd.DataFrame({
    
    # 'N': [10],
    # 'P': [12],
    # 'K': [13],
    # 'temperature': [20.8],
    # 'humidity': [10.0],
    # 'ph': [6.5],
    # 'rainfall': [150.9]

    'N': [40],
    'P': [20],
    'K': [15],
    'temperature': [25.0],
    'humidity': [80.0],
    'ph': [6.5],
    'rainfall': [200.0]

})

# **Validation: Check if the conditions are suitable for crops**
invalid_conditions = (
    (new_data['N'][0] == 0 and new_data['P'][0] == 0 and new_data['K'][0] == 0) or  # No nutrients
    (new_data['temperature'][0] <= 0) or
    (new_data['humidity'][0] <= 5) or
    (new_data['ph'][0] < 4 or new_data['ph'][0] > 10) or
    (new_data['rainfall'][0] == 0)
)

if invalid_conditions:
    print("\nNo crop is recommended for the given conditions. The environment is unsuitable for farming.")
else:
    # Get predicted probabilities
    predicted_probabilities = model.predict_proba(new_data)

    # Create a DataFrame with the predicted probabilities
    predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

    # Filter out crops with zero probability
    filtered_predictions = predictions_df.T[predictions_df.T[0] > 0].sort_values(by=0, ascending=False)

    # Check if any crop is recommended
    if filtered_predictions.empty:
        print("\nNo crop is recommended for the given conditions. The environment is unsuitable for farming.")
    else:
        # Display the predicted probabilities for each crop
        print("\nPredicted probabilities for each crop:")
        print(filtered_predictions)

        # Get the most probable crop
        most_probable_crop = filtered_predictions.index[0]
        print(f"\nThe most probable crop for the given conditions is: {most_probable_crop}")
