# Data Pipeline Phase One Web Portal

http://ec2-34-226-142-78.compute-1.amazonaws.com:5000/

## start website (with docker)
Go to where the docker-compose file is

```
docker-compose build
docker-compose up
```
Go to localhost:5000

Note: needs to install docker first

## deploy website
1. production build for react
```
cd react-client
npm run build
```
2. build and push the image
go to where the docker-compose file is
```
docker-compose build
docker-compose push
```
3. go to EC2 server and pull the image

Note: get the pem file from Abdiel
```
sudo ssh -i "enrichment_app_key.pem" ec2-user@ec2-34-226-142-78.compute-1.amazonaws.com
sudo docker-compose pull
sudo docker-compose up
```
Go to: http://ec2-34-226-142-78.compute-1.amazonaws.com:5000/

## config (set in server.py)
1. access token: 30 min expiration, refresh token: 45 min expiration
2. Two types of users for login: 

username: admin, password: Texas512

username: user, password: apple

3. reports stored in uploads folder

## code structure
### flask-server

1. uploads: storing uploaded reports
2. server.py: backend server

### react-client
1. api: customized axios instance
2. context: storing user login info on the front end
3. hooks: hooks for handling login

## reference
login and authentication

https://www.youtube.com/watch?v=X3qyxo_UTR4&list=PL0Zuz27SZ-6PRCpm9clX0WiBEMB70FWwd

react-table v7

https://www.youtube.com/watch?v=YwP4NAZGskg&list=PLC3y8-rFHvwgWTSrDiwmUsl4ZvipOw9Cz
