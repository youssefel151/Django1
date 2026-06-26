import mysql.connector

database=mysql.connector.connect(
    host = 'localhost',
    user = 'user',
    password = '123',
)

CursorObject.databases.cursor()
CursorObject.execute('CREATE DATABASE db_crm')

print('Bien faitt !!')