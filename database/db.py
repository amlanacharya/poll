import sqlite3
import os
import pandas as pd

DATABASE_NAME = 'myth_fact_poll.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()

    # Students table create
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mobile_number TEXT NOT NULL UNIQUE,
        email TEXT UNIQUE
    )
    ''')

    # Polls table create    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS polls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT 0
    )
    ''')

    # Options table create  
    cur.execute('''
    CREATE TABLE IF NOT EXISTS options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        poll_id INTEGER,
        option_text TEXT NOT NULL,
        FOREIGN KEY (poll_id) REFERENCES polls (id)
    )
    ''')

    # Votes table create    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        poll_id INTEGER,
        student_id INTEGER,
        option_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (poll_id) REFERENCES polls (id),
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (option_id) REFERENCES options (id)
    )
    ''')

    conn.commit()
    conn.close()

def add_student(name, mobile_number, email):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO students (name, mobile_number, email) VALUES (?, ?, ?)',
                    (name, mobile_number, email))
        conn.commit()
        student_id = cur.lastrowid
        return student_id
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: students.mobile_number" in str(e):
            raise ValueError("A student with this mobile number already exists.")
        else:
            raise ValueError(f"An error occurred while adding the student: {str(e)}")
    finally:
        conn.close()

def get_active_poll():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM polls WHERE is_active = 1')
    poll = cur.fetchone()
    conn.close()
    return poll

def get_poll_options(poll_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, option_text FROM options WHERE poll_id = ?', (poll_id,))
    options = [{'id': row['id'], 'option_text': row['option_text']} for row in cur.fetchall()]
    conn.close()
    return options

def add_vote(poll_id, student_id, option_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO votes (poll_id, student_id, option_id) VALUES (?, ?, ?)',
                (poll_id, student_id, option_id))
    conn.commit()
    conn.close()

def get_poll_results(poll_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
    SELECT o.option_text, COUNT(v.id) as vote_count
    FROM options o
    LEFT JOIN votes v ON o.id = v.option_id
    WHERE o.poll_id = ?
    GROUP BY o.id
    ''', (poll_id,))
    results = cur.fetchall()
    conn.close()
    return results

def get_all_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, mobile_number, email FROM students')
    students = cur.fetchall()
    conn.close()
    return students
