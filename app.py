from flask import *
from config import *
from flask_bcrypt import Bcrypt
app=Flask(__name__)

app.secret_key = "AGSFDJ68424KJGD34SDKHF3434DJKJ"
bcrypt = Bcrypt(app)

@app.route('/create')
def home():
    cursor.execute("SELECT  user_id,username FROM users")
    users = cursor.fetchall()
    
    cursor.execute("SELECT  project_id,project_name FROM projects")
    projects = cursor.fetchall()
    
    cursor.execute("SELECT  category_id,category_name FROM task_categories")
    task_categories = cursor.fetchall()
    

    return render_template('tasks.html',users=users,projects=projects,task_categories=task_categories)

@app.route('/create_task', methods=['POST'])
def create_task():
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        description = request.form.get('description')
        status = request.form.get('status')
        project_id = request.form.get('project_id')
        category_id = request.form.get('category_id')
        created_by = request.form.get('created_by')
        assigned_to = request.form.get('assigned_to')


        cursor.execute("INSERT INTO tasks (task_name, description, status, project_id,category_id,  created_by, assigned_to) VALUES (%s, %s, %s, %s, %s,%s,%s)",
                       (task_name, description, status,project_id,category_id, created_by, assigned_to))
        cursor.execute("INSERT INTO tasks_backup (task_name, description, status, created_by, assigned_to) VALUES (%s, %s, %s, %s, %s)",
                       (task_name, description, status, created_by, assigned_to))
        connection.commit()

       

        return redirect(url_for('display_tasks'))
    cursor.execute("SELECT  user_id,username FROM users")
    users = cursor.fetchall()
    
    cursor.execute("SELECT  project_id,project_name FROM projects")
    projects = cursor.fetchall()
    
    cursor.execute("SELECT  category_id,category_name FROM task_categories")
    task_categories = cursor.fetchall()
    

    return render_template('tasks.html',users=users,projects=projects,task_categories=task_categories)
    


@app.route('/')
def display_tasks():
    query='''
    SELECT
    tasks.task_id,
    tasks.task_name,
    tasks.description,
    tasks.status,
    tasks.priority,
    tasks.due_date,
    tasks.estimation_hours,
    projects.project_name,
    task_categories.category_name,
    created_by_user.full_name AS created_by_user_name,
    assigned_to_user.full_name AS assigned_to_user_name
FROM
    tasks
JOIN
    projects ON tasks.project_id = projects.project_id
JOIN
    task_categories ON tasks.category_id = task_categories.category_id
JOIN
    users AS created_by_user ON tasks.created_by = created_by_user.user_id
LEFT JOIN
    users AS assigned_to_user ON tasks.assigned_to = assigned_to_user.user_id;
    '''
    cursor.execute(query)
    tasks = cursor.fetchall()
    return render_template('display_tasks.html', tasks=tasks)

@app.route('/edit/<int:task_id>',methods=['GET','POST'])
def edit_task(task_id):
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        description = request.form.get('description')
        status = request.form.get('status')
        project_id = request.form.get('project_id')
        category_id = request.form.get('category_id')
        created_by = request.form.get('created_by')
        assigned_to = request.form.get('assigned_to')

        cursor.execute("UPDATE tasks SET task_name=%s, description=%s, status=%s, project_id=%s, category_id=%s, created_by=%s, assigned_to=%s WHERE task_id=%s", (task_name, description, status,project_id, category_id, created_by, assigned_to, task_id))
        connection.commit()

        return redirect(url_for('display_tasks'))

    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    tasks = cursor.fetchone()
    cursor.execute("SELECT user_id, username FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT  project_id,project_name FROM projects")
    projects = cursor.fetchall()
    
    cursor.execute("SELECT  category_id,category_name FROM task_categories")
    task_categories = cursor.fetchall()
    
    


    return render_template('edit_task.html', tasks=tasks, users=users,projects=projects,task_categories=task_categories)



@app.route('/timelog/<int:task_id>',methods=['GET','POST'])
def time_log(task_id):
    if request.method == 'GET':


        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        tasks = cursor.fetchone()

        cursor.execute("SELECT * FROM time_logs WHERE task_id = %s", (task_id,))
        time_logs = cursor.fetchall()


        return render_template('timelogs.html', tasks=tasks,time_logs=time_logs)

