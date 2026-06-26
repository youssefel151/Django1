import mysql.connector

database=mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '123',
)

CursorObject=database.cursor()

CursorObject.execute('CREATE DATABASE db_crm')

print('Bien faitt !!')