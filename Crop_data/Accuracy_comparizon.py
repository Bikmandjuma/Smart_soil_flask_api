# import matplotlib.pyplot as plt
# import seaborn as sns
# from dataset import dataset  # Import the dataset function

# # Load the dataset using the dataset function
# data = dataset()

# # You can modify this to your actual model names and accuracies
# model_name = ['Model 1', 'Model 2', 'Model 3', 'Model 4', 'Model 5']
# accuracy = [0.85, 0.88, 0.91, 0.87, 0.90]  # These are just example accuracy values

# # Creating the bar plot
# plt.figure(figsize=(15, 9))
# plt.title('Accuracy Comparison')
# plt.xlabel('Accuracy')
# plt.ylabel('Model')

# # Create the bar plot using seaborn
# sns.barplot(x=accuracy, y=model_name)

# # Show the plot
# plt.show()

# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score
# from dataset import dataset  # Import the dataset function

# # Load the dataset using the dataset function
# data = dataset()

# # Define the features and target
# X = data.drop(columns=['label'])  # All columns except 'label' are features
# y = data['label']  # 'label' is the target variable (crop label)

# # Split the data into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initialize the models
# models = {
#     'Decision Tree': DecisionTreeClassifier(),
#     'Random Forest': RandomForestClassifier(),
#     'SVM': SVC(),
#     'KNN': KNeighborsClassifier(),
#     'Logistic Regression': LogisticRegression(max_iter=1000)
# }

# # List to store accuracies
# accuracies = []

# # Train each model and compute accuracy
# for model_name, model in models.items():
#     # Train the model
#     model.fit(X_train, y_train)
    
#     # Predict on the test set
#     y_pred = model.predict(X_test)
    
#     # Calculate accuracy
#     accuracy = accuracy_score(y_test, y_pred)
#     accuracies.append(accuracy)

# # Plotting the results
# plt.figure(figsize=(15, 9))
# plt.title('Accuracy Comparison')
# plt.xlabel('Accuracy')
# plt.ylabel('Model')

# # Create the bar plot using seaborn
# sns.barplot(x=accuracies, y=list(models.keys()))

# # Show the plot
# plt.show()

# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score
# from dataset import dataset  # Import the dataset function

# # Load the dataset using the dataset function
# data = dataset()

# # Show the first few rows to confirm the data
# print(data.head())

# # Define the features and target
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]  # Features
# y = data['label']  # Target variable (crop label)

# # Split the data into training and test sets (80% train, 20% test)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initialize the models
# models = {
#     'Decision Tree': DecisionTreeClassifier(),
#     'Random Forest': RandomForestClassifier(),
#     'SVM': SVC(kernel='linear'),  # Using linear kernel for feature importance
#     'KNN': KNeighborsClassifier(),
#     'Logistic Regression': LogisticRegression(max_iter=1000)
# }

# # List to store feature importances for each model
# feature_importances = []

# # Train each model and calculate feature importance
# for model_name, model in models.items():
#     # Train the model on the training data
#     model.fit(X_train, y_train)
    
#     # Get feature importance (if available)
#     if hasattr(model, 'coef_'):  # Logistic Regression and SVM
#         importance = model.coef_[0]
#     elif hasattr(model, 'feature_importances_'):  # Decision Tree, Random Forest
#         importance = model.feature_importances_
#     else:
#         importance = [0] * len(X.columns)  # For models that don't have feature importance
    
#     # Store feature importance along with the model name
#     feature_importances.append(importance)

# # Plotting the results
# plt.figure(figsize=(15, 9))
# plt.title('Feature Importance Comparison for Different Models')

# # Plot each model's feature importance
# for i, (model_name, importance) in enumerate(zip(models.keys(), feature_importances)):
#     sns.barplot(x=importance, y=X.columns, label=model_name, ci=None)

# plt.xlabel('Importance')
# plt.ylabel('Feature')
# plt.legend(title='Models')
# plt.show()

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
