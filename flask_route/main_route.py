from flask import Flask

from flask_route.monthly_route import monthly_api

app = Flask(__name__)
app.secret_key = "9999"
port = 6620

@app.route("/test", methods=["GET", "POST"])
def test_api():
    result = {
        "message": "ok",
    }
    return result

app.register_blueprint(monthly_api, url_prefix="/monthly")