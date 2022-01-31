from flask import Flask
from flask import request 
from flask import jsonify
app = Flask(__name__)
import os
import data_access as da
from config import config

# This will make sure that the database is up and running
while not da.create_tables():
  da.create_tables() 

# The admin api is just for myself during the development to verify db settings and db schema status 
@app.route('/api/admin/show_config')
def admin_show_conf():
    my_conf = config()
    return my_conf 

@app.route('/api/admin/create_tables')
def admin_create_tables():
    if da.create_tables() == True:
        status = {"status" : "success: the SQL tables has been created"}
    else:
        status = {"status" : "error: the SQL tables has not been created"}
    return jsonify(status) 

# if no id is passed, this api will return all buildings
# new buildings can be created with the POST method
@app.route('/api/buildings', methods = ['GET', 'POST'])
def buildings():
    if request.method == 'GET':
        building_id = request.values.get('building_id')
        if building_id is None:
            result = []
            rows = da.get_all_buildings()
            for row in rows:
                result.append({"building_id":row[0], "name":row[1]})
        else:
            result = []
            rows = da.get_building(building_id)
            for row in rows:
                result.append({"building_id":row[0], "name":row[1]})
    if request.method == 'POST':
        name = request.form.get('name')
        if da.insert_building(name):
            result = {"status": "success"}
        else:
            result = {"status": "error"}
    return jsonify(result)

# tasks can be queried on both task_id and building_id
# new tasks can be created with the POST method. 
# a building must axist for a task to be created
@app.route('/api/tasks', methods = ['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        task_id = request.values.get('task_id')
        building_id = request.values.get('building_id')
        if task_id is None and building_id is None:
            result = []
            rows = da.get_all_tasks()
        elif task_id is not None and building_id is None:
            result = []
            rows = da.get_task_by_task_id(task_id)
        elif task_id is None and building_id is not None:
            result = []
            rows = da.get_task_by_building_id(building_id)
        for row in rows:
            result.append({ "task_id":row[0], "building_id":row[1], "name":row[2], "description":row[3], "cost":row[4], "due_date":row[5]})
    if request.method == 'POST':
        building_id = request.form.get('building_id')
        name = request.form.get('name')
        cost = request.form.get('cost')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        if da.insert_task(building_id, name, cost, description, due_date):
            result = {"status": "success"}
        else:
            result = {"status": "error"}
    return jsonify(result)

# this report will return all tasks and their costs, along with building name
@app.route('/api/reports/tasks_details', methods = ['GET'])
def report_tasks_details():
    result = []
    rows = da.get_report_tasks_details()
    for row in rows:
        result.append({ "building_name":row[0], "task_name":row[1], "cost":row[2], "due_date":row[3]})
    return jsonify(result)

# this report will return a list with costs per year 
@app.route('/api/reports/tasks_cost_per_year', methods = ['GET'])
def report_tasks_cost_per_year():
    result = []
    rows = da.get_report_tasks_cost_per_year()
    for row in rows:
        result.append({ "year":int(row[0]), "total_cost":int(row[1])})
    return jsonify(result)


