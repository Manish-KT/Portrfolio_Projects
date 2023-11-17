"""
This script is responsible for handling training and testing split of dataset.
"""

"""Training and Evaluating Machine Learning Models:"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load your dataset (X, y)
from Data_cleaning import cleaned_data

# asking target column
target_col = input("Enter the traget column name: ")

X = cleaned_data.drop([target_col])
y = cleaned_data[target_col]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train a machine learning model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy}")
