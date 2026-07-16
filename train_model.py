# train_model.py
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def train_risk_model():
    # Load dataset
    try:
        df = pd.read_csv('student_data.csv')
    except FileNotFoundError:
        print("Dataset not found. Please run dataset_generate.py first.")
        return

    # Select operational numerical features for prediction
    features = [
        'attendance_rate', 'homework_submission_rate', 'exam_score_avg',
        'gate_pass_violations', 'bus_delay_minutes', 'sentiment_score', 'gamified_points'
    ]
    
    X = df[features]
    y = df['risk_label']
    
    # Split Dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train Random Forest Classifier
    print("Training predictive model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"Model Training Complete. Accuracy: {acc*100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, predictions))
    
    # Save the model artifact
    with open('risk_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved successfully as 'risk_model.pkl'.")

if __name__ == "__main__":
    train_risk_model()