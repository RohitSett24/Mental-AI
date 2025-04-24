import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples - using a smaller dataset for faster training
n = 500

# Define categories and values
academic_categories = ['Excellent', 'Good', 'Average', 'Poor']
mental_health_conditions = ['Anxiety', 'Depression', 'Stress', 'Bipolar', 'OCD', 'PTSD', 'ADD', 'Panic Disorder', 'Normal']

# Generate synthetic data with all 10 features
data = {
    'sleep_hours': np.random.randint(3, 12, n),
    'academic_performance': np.random.choice(academic_categories, n),
    'bullied': np.random.choice([True, False], n, p=[0.3, 0.7]),
    'has_close_friends': np.random.choice([True, False], n, p=[0.8, 0.2]),
    'homesick_level': np.random.randint(1, 6, n),
    'mess_food_rating': np.random.randint(1, 6, n),
    'sports_participation': np.random.choice([True, False], n, p=[0.5, 0.5]),
    'social_activities': np.random.randint(0, 6, n),
    'study_hours': np.random.randint(0, 11, n),
    'screen_time': np.random.randint(1, 13, n),
    'mental_health_condition': np.random.choice(mental_health_conditions, n)
}

# Create DataFrame
df = pd.DataFrame(data)

print("Created synthetic dataset with 10 features")

# Encode categorical features
le_academic = LabelEncoder()
df['academic_performance'] = le_academic.fit_transform(df['academic_performance'])

le_condition = LabelEncoder()
df['mental_health_condition'] = le_condition.fit_transform(df['mental_health_condition'])

# Convert boolean columns to int
df['bullied'] = df['bullied'].astype(int)
df['has_close_friends'] = df['has_close_friends'].astype(int)
df['sports_participation'] = df['sports_participation'].astype(int)

# Features and target
X = df.drop('mental_health_condition', axis=1)
y = df['mental_health_condition']

print("Training model with all 10 features...")

# Train Random Forest with fewer trees for speed
clf = RandomForestClassifier(n_estimators=20, random_state=42)
clf.fit(X, y)

print("Model training complete")

# Save the model and encoders
joblib.dump(clf, 'mental_health_rf_model_2500.pkl')
joblib.dump(le_academic, 'le_academic_2500.pkl')
joblib.dump(le_condition, 'le_condition_2500.pkl')
print("Model and encoders saved - replacing existing files")
