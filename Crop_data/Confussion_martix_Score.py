import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
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

# Initialize the RandomForestClassifier
model = RandomForestClassifier(random_state=0)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Confusion matrix
cm = metrics.confusion_matrix(y_test, y_pred)

# Plot the confusion matrix as a heatmap
plt.figure(figsize=(15, 15))
sns.heatmap(cm, annot=True, fmt=".0f", linewidths=.5, square=True, cmap='Blues_r')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
all_sample_title = 'Confusion Matrix - Accuracy Score: ' + str(metrics.accuracy_score(y_test, y_pred))
plt.title(all_sample_title, size=15)
plt.show()

# Print the classification report
print(metrics.classification_report(y_test, y_pred))
