import os
import pymysql


SDB_HOST = os.getenv("SDB_HOST")
SDB_DATABASE_USER = os.getenv("SDB_DATABASE_USER")
SDB_DATABASE_PASSWORD = os.getenv("SDB_DATABASE_PASSWORD")
SDB_DATABASE_NAME = os.getenv("SDB_DATABASE_NAME")

# mysql connection
connection = pymysql.connect(
    host=SDB_HOST, user=SDB_DATABASE_USER, passwd=SDB_DATABASE_PASSWORD, db=SDB_DATABASE_NAME, port=3306
)