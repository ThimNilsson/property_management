# property_management
## Pre-req
docker  
docker-compose  
## Install
sudo docker-compose up -d  
## Loading Testdata
\\#Load two building objects to database  
curl --request POST --data "name=byggnad1" http://localhost:5000/api/buildings  
curl --request POST --data "name=byggnad2" http://localhost:5000/api/buildings  
\\#Query all of the building objects just  
curl http://localhost:5000/api/buildings  
\\#Query one of the building objects  
curl http://localhost:5000/api/buildings?building_id=1  

\\#Load maintenance tasks  
curl --request POST --data "building_id=1&name=byta golv&cost=50000&description=golv är slitet&due_date=2022-01-31" http://localhost:5000/api/tasks  
curl --request POST --data "building_id=1&name=lägga om tak&cost=200000&description=tak läcker&due_date=2022-01-31" http://localhost:5000/api/tasks  
\\#Query all of the maintenance tasks  
curl http://localhost:5000/api/tasks  
\\#Query one of the maintenance tasks  
curl http://localhost:5000/api/tasks?building_id=1  


## Full example with ubuntu
$ sudo apt install docker docker-compose  
$ git clone https://github.com/ThimNilsson/property_management.git  
$ cd property_management/  
$ sudo docker-compose up -d  
