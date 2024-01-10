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
        INSERT INTO time_logs ( task_id,start_time, end_time, duration_minutes, notes)
        VALUES (%s, %s, %s, %s, %s)
    """

time_logs_data = [
    (3,'2024-01-02 08:00:00', '2024-01-02 09:30:00', 90, 'Working on project A'),
    (4,'2024-01-02 10:00:00', '2024-01-02 12:00:00', 120, 'Meeting with team'),
    (10,'2024-01-02 10:20:00','2024-01-02 12:20:00', 60,'created logout button'),
    
    ]
cursor.executemany(insert_query, time_logs_data)
connection.commit()