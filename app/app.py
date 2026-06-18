# app/app.py
from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )

@app.route("/")
def home():
    return jsonify({"status": "ok", "service": "devops-challenge"})

@app.route("/health")
def health():
    return "OK", 200

@app.route("/ready")
def ready():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        conn.close()
        return jsonify({"status": "OK", "service": "Ready"})

    except Exception as e:
        return str(e), 500

@app.route("/db")
def db_check():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        conn.close()
        return jsonify({"db": "connected", "version": version[0]})
    except Exception as e:
        return jsonify({"db": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)