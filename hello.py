import mysql.connector
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'HIMA@BINDU123',
    'database': 'Task',
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

user_data = {
    'username': 'john',
    'password': 'john123',
    'full_name': 'John',
    'email': 'johndoe@gmail.com',
}

user_data2 = {
    'username': 'jane',
    'password': 'jane234',
    'full_name': 'Jane',
    'email': 'janesmith@gmail.com',
}


sql = "INSERT INTO users (username, password,full_name, email) VALUES (%s, %s, %s,%s)"


cursor.execute(sql, (user_data['username'], user_data['password'],user_data['full_name'], user_data['email']))

cursor.execute(sql, (user_data2['username'], user_data2['password'],user_data2['full_name'], user_data2['email']))


connection.commit()


cursor.close()
connection.close()