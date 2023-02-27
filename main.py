import boto3
import datetime
import json
import subprocess
import base64
import psycopg2

##  Postgres credentials
username = 'postgres'
password = 'postgres'
database = 'postgres'

## AWS que url 
url = 'http://localhost:4566/000000000000/login-queue'
max_msg = 1

## Functions for encoding and decoding PII data into base16 strings
def mask_string(s):
    return base64.b16encode(s.encode('ascii')).decode('utf-8')

def unmask_string(s):
    return base64.b16decode(s.encode('ascii')).decode('utf-8')

## setting query string
max_query='--max-number-of-messages '+str(max_msg)
query ='awslocal sqs receive-message --queue-url' + ' ' + url + ' '+max_query

## using awslocal to read message from queue 
out = subprocess.check_output(query, shell=True)

## processing output
messages = json.loads(out)['Messages']

## encoding PII data into base 16 strings
msg_encoded=[]
for msg in messages:
    body = json.loads(messages[0]['Body'])
    masked_ip = mask_string(body['ip'])
    masked_devId = mask_string(body['device_id'])
    body['ip'], body['device_id'] = masked_ip, masked_devId
    msg_encoded.append(body)

## Connecting to database using psycopg2 driver
conn = psycopg2.connect(dbname=database, user=username, password=password, port='5432')
cursor=conn.cursor()
create_comm = '''CREATE TABLE IF NOT EXISTS user_logins(
user_id varchar(128),
device_type varchar(32),
masked_ip varchar(256),
masked_device_id varchar(256),
locale varchar(32),
app_version integer,
create_date date
)'''
cursor.execute(create_comm)

## Inserting recieved message data into table in DB
for msg in msg_encoded:
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute('''INSERT INTO user_logins ( user_id, 
                    
                    device_type, 
                    masked_ip,
                    masked_device_id,  
                    locale, 
                    app_version,
                    create_date,  
                    VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                    msg['user_id'],
                    msg['device_type'],
                    msg['masked_ip'],
                    msg['masked_device_id'],
                    msg['locale'],
                    msg['app_version'],
                    msg['create_date'] )
    conn.commit()

conn.close()


