import os

# Set environment variables
def config():
    db = os.environ['POSTGRES_DB']
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    server = os.environ['POSTGRES_SERVER']
    port = os.environ['POSTGRES_PORT']

    conn = { "host": server, "database": db, "user": user, "password": password }
    return conn

