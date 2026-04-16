import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, jsonify, render_template

from shared.db import SessionLocal, init_db, wait_for_db
from shared.models import User

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.created_at.desc()).all()
        return render_template("index.html", users=users)
    finally:
        db.close()


@app.route("/api/users")
def api_users():
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.created_at.desc()).all()
        return jsonify([u.to_dict() for u in users])
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Waiting for database...")
    wait_for_db()
    init_db()
    logger.info("Starting Flask app...")
    app.run(debug=False, host="0.0.0.0", port=5000)
