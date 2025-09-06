import mysql.connector
from datetime import date, timedelta

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sanithya@10",
    database="campus_events"
)
cursor = conn.cursor()


# 1) Insert sample colleges

colleges = [
    ('Tech University',),
    ('Innovation College',)
]

cursor.executemany("""
INSERT INTO colleges (name) VALUES (%s)
""", colleges)

# Get inserted college IDs
cursor.execute("SELECT college_id, name FROM colleges")
college_rows = cursor.fetchall()
college_dict = {name: cid for cid, name in college_rows}


# 2) Insert sample students

students = [
    ('Alice', 'alice@tech.edu', college_dict['Tech University']),
    ('Bob', 'bob@tech.edu', college_dict['Tech University']),
    ('Charlie', 'charlie@tech.edu', college_dict['Tech University']),
    ('David', 'david@innovation.edu', college_dict['Innovation College']),
    ('Eva', 'eva@innovation.edu', college_dict['Innovation College']),
    ('Frank', 'frank@innovation.edu', college_dict['Innovation College'])
]

cursor.executemany("""
INSERT INTO students (name, email, college_id) VALUES (%s, %s, %s)
""", students)


# 3) Insert sample events

today = date.today()
events = [
    # Tech University
    ('AI Workshop', 'Workshop', today + timedelta(days=5), college_dict['Tech University'], 'Admin1'),
    ('Hackathon 2025', 'Hackathon', today + timedelta(days=10), college_dict['Tech University'], 'Admin1'),
    ('Tech Fest', 'Fest', today + timedelta(days=15), college_dict['Tech University'], 'Admin2'),

    # Innovation College
    ('Robotics Seminar', 'Seminar', today + timedelta(days=7), college_dict['Innovation College'], 'Admin3'),
    ('Innovation Hackathon', 'Hackathon', today + timedelta(days=12), college_dict['Innovation College'], 'Admin3'),
    ('Cultural Fest', 'Fest', today + timedelta(days=18), college_dict['Innovation College'], 'Admin4')
]

cursor.executemany("""
INSERT INTO events (name, type, date, college_id, created_by) 
VALUES (%s, %s, %s, %s, %s)
""", events)

# Commit changes and close
conn.commit()
cursor.close()
conn.close()

print("Sample colleges, students, and events inserted successfully!")
