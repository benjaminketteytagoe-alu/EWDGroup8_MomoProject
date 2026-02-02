from flask import Flask
from dotenv import load_dotenv
import os

from db import db
from routes.users import user_bp
from routes.transactions import transactions_bp

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


app = Flask(__name__)
app.json.sort_keys = False

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(transactions_bp, url_prefix="/api")


if __name__ == "__main__":
    app.run(debug=True, port=3000)
