
# lets-ride

There will be 2 persons one is a Rider and the other is an Asset Transportation Requester (will be referred as requester from now on). 
A Rider is a person who travels from one place to another and is willing to carry some assets(packages/luggages) along with him. 
A Requester is a person who wants his assets to be carried by someone else from one place to another. 
Requesters can create transportation requests and Riders can share their rides independently
.



# Features

- A Rider can share his travel info with details like from and to locations, the number of assets he can take with him etc. 

- Requesters can request to carry their assets, with details like from and to locations, the type of assets, number of assets that need to be carried.
- A Requester should be able to see all the asset transportation requests requested by him. 

- A Requester should be able to see all the matching travel info shared by Riders based on his asset transportation requests locations.

- A Requester can apply to carry his assets by a Rider.



# Installation

Install lets-ride with pip

```bash
  pip install requirements.txt
```

Build docker image

```bash
docker build -t rider .
```

# Running the server

run django server locally

```bash
python manage.py runserver 0.0.0.0:8000
```

Run in a docker container

```bash 
docker run -d --name lets-ride -p 8000:8000 rider
```
    