import mysql.connector

# Connect to MySQL server (without specifying database yet)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sanithya@10"
)
cursor = conn.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS campus_events")
cursor.execute("USE campus_events")

# Create Colleges Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS colleges (
    college_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
)
""")

# Create Students Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE,
    college_id INT,
    FOREIGN KEY (college_id) REFERENCES colleges(college_id)
)
""")

# Create Events Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    type ENUM('Hackathon','Workshop','Seminar','Fest','TechTalk','Other') NOT NULL DEFAULT 'Other',
    date DATE NOT NULL,
    college_id INT,
    created_by VARCHAR(100),
    FOREIGN KEY (college_id) REFERENCES colleges(college_id)
)
""")

# Create Registrations Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    event_id INT,
    UNIQUE(student_id, event_id), -- prevent duplicate registrations
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
)
""")

# Create Attendance Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    att_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    event_id INT,
    status ENUM('present','absent') DEFAULT 'absent',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
)
""")

# Create Feedback Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    fb_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    event_id INT,
    rating INT CHECK(rating BETWEEN 1 AND 5),
    comments VARCHAR(250),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
)
""")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("Database and all tables created successfully!")
