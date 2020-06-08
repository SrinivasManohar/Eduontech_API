
import os
from flask import Flask, render_template
from views.alerts import alert_blueprint
from views.courses import course_blueprint
from views.users import user_blueprint

app = Flask(__name__)
app.secret_key = 'edutech'
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)

@app.route("/")
def home():
    return render_template("home.html")

# @app.route("/")
# def map_func():
#     return render_template('interactive_map.html')

app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(course_blueprint, url_prefix="/courses")
app.register_blueprint(user_blueprint, url_prefix="/users")


if __name__ == "__main__":
    app.run(port=49674, debug=True)