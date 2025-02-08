from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Homepage
@app.route('/')
def home():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['role'] = user['role']
        if user['role'] == 'student':
            return redirect(url_for('student_dashboard'))
        elif user['role'] == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        elif user['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
    else:
        return "Invalid credentials!"

# Student Dashboard
@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM seating_arrangement WHERE student_id = %s", (session['user_id'],))
    seating_info = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('student_dashboard.html', seating_info=seating_info)

# Teacher Dashboard
@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM teachers WHERE id = %s", (session['user_id'],))
    teacher_info = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('teacher_dashboard.html', teacher_info=teacher_info)

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    return render_template('admin_dashboard.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)