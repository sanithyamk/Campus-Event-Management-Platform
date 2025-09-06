import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import pool from './db.js';

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Home route
app.get('/', (req, res) => {
  res.send('Campus Event Management API is running! Use the /reports endpoints.');
});

// 1) Event Popularity Report

app.get('/reports/event-popularity', async (req, res) => {
  const [rows] = await pool.query(`
    SELECT e.event_id, e.name AS event_name, c.name AS college_name, COUNT(r.reg_id) AS total_registrations
    FROM events e
    JOIN colleges c ON e.college_id = c.college_id
    LEFT JOIN registrations r ON e.event_id = r.event_id
    GROUP BY e.event_id
    ORDER BY total_registrations DESC
  `);
  res.json(rows);
});


// 2) Student Participation Report

app.get('/reports/student-participation', async (req, res) => {
  const [rows] = await pool.query(`
    SELECT s.student_id, s.name AS student_name, c.name AS college_name, 
           COUNT(a.att_id) AS events_attended
    FROM students s
    JOIN colleges c ON s.college_id = c.college_id
    LEFT JOIN attendance a ON s.student_id = a.student_id AND a.status='present'
    GROUP BY s.student_id
    ORDER BY events_attended DESC
  `);
  res.json(rows);
});


// 3) Top 3 Most Active Students

app.get('/reports/top-students', async (req, res) => {
  const [rows] = await pool.query(`
    SELECT s.student_id, s.name AS student_name, COUNT(a.att_id) AS events_attended
    FROM students s
    JOIN attendance a ON s.student_id = a.student_id AND a.status='present'
    GROUP BY s.student_id
    ORDER BY events_attended DESC
    LIMIT 3
  `);
  res.json(rows);
});

// 4) Average Feedback Score

app.get('/reports/feedback', async (req, res) => {
  const [rows] = await pool.query(`
    SELECT e.event_id, e.name AS event_name, AVG(f.rating) AS avg_feedback
    FROM events e
    LEFT JOIN feedback f ON e.event_id = f.event_id
    GROUP BY e.event_id
    ORDER BY avg_feedback DESC
  `);
  res.json(rows);
});


// 5) Flexible Report (Filter by Event Type)

app.get('/reports/events-by-type/:type', async (req, res) => {
  const { type } = req.params;
  const [rows] = await pool.query(`
    SELECT e.event_id, e.name AS event_name, e.type, COUNT(r.reg_id) AS total_registrations
    FROM events e
    LEFT JOIN registrations r ON e.event_id = r.event_id
    WHERE e.type = ?
    GROUP BY e.event_id
    ORDER BY total_registrations DESC
  `, [type]);
  res.json(rows);
});
// Get registered events for a student
app.get('/my-registrations/:student_id', async (req, res) => {
  const { student_id } = req.params;
  const [rows] = await pool.query(`
    SELECT e.event_id, e.name, e.date
    FROM events e
    JOIN registrations r ON e.event_id = r.event_id
    WHERE r.student_id = ?
  `, [student_id]);
  res.json(rows);
});

// Mark attendance
app.post('/attendance', async (req, res) => {
  const { student_id, event_id, status } = req.body;
  try {
    await pool.query(`
      INSERT INTO attendance (student_id, event_id, status)
      VALUES (?, ?, ?)
      ON DUPLICATE KEY UPDATE status=VALUES(status)
    `, [student_id, event_id, status]);
    res.json({ success: true, message: 'Attendance marked!' });
  } catch (err) {
    res.json({ success: false, message: err.message });
  }
});

// Submit feedback
app.post('/feedback', async (req, res) => {
  const { student_id, event_id, rating, comments } = req.body;
  try {
    await pool.query(`
      INSERT INTO feedback (student_id, event_id, rating, comments)
      VALUES (?, ?, ?, ?)
      ON DUPLICATE KEY UPDATE rating=VALUES(rating), comments=VALUES(comments)
    `, [student_id, event_id, rating, comments]);
    res.json({ success: true, message: 'Feedback submitted!' });
  } catch (err) {
    res.json({ success: false, message: err.message });
  }
});


app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
