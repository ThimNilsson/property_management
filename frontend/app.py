import requests
import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap


app = Flask(__name__)
# A secret key is needed for several FLASK functions
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# Flask-Bootstrap requires this line
Bootstrap(app)

# Forms
class BuildingForm(FlaskForm):
    name = StringField('Namn på fastighet?', validators=[DataRequired()])
    submit = SubmitField('Lägg till')

class TaskForm(FlaskForm):
    name = StringField('Namn på underhåll?', validators=[DataRequired()])
    description = TextAreaField('Beskrivning av underhåll?', validators=[DataRequired(), Length(max=2048)])
    cost = IntegerField('Kostnad i sek?', validators=[DataRequired()])
    due_date = DateField('Datum?', validators=[DataRequired()])
    submit = SubmitField('Lägg till')

def query_api(API_URL):
    """submit the API query using variables for zip and API_KEY"""
    try:
        data = requests.get(API_URL).json()
    except Exception as exc:
        print(exc)
        data = None
    return data

def post_api(API_URL, body):
    """submit the API query using variables for zip and API_KEY"""
    try:
        data = requests.post(API_URL, data = body).json()
    except Exception as exc:
        print(exc)
        data = None
    return data

@app.route('/')
def index():
    return render_template('index.html')

# Currently two reports are avalible. This function query for the reports and render a page to display them
@app.route('/report')
def report():
    TASKS_REPORT_DETAIL_API_URL = ('http://backend:5000/api/reports/tasks_details')
    tasks_report_details_resp =  query_api(TASKS_REPORT_DETAIL_API_URL)
    TASKS_REPORT_COST_API_URL = ('http://backend:5000/api/reports/tasks_cost_per_year')
    tasks_report_cost_resp=  query_api(TASKS_REPORT_COST_API_URL)
    return render_template('report.html', details=tasks_report_details_resp, year_cost=tasks_report_cost_resp)


@app.route('/property_management', methods=['GET', 'POST'])
def property_management():
    # Get a list of all buildings, in order to disaply them
    BUILDINGS_API_URL = ('http://backend:5000/api/buildings')
    buildingsresp =  query_api(BUILDINGS_API_URL)
    # Form to add new buildings
    buildingform = BuildingForm()
    message = ""
    if buildingform.validate_on_submit():
        name = buildingform.name.data
        post_api(BUILDINGS_API_URL, {"name": name})
        # refresh list of existing buildings at submit
        buildingsresp =  query_api(BUILDINGS_API_URL)
    return render_template('property_management.html', buildings=buildingsresp, buildingform=buildingform)


@app.route('/task_management/<string:building_id>', methods=['GET', 'POST'])
def task_management(building_id):
    # Get list of tasks per building
    BUILDINGS_API_URL = ('http://backend:5000/api/buildings?building_id={}'.format(building_id))
    buildingsresp =  query_api(BUILDINGS_API_URL)
    TASKS_API_URL = ('http://backend:5000/api/tasks?building_id={}'.format(building_id))
    TASKS_POST_API_URL = ('http://backend:5000/api/tasks')
    tasksresp =  query_api(TASKS_API_URL)
    # Form to add new tasks
    form = TaskForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        cost = form.cost.data
        due_date = form.due_date.data
        post_api(TASKS_POST_API_URL, {"building_id": building_id, "name": name, "description": description, "cost": cost, "due_date": due_date})
        # refresh list of existing tasks at submit
        tasksresp =  query_api(TASKS_API_URL)
    return render_template('task_management.html', building=buildingsresp, tasks=tasksresp, form=form)

if __name__ == '__main__':
    app.run(debug=True)
