# dataset_generate.py
import pandas as pd
import numpy as np
import random

def generate_dataset(num_records=10000):
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    sentiment_phrases_low_risk = [
        "I feel great today", "Class was fun", "Excited for the football game",
        "Homework was easy", "Had a good day at school", "Love my teachers"
    ]
    sentiment_phrases_high_risk = [
        "Feeling very overwhelmed", "Nobody wants to talk to me", "Struggling with math",
        "So tired and stressed out", "I feel lonely during lunch", "Too much pressure"
    ]
    
    for i in range(1, num_records + 1):
        student_id = f"STU{i:05d}"
        
        # Academic Analytics
        attendance_rate = round(np.random.beta(a=8, b=2) * 100, 2)  # Skewed towards high attendance
        homework_submission_rate = round(np.random.beta(a=7, b=3) * 100, 2)
        exam_score_avg = round(np.random.normal(75, 12), 2)
        exam_score_avg = max(0.0, min(100.0, exam_score_avg))
        
        # Safety & Transport Log Metrics
        gate_pass_violations = np.random.poisson(0.3) # Mostly 0, occasionally higher
        bus_delay_minutes = int(np.random.exponential(scale=5))
        
        # Mental Wellness Indicators (Simulated Sentiment Analysis score -1 to 1)
        # If homework submission or exam scores are low, increase chance of negative sentiment
        if exam_score_avg < 55 or homework_submission_rate < 60:
            sentiment_score = round(np.random.uniform(-1.0, 0.2), 2)
            sentiment_text = random.choice(sentiment_phrases_high_risk)
        else:
            sentiment_score = round(np.random.uniform(-0.2, 1.0), 2)
            sentiment_text = random.choice(sentiment_phrases_low_risk)
            
        # Gamification component
        gamified_points = int((homework_submission_rate * 10) + (exam_score_avg * 5))
        
        # Determine Target Class: Risk Level (0: Stable, 1: At-Risk)
        # Decision boundary based on high distress indicators
        risk_score = (
            (100 - attendance_rate) * 0.25 + 
            (100 - homework_submission_rate) * 0.35 + 
            (100 - exam_score_avg) * 0.2 + 
            (gate_pass_violations * 10) + 
            (-sentiment_score * 30)
        )
        
        risk_label = 1 if risk_score > 35 else 0
        
        data.append([
            student_id, attendance_rate, homework_submission_rate, exam_score_avg,
            gate_pass_violations, bus_delay_minutes, sentiment_score, sentiment_text,
            gamified_points, risk_label
        ])
        
    columns = [
        'student_id', 'attendance_rate', 'homework_submission_rate', 'exam_score_avg',
        'gate_pass_violations', 'bus_delay_minutes', 'sentiment_score', 'sentiment_text',
        'gamified_points', 'risk_label'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('student_data.csv', index=False)
    print(f" Successfully generated 'student_data.csv' with {num_records} records.")

if __name__ == "__main__":
    generate_dataset()