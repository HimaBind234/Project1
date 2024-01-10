import mysql.connector
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'HIMA@BINDU123',
    'database': 'Task',
}


connection = mysql.connector.connect(**db_config)

cursor = connection.cursor()

