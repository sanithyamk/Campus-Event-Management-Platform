import mysql.connector
import random

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sanithya@10",
    database="campus_events"
)
cursor = conn.cursor()


# 1) Get all students and events

cursor.execute("SELECT student_id, college_id FROM students")
students = cursor.fetchall()  # [(student_id, college_id), ...]

cursor.execute("SELECT event_id, college_id FROM events")
events = cursor.fetchall()  # [(event_id, college_id), ...]


# 2) Register students to events in their college

registrations = []
for student_id, college_id in students:
    # Register each student to 1-3 random events from their college
    college_events = [eid for eid, ecid in events if ecid == college_id]
    chosen_events = random.sample(college_events, k=min(len(college_events), random.randint(1, 3)))
    for eid in chosen_events:
        registrations.append((student_id, eid))

# Insert registrations (ignore duplicates)
for student_id, event_id in registrations:
    try:
        cursor.execute("INSERT INTO registrations (student_id, event_id) VALUES (%s, %s)", (student_id, event_id))
    except mysql.connector.IntegrityError:
        pass  # already registered


# 3) Mark attendance randomly

cursor.execute("SELECT reg_id, student_id, event_id FROM registrations")
all_regs = cursor.fetchall()  # [(reg_id, student_id, event_id), ...]

for _, student_id, event_id in all_regs:
    status = random.choice(['present', 'absent'])
    cursor.execute("INSERT INTO attendance (student_id, event_id, status) VALUES (%s, %s, %s)",
                   (student_id, event_id, status))


# 4) Give feedback randomly (only for students who attended)

cursor.execute("SELECT student_id, event_id FROM attendance WHERE status='present'")
attended = cursor.fetchall()

for student_id, event_id in attended:
    rating = random.randint(1, 5)
    comments = f"Feedback rating {rating}"
    cursor.execute("INSERT INTO feedback (student_id, event_id, rating, comments) VALUES (%s, %s, %s, %s)",
                   (student_id, event_id, rating, comments))

# Commit changes and close
conn.commit()
cursor.close()
conn.close()

print("Students registered, attendance marked, and feedback submitted successfully!")
