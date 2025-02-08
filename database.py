import mysql.connector

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="seating_system"
    )

# Create tables if they don't exist
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL,
            role ENUM('student', 'teacher', 'admin') NOT NULL
        )
    """)

    # Create Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            class VARCHAR(50) NOT NULL
        )
    """)

    # Create Teachers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            class_assigned VARCHAR(50)
        )
    """)

    # Create Seating Arrangement table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seating_arrangement (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            teacher_id INT,
            class VARCHAR(50),
            seat_number INT,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Call this function to initialize the database
initialize_db()