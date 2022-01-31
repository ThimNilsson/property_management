# property_management
## General  
I'm just practicing API development. This will spin upp 4 containers.  
- Backend : API, python, Flask  
- DB : Postgres  
- Frontend : Python, Flaks  
- DB Management : Adminer  

The containers are placed in different networks to simulate real life network scenario. 
The application is used for register and query maintenance plans for realestate properties. 

By default the backend API will be reaced on port 5000, and the frontend will bea reached on port 80. This can be changed in the docker compose file.  

## Pre-req
docker  
docker-compose  
## Install
sudo docker-compose up -d  

## Tutorial: Install on ubuntu
$ sudo apt install docker docker-compose  
$ git clone https://github.com/ThimNilsson/property_management.git  
$ cd property_management/  
$ sudo docker-compose up -d  

## Load Testdata
\#Load two building objects to database  
curl --request POST --data "name=byggnad1" http://localhost:5000/api/buildings  
curl --request POST --data "name=byggnad2" http://localhost:5000/api/buildings  

\#Load maintenance tasks  
curl --request POST --data "building_id=1&name=byta golv&cost=50000&description=golv är slitet&due_date=2022-01-31" http://localhost:5000/api/tasks  
curl --request POST --data "building_id=1&name=lägga om tak&cost=200000&description=tak läcker&due_date=2022-01-31" http://localhost:5000/api/tasks  
curl --request POST --data "building_id=2&name=vvs&cost=220000&description=tak läcker&due_date=2023-01-31" http://localhost:5000/api/tasks  

## Test
\#Query all of the building objects just  
curl http://localhost:5000/api/buildings  

\#Query one of the building objects  
curl http://localhost:5000/api/buildings?building_id=1  

\#Query all of the maintenance tasks  
curl http://localhost:5000/api/tasks  

\#Query one of the maintenance tasks  
curl http://localhost:5000/api/tasks?building_id=1  

\#Query reports  
curl "http://localhost:5000/api/reports/tasks_details" -Method GET  
curl "http://localhost:5000/api/reports/tasks_cost_per_year" -Method GET  

\#Query some environment inforamtion  
curl "http://localhost:5000/api/admin/show_config" -Method GET  
curl "http://localhost:5000/api/admin/create_tables" -Method GET 
