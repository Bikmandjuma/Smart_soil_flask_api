import matplotlib.pyplot as plt
import seaborn as sns
from dataset import dataset  # Import the dataset function

# Calling the dataset function to load the data
data = dataset()  # This loads the dataset as a DataFrame

# Columns to plot
columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

# Create subplots: 7 rows, 1 column
fig, ax = plt.subplots(7, 1, figsize=(15, 21), sharex=True)

i = 0
for column in columns:
    # Create a violin plot for each column
    sns.violinplot(data=data, x='label', y=column, ax=ax[i])
    
    # Rotate the x-axis labels
    ax[i].set_xticklabels(ax[i].get_xticklabels(), rotation=45)
    
    # Title for each subplot
    ax[i].set_title(f'{column} distribution by crop label', fontsize=16)
    
    i = i + 1

# General title for the entire figure
plt.suptitle('Distribution of Different Features by Crop Label', fontsize=20, c='black')

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.95)  # Adjust the top margin to make space for the suptitle
plt.show()