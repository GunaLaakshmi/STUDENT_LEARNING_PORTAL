import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv(r"C:\Users\guna laakshmi\Downloads\student_engagement_dataset.csv")

# Encode categorical variables
label_encoder_device = LabelEncoder()
df['Device_Type'] = label_encoder_device.fit_transform(df['Device_Type'])

label_encoder_engagement = LabelEncoder()
df['Engagement_Level'] = label_encoder_engagement.fit_transform(df['Engagement_Level'])

# Features and target
X = df[['Time_Spent_Modules', 'Device_Type', 'Engagement_Level', 'Participation_Forums', 'Assignment_Submissions']]  # Selected features
y = df['Quiz_Performance_Average']  # Target (Quiz_Performance_Average)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model using Random Forest Regressor
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Predict on the test data
y_pred = model.predict(X_test)

# Save the trained model
joblib.dump(model, 'recommendation_model.pkl')
print("Random Forest model saved successfully.")

# Save the label encoder for decoding predictions later (if needed)
joblib.dump(label_encoder_device, 'label_encoder_device.pkl')
joblib.dump(label_encoder_engagement, 'label_encoder_engagement.pkl')
print("Label encoders saved successfully.")
