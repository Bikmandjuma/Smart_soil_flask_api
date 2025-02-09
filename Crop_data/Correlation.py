import matplotlib.pyplot as plt
import seaborn as sns
from dataset import dataset  # Import the function dataset from dataset.py

# Reading the dataset using the dataset function
data = dataset()  # Call the dataset function to load the data

# Selecting only numeric columns for correlation
numeric_data = data.select_dtypes(include=['float64', 'int64'])

# Create a figure and axis for the heatmap
fig, ax = plt.subplots(1, 1, figsize=(15, 9))

# Create a heatmap to visualize the correlation between numeric features
sns.heatmap(numeric_data.corr(), annot=True)

# Set axis labels
ax.set(xlabel='Features', ylabel='Features')

# Adding a title to the heatmap
plt.title('Correlation between Different Features', fontsize=20, color='black')

# Show the heatmap
plt.show()