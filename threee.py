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
        INSERT INTO task_categories ( category_name)
        VALUES (%s)
    """

category_data = [
    ('create  webpages',),
    ('creating login pages',),
    
    ]
cursor.executemany(insert_query, category_data)
connection.commit()