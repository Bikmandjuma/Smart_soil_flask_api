import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from dataset import dataset  # Import the dataset function

# Load the dataset using the dataset function
data = dataset()

# Show the first few rows to confirm the data
print(data.head())

# Define the features and target
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]  # Features
y = data['label']  # Target variable (crop label)

# Split the data into training and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize a single model
model = RandomForestClassifier()

# Train the model on the training data
model.fit(X_train, y_train)

# Get feature importance for RandomForest
importance = model.feature_importances_

# Plotting the feature importance
plt.figure(figsize=(10, 6))
sns.barplot(x=importance, y=X.columns, color='skyblue')
plt.title('Feature Importance using RandomForestClassifier')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()
