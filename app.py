from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "Teacher's_journal/grades.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/grades", methods=["GET"])
def get_grades():
    data = load_data()
    return jsonify(data)


@app.route("/grades", methods=["POST"])
def add_grade():
    data = load_data()
    req = request.json
    
    student = req.get("student")
    subject = req.get("subject")
    grade = req.get("grade")
    print(student,subject,grade)
    if not student or not subject:
        return jsonify({"status": "error"}), 400

    if student not in data:
        data[student] = {}
    if int(grade) > 5:
        grade = '5'
    elif int(grade) < 1:
        grade = '1'
    
    data[student][subject] = grade

    save_data(data)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
