# Monge usage demo

Giving the short demo of how to interact e.g. query, aggregate with Mongodb as One of the most popular noSQL 

# Service
1. Mongodb server
    - `docker-compose up -d`
2. run scripts locally in `./scripts`


# Run (dev mode)
- If virtual env already exists, activate: pipenv shell
    - If not, create virtual env: pipenv shell
    - Install all required packages:
        - install packages exactly as specified in Pipfile.lock: pipenv sync
        - install using the Pipfile, including the dev packages: pipenv install --dev

# Files
- db and table could be adjusted in `scripts/config.py` 
- The data will be inserted when the MongoDB server is initialized  via `scripts/insert_data_to_db.py`
- The core script is `scripts/mongo.py` which wrap up the frequent functions being used in pymongo and is further customized to a class object with the purpose of ease of usage
- `extract_data.py` show some examples of how to interact data with Mongodb e.g. update, query, aggregation

