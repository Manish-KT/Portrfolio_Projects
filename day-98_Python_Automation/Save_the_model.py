"""
This script is responsible for saving the best model.
"""

from sklearn.externals import joblib
from Train_and_Test import X, y
from Hyperparameter_Tuning import best_model

# Assuming best_model is the model after hyperparameter tuning
# Train the best model on the entire dataset (optional)
best_model.fit(X, y)

# Save the model to a file
joblib.dump(best_model, 'best_model.joblib')

# Now you can load the model whenever you need it
loaded_model = joblib.load('best_model.joblib')

# Use the loaded model for predictions
predictions = loaded_model.predict(X_test)
