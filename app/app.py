from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)


@app.route('/')
def index():
    return "This is the API"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
