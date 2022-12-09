## Let us Dribble

Chad NBA NOSQL database meant to analyze teammates.

### Setup:
* Install [Docker](https://www.docker.com/)
* Start Docker Desktop
* Clone this repo and navigate to it
* cd into app directory
* In terminal, run "docker build . -t bball:latest" (will take a few mins)
* Run "docker run -dit bball:latest" 
* You know have a docker container
* Either attach in terminal or open docker desktop browser, go to container tab, find newly created container, and select "Open Terminal"
* Within container, run "poetry run python3 run.py" (will also take a few mins)
### Intended Tech Stack:
* Python
* Docker
* Neo4J
* Poetry

### TODO:
* Put better data into neo4J DB. Player data is not in other than name
* Make analysis