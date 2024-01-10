import mysql.connector
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'HIMA@BINDU123',
    'database': 'Task',
}


connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()
insert_query = """
        INSERT INTO projects ( project_name, description)
        VALUES (%s, %s)
    """


projects_data = [
    ('create hackerrank webpage','To create a hackerrank page containing login details'),
    ('creating login page','To create a user login page'),
    
    ]

cursor.executemany(insert_query, projects_data)
connection.commit()