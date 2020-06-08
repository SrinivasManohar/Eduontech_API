from flask import Blueprint, render_template, request, redirect, url_for, session
from models.alert import Alert
from models.course import Course
from models.subject import Subject
from models.user import requires_login

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
@requires_login
def index():
    alerts = Alert.find_many_by('user_email', session['email'])
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def create_alert():
    if request.method == 'POST':
        subject_url = request.form['subject_url']

        course = Course.find_by_url(subject_url)
        subject = Subject(subject_url, course.tag_name, course.query)
        subject.load_price()
        subject.save_to_mongo()

        alert_name = request.form['name']
        price_limit = request.form['price_limit']

        Alert(alert_name, subject._id, price_limit, session['email']).save_to_mongo()

    # What happens if it's a GET request
    return render_template("alerts/new_alert.html")



@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])

        alert = Alert.get_by_id(alert_id)
        alert.price_limit = price_limit
        alert.save_to_mongo()

        return redirect(url_for('.index'))

    # What happens if it's a GET request
    return render_template("alerts/edit_alert.html", alert=Alert.get_by_id(alert_id))


@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_mongo()
    return redirect(url_for('.index'))
