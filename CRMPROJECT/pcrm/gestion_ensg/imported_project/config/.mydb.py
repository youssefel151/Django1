import mysql.connector

database=mysql.connector.connector(
    host='localhost',
    user='root',
    password='',

)

cursorDbject=database.cursor()

cursorDbject.execute("create DATABASE db_crm")

print("tout est bien")

