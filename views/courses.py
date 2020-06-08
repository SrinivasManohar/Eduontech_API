import json
from flask import Blueprint, render_template, request, redirect, url_for
from models.course import Course
from models.user import requires_login, requires_admin

course_blueprint = Blueprint('courses', __name__)


@course_blueprint.route('/')
@requires_login
def index():
    courses = Course.all()
    return render_template('courses/course_index.html', course=courses)


@course_blueprint.route('/new', methods=['GET', 'POST'])
@requires_admin
def create_course():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        Course(name, url_prefix, tag_name, query).save_to_mongo()

    # What happens if it's a GET request
    return render_template("courses/new_course.html")



@course_blueprint.route('/edit/<string:course_id>', methods=['GET', 'POST'])
@requires_admin
def edit_course(course_id):
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        course = Course.get_by_id(course_id)

        course.name = name
        course.url_prefix = url_prefix
        course.tag_name = tag_name
        course.query = query

        course.save_to_mongo()

        return redirect(url_for('.index'))

    # What happens if it's a GET request
    return render_template("courses/edit_course.html", course=Course.get_by_id(course_id))


@course_blueprint.route('/delete/<string:course_id>')
@requires_admin
def delete_course(course_id):
    Course.get_by_id(course_id).remove_from_mongo()
    return redirect(url_for('.index'))
