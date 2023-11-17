"""
This script will be used to automate the process of Machine Learning Automation:
Which will include:
    - Data preprocessing
    - Build scripts for training and evaluating machine learning models.
    - Automate hyperparameter tuning.
    - Saving the best model.
"""

# Load your dataset
data = input("Enter the path to your dataset: ")

import Data_cleaning, Train_and_Test, Hyperparameter_Tuning, Save_the_model
