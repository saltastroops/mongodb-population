import os
from pymysql import connect


SDB_HOST = os.environ["SDB_HOST"]
SDB_DATABASE_USER = os.getenv("SDB_DATABASE_USER")
SDB_DATABASE_PASSWORD = os.getenv("SDB_DATABASE_PASSWORD")
SDB_DATABASE_NAME = os.getenv("SDB_DATABASE_NAME")

# mysql connection

print(SDB_HOST, SDB_DATABASE_PASSWORD)
connection = connect(
    host=SDB_HOST, user=SDB_DATABASE_USER, passwd=SDB_DATABASE_PASSWORD, db=SDB_DATABASE_NAME, port=3306
)
# def connection():
#     return connect(**sql_config)