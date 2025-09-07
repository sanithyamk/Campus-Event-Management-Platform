"Campus Event Management System" 
This project implements a Campus Event Management system that displays all registered events for each student using a unique ID. Students can mark their attendance as present and also submit feedback by rating events from 1 to 5
   Admin Role:
The system allows college administrators to create and manage events such as workshops, hackathons, seminars, and cultural fests. Each event is linked to a specific college, and administrators can view, edit, or cancel events as needed. This ensures that all event-related data is structured and accessible for reporting purposes.
   Student Role:
Students who registered for events using their unique student ID.They can view a list of their registered events, mark their attendance as present on the event day, and submit feedback by rating events from 1 to 5. This provides real-time tracking of participation and satisfaction.
   Database Tracking:
The backend database stores all essential data including students, events, registrations, attendance, and feedback. Constraints like unique registration prevent duplicate entries, ensuring data integrity. This structured storage allows efficient generation of reports and analytics.
   Reports & Analytics:
Student Participation Report: Shows how many events each student attended.
Top 3 Active Students: Highlights students with the highest attendance, helping staff monitor engagement.
   "Technologies Used"
- Database: MySQL
- Backend: Node.js + Express
- Frontend: HTML, CSS, JavaScript
- Python (for DB setup script)
    To check the backend is running use this
 1)(node server.js) : It will help to start your backend server (built using Node.js + Express).
It connects to MySQL (your database).
It listens on a port (3000 in my case).
    It provides API endpoints :The system provides API endpoints that query MySQL and return data in JSON format for student participation, top active students, event feedback, and event filtering by type
  1)http://localhost:3000/reports/student-participation
2)http://localhost:3000/reports/top-students
3)http://localhost:3000/reports/feedback
4)http://localhost:3000/reports/events-by-type/Workshop

    HOW TO RUN THIS
  pip install mysql-connector-python : This is for Python projects, It installs the MySQL Connector library so Python can connect to a MySQL database.
  npm install express mysql2 cors body-parser : This is for Node.js projects
  >> python step1_setup.py
  >> python step2_seed.py
  >>  python step3_populate_activity.py
  >> npm init -y                                         
>>  npm install -g live-server
>> start index.html
   TO RUN and SEE THE OUTPUT 
>>cd C:\webknot\campus_events\frontend
>> live-server  (it will the output )
>> cd C:\webknot\campus_events
>> node server.js (it will connect with backend it has to run to get the frontend)
Server running on http://localhost:3000
    TO push all the code to github without missing any code 
git remote add origin https://github.com/sanithyamk/Campus-Event-Management-Platform.git
>> git branch -M main
>> git push -u origin main

