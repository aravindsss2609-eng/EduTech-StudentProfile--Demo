import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Core Global In-Memory Databases - Kept completely intact and upgraded safely
STUDENT_REGISTRY = []
SYSTEM_REPORTS = []
WELLNESS_LOGS = []
OD_REGISTRY = []  # Added to track all official duty student event logs safely!

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictive-analytics')
def predictive_analytics():
    return render_template('predictive-analytics.html')

@app.route('/behavioral-matrix')
def behavioral_matrix():
    return render_template('behavioral-matrix.html')

@app.route('/historical-timeline')
def historical_timeline():
    return render_template('historical-timeline.html')

@app.route('/report-issue')
def report_issue():
    return render_template('report-issue.html')

@app.route('/report-history')
def report_history():
    return render_template('report-history.html')

@app.route('/student-profiles')
def student_profiles():
    return render_template('student-profiles.html')

@app.route('/od-letter')
def od_letter():
    return render_template('od-letter.html')

@app.route('/leave-letter')
def leave_letter():
    return render_template('leave-letter.html')

@app.route('/wellness-sanctuary')
def wellness_sanctuary():
    return render_template('wellness-sanctuary.html')


# --- SYSTEM REST API ENDPOINTS ---

@app.route('/api/get_students', methods=['GET'])
def get_students():
    return jsonify(STUDENT_REGISTRY)

@app.route('/api/add_student', methods=['POST'])
def add_student():
    data = request.json
    try:
        new_student = {
            "student_id": data.get("student_id"),
            "name": data.get("name", "N/A"),
            "age": data.get("age", "N/A"),
            "phone": data.get("phone", "N/A"),
            "email": data.get("email", "N/A"),
            "address": data.get("address", "N/A"),
            "dob": data.get("dob", "N/A"),
            "gender": data.get("gender", "N/A"),
            "attendance_rate": float(data.get("attendance_rate", 0)),
            "homework_submission_rate": float(data.get("homework_submission_rate", 0)),
            "exam_score_avg": float(data.get("exam_score_avg", 0)),
            "sentiment_text": data.get("sentiment_text", "Normal Status"),
            "projects_done": data.get("projects_done", "None Specified"),
            "hobbies": data.get("hobbies", "None Specified"),
            "target_course": data.get("target_course", "None Specified")
        }
        STUDENT_REGISTRY.append(new_student)
        return jsonify({"status": "success", "message": "Comprehensive Student Metadata Vector Logged!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/get_reports', methods=['GET'])
def get_reports():
    return jsonify(SYSTEM_REPORTS)

@app.route('/api/add_report', methods=['POST'])
def add_report():
    data = request.json
    try:
        new_report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reporter_role": data.get("reporter_role"),
            "reporter_name": data.get("reporter_name") or "Anonymous",
            "issue_category": data.get("issue_category"),
            "urgency_level": data.get("urgency_level"),
            "description": data.get("description")
        }
        SYSTEM_REPORTS.append(new_report)
        return jsonify({"status": "success", "message": "Grievance filed successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# --- NEW OD EVENT SYSTEM APIS ---

@app.route('/api/add_od_log', methods=['POST'])
def add_od_log():
    data = request.json
    try:
        new_od = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "student_name": data.get("student_name") or "Unnamed Student",
            "student_id": data.get("student_id") or "N/A",
            "department": data.get("department") or "N/A",
            "event_name": data.get("event_name") or "N/A",
            "venue": data.get("venue") or "N/A",
            "start_date": data.get("start_date") or "N/A",
            "end_date": data.get("end_date") or "N/A"
        }
        OD_REGISTRY.append(new_od)
        return jsonify({"status": "success", "message": "Official Duty record stored successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/get_od_logs', methods=['GET'])
def get_od_logs():
    return jsonify(OD_REGISTRY)

# --- WELLNESS MONITOR API ---
@app.route('/api/add_wellness_log', methods=['POST'])
def add_wellness_log():
    data = request.json
    try:
        new_log = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "student_name": data.get("student_name") or "Anonymous Student",
            "issue_type": data.get("issue_type"),
            "medication_given": data.get("medication_given") or "Rest & Care Observation",
            "dosage": data.get("dosage") or "N/A",
            "support_note": data.get("support_note") or "Keep showing up. You are doing amazing."
        }
        WELLNESS_LOGS.append(new_log)
        return jsonify({"status": "success", "message": "Wellness profile and medical dispatch updated!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/get_wellness_logs', methods=['GET'])
def get_wellness_logs():
    return jsonify(WELLNESS_LOGS)

@app.route('/api/get_logs', methods=['GET'])
def get_logs():
    total_students = len(STUDENT_REGISTRY)
    if total_students == 0:
        return jsonify([])

    avg_performance = sum(s["exam_score_avg"] for s in STUDENT_REGISTRY) / total_students
    avg_attendance = sum(s["attendance_rate"] for s in STUDENT_REGISTRY) / total_students
    
    anxiety_factor = round(max(0.05, (100 - avg_performance) / 100), 2)
    xp_velocity = f"{int(avg_attendance * 150)} XP"
    safety_clearance = f"{round(min(99.9, avg_attendance + 5), 2)}%"

    return jsonify([
        {"date": datetime.now().strftime("%Y-%m-%d (Active Session)"), "anxiety": anxiety_factor, "velocity": xp_velocity, "safety": safety_clearance}
    ])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)