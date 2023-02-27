# Fetch #
## Data Engineering Take Home: ETL off a SQS Qeueue ##

This is the solution for this assignment:
https://fetch-hiring.s3.amazonaws.com/data-engineer/pii-masking.pdf

This assignment has been completed using python 3.9. The first objective, to read JSON data containing user login information from an AWS SQS queue was done using AWSCLI-local. The command was generated in python and the response further processed. The PII fields (deviceID and IP) were maskedd using a simple base16 encoding which should make ie easy for analysts to identify duplicates. Finally, the driver from psycopg2 was used to establish a connection to the postgres database and the messages from the queue are written into the tables.

## To run the code
1. Clone this repo.
```bash
git clone https://github.com/tapanr25/Fetch-assignment.git
```

2. Go into the cloned repo.
```bash
cd Fetch-assignment
```
3. Install postgressql client
```bash
apt install postgresql-client
```
4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Start docker images 
```bash
docker-compose up
```

6. Run the python script to run the application
```bash
python main.py
```

7. Stop docker images 
```bash
docker-compose down
```

## To checking the table in postgres

```bash
psql -d postgres -U postgres -p 5432 -h localhost -W
```
    - **password**=`postgres`
