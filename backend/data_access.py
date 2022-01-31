#!/usr/bin/python

import psycopg2
from config import config

def run_generic_commands(commands):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        return True 
    except (Exception, psycopg2.DatabaseError) as error:
        raise(error)
        return False 
    finally:
        if conn is not None:
            conn.close()

def run_command(command):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        rows = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        return rows 
    except (Exception, psycopg2.DatabaseError) as error:
        raise(error)
    finally:
        if conn is not None:
            conn.close()

def get_task_by_task_id(task_id):
    return run_command("SELECT * FROM tasks where task_id = '{}'".format(task_id))

def get_task_by_building_id(building_id):
    return run_command("SELECT * FROM tasks where building_id = '{}'".format(building_id))

def get_all_tasks():
    return run_command("SELECT * FROM tasks")

def insert_task(building_id, name, cost, description, due_date):
    return run_command("INSERT INTO tasks (building_id, name, cost, description, due_date) VALUES({}, '{}', {}, '{}', '{}') RETURNING task_id;".format(building_id, name, cost, description, due_date))

def get_all_buildings():
    return run_command("SELECT * FROM buildings")

def get_building(id):
    return run_command("SELECT * FROM buildings WHERE building_id = {}".format(id))

def insert_building(name):
    return run_command("INSERT INTO buildings (name) values ('{}') RETURNING building_id".format(name))
    
def get_report_tasks_details():
    command="""
    SELECT
    b.name,
    t.name,
    t.cost,
    t.due_date
    FROM buildings b
        inner join tasks t
            on b.building_id = t.building_id
    ORDER BY t.due_date
    """
    return run_command(command)

def get_report_tasks_cost_per_year():
    command="""
    SELECT date_part('year', due_date) as year,
    sum(cost) as yearly_cost
        FROM tasks
    GROUP BY year
    """
    return run_command(command)

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS buildings(
            building_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks(
                task_id SERIAL PRIMARY KEY,
                building_id INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                description VARCHAR(2048) NOT NULL,  
                cost INTEGER NOT NULL,  
                due_date date NOT NULL,  
                FOREIGN KEY (building_id)
                REFERENCES buildings (building_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
        )
    status = run_generic_commands(commands)
    return status 


if __name__ == '__main__':
    create_tables()