@app.route('/create_time_log/<int:task_id>', methods=['POST'])
def create_time_log(task_id):
    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        duration_minutes = request.form['duration']
        notes = request.form['notes']
        cursor.execute("INSERT INTO time_logs (task_id, start_time, end_time, duration_minutes,notes) VALUES (%s, %s, %s, %s,%s)",
                       (task_id, start_time, end_time, duration_minutes,notes))
        connection.commit()
        return redirect(url_for('time_log', task_id=task_id))
    
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        entered_password = request.form['password']
        sql = "SELECT password FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()

        if result and bcrypt.check_password_hash(result[0], entered_password):
            sql_update = "UPDATE users SET authenticate = TRUE WHERE username = %s"
            cursor.execute(sql_update, (username,))
            connection.commit()
            session['username'] = request.form['username']
            return redirect('/user')
        else:
            return "Invalid username or password"

    return render_template('login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        full_name = request.form['full_name']
        email = request.form['email']

        sql = "INSERT INTO users (username, password, full_name, email) VALUES (%s, %s, %s, %s)"
        values = (username, password, full_name, email)

        cursor.execute(sql, values)
        connection.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/user', methods=['GET'])
def homes():
    if not is_admin():
        return redirect(url_for('user_group'))
    query='''SELECT
    users.user_id,
    users.username,
    users.full_name,
    users.email,
    users.authenticate,
    users.active,
    users.created_at,
    users.updated_at,
    GROUP_CONCAT(`groups`.group_name) AS user_groups
FROM
    users
LEFT JOIN
    user_groups ON users.user_id = user_groups.user_id
LEFT JOIN
    `groups` ON user_groups.group_id = `groups`.group_id
GROUP BY
    users.user_id;'''
    
    cursor.execute(query)
    users = cursor.fetchall()
    return render_template('user_list.html', users=users)

@app.route('/edits/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        user_name = request.form['user_name']
        full_name = request.form['full_name']
        email = request.form['email']
        active = request.form['active']
        sql_update_user = "UPDATE users SET username = %s, full_name = %s, email = %s, active = %s WHERE user_id = %s"
        update_values = (user_name, full_name, email, active, user_id)

        cursor.execute(sql_update_user, update_values)
        connection.commit()

        return redirect('/user')

    sql_select_user = "SELECT user_id, username, full_name, email, active FROM users WHERE user_id = %s"
    cursor.execute(sql_select_user, (user_id,))
    users = cursor.fetchone()

    return render_template('edit_user.html', users=users)

@app.route('/deactivate_user/<int:user_id>')
def deactivate_user(user_id):
    sql_deactivate_user = "UPDATE users SET active = 0 WHERE user_id = %s"
    cursor.execute(sql_deactivate_user, (user_id,))
    connection.commit()
    
    return redirect(url_for('homes'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/assign_role/<int:user_id>', methods=['POST'])
def assign_role(user_id):
    if request.method == 'POST':
        role_manager = 'role_manager' in request.form
        role_employee = 'role_employee' in request.form
        role_admin = 'role_admin' in request.form

        roles = []

        if role_manager:
            roles.append('Manager')
        if role_employee:
            roles.append('Employee')
        if role_admin:
            roles.append('Admin')

        update_roles_query = "DELETE FROM user_groups WHERE user_id = %s"
        cursor.execute(update_roles_query, (user_id,))

        if roles:
            get_group_ids_query = "SELECT group_id FROM `groups` WHERE group_name IN (" + ",".join(["%s"] * len(roles)) + ")"
            cursor.execute(get_group_ids_query, roles)
            group_ids = [result[0] for result in cursor.fetchall()]
            insert_roles_query = "INSERT INTO user_groups (user_id, group_id) VALUES (%s, %s)"
            for group_id in group_ids:
                cursor.execute(insert_roles_query, (user_id, group_id))

            connection.commit()

    return redirect('/user')

def is_admin():
    if 'username' in session:
        username = session['username']
        sql = "SELECT COUNT(*) FROM user_groups ug JOIN `groups` g ON ug.group_id = g.group_id WHERE ug.user_id = (SELECT user_id FROM users WHERE username = %s) AND g.group_name = 'Admin'"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        return result[0] > 0
    return False





@app.route('/usergroup', methods=['GET'])
def user_group():

      
        


       return render_template('user_group.html')




if __name__=='__main__':
    app.run(debug=True)