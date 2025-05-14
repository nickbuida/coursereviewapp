import sqlite3
import hashlib

# Connect to database
connection = sqlite3.connect('database.db')

# Create tables from schema
with open('schema.sql', 'rb') as f:
    schema_content = f.read()
    connection.executescript(schema_content.decode('utf-8'))

cur = connection.cursor()

# Insert sample departments
cur.execute("INSERT INTO departments (department_name) VALUES ('Computer Science')")
cur.execute("INSERT INTO departments (department_name) VALUES ('Mathematics')")
cur.execute("INSERT INTO departments (department_name) VALUES ('Physics')")
cur.execute("INSERT INTO departments (department_name) VALUES ('Business')")
cur.execute("INSERT INTO departments (department_name) VALUES ('Psychology')")
cur.execute("INSERT INTO departments (department_name) VALUES ('English')")
cur.execute("INSERT INTO departments (department_name) VALUES ('Biology')")
cur.execute("INSERT INTO departments (department_name) VALUES ('Chemistry')")

# Create users first (moved up from bottom of file)
cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
            ('alice', hashlib.sha256('password'.encode()).hexdigest(), 'alice@example.com'))
cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
            ('bob', hashlib.sha256('student123'.encode()).hexdigest(), 'bob@example.com'))
cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
            ('demo', hashlib.sha256('password'.encode()).hexdigest(), 'demo@example.com'))

# Insert sample students with user_id relationship
cur.execute("INSERT INTO students (student_id, user_id, name, academic_details) VALUES (1, 1, 'Alice Smith', 'Senior')")  # Alice is user_id 1
cur.execute("INSERT INTO students (student_id, user_id, name, academic_details) VALUES (2, 2, 'Bob Johnson', 'Junior')")  # Bob is user_id 2
cur.execute("INSERT INTO students (student_id, user_id, name, academic_details) VALUES (3, 3, 'Demo User', 'Graduate')")  # Demo is user_id 3

# Insert sample professors
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Alan Turing')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Ada Lovelace')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Marie Curie')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Richard Feynman')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Grace Hopper')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Charles Darwin')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Jane Goodall')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Stephen Hawking')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Rosalind Franklin')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Carl Sagan')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Barbara McClintock')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Albert Einstein')")

# Insert sample courses
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('CS101', 'Intro to Computer Science', 1)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('CS201', 'Data Structures', 1)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('CS310', 'Database Systems', 1)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('CS350', 'Software Engineering', 1)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('MATH201', 'Calculus II', 2)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('MATH101', 'College Algebra', 2)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('MATH315', 'Linear Algebra', 2)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('PHYS101', 'Intro to Physics', 3)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('PHYS220', 'Quantum Mechanics', 3)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('BUS200', 'Principles of Management', 4)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('BUS350', 'Marketing Strategies', 4)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('PSYCH101', 'Intro to Psychology', 5)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('ENG210', 'Creative Writing', 6)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('BIO101', 'Introduction to Biology', 7)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('BIO335', 'Genetics', 7)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('CHEM101', 'General Chemistry', 8)")

# Associate professors with courses
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('CS101', 1)")  # Alan Turing - Intro to CS
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('MATH201', 2)")  # Ada Lovelace - Calculus II
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('CS201', 5)")  # Grace Hopper - Data Structures
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('CS310', 1)")  # Alan Turing - Database Systems
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('CS350', 5)")  # Grace Hopper - Software Engineering
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('PHYS101', 4)")  # Richard Feynman - Intro to Physics
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('PHYS220', 8)")  # Stephen Hawking - Quantum Mechanics
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('MATH101', 2)")  # Ada Lovelace - College Algebra
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('MATH315', 12)")  # Albert Einstein - Linear Algebra
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('BUS200', 5)")  # Grace Hopper - Principles of Management
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('BUS350', 5)")  # Grace Hopper - Marketing Strategies
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('PSYCH101', 7)")  # Jane Goodall - Intro to Psychology
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('ENG210', 10)")  # Carl Sagan - Creative Writing
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('BIO101', 6)")  # Charles Darwin - Intro to Biology
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('BIO335', 6)")  # Charles Darwin - Genetics
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('CHEM101', 3)")  # Marie Curie - General Chemistry
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('CS201', 1)")  # Alan Turing also teaches Data Structures
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('PHYS101', 12)")  # Einstein also teaches Intro to Physics

# Insert sample performance data
cur.execute("INSERT INTO performance (student_id, course_code, score, grade, attendance) VALUES (1, 'CS101', 92.5, 'A-', 95.0)")
cur.execute("INSERT INTO performance (student_id, course_code, score, grade, attendance) VALUES (2, 'MATH201', 85.0, 'B+', 87.0)")

# Insert sample reviews
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments) VALUES (1, 1, 'CS101', 7.5, 9, 'Great intro course! Dr. Turing explains concepts very clearly.')")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments) VALUES (2, 2, 'MATH201', 6.0, 8, 'Challenging but rewarding. Dr. Lovelace is very helpful during office hours.')")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments) VALUES (1, 5, 'CS201', 8.0, 9, 'Dr. Hopper is an amazing professor. The projects are challenging but you learn so much.')")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments) VALUES (2, 4, 'PHYS101', 7.0, 10, 'Dr. Feynman makes physics fascinating! His examples are always interesting.')")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments) VALUES (1, 12, 'PHYS101', 8.5, 7, 'Dr. Einstein is brilliant but sometimes hard to follow in lectures.')")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments) VALUES (2, 6, 'BIO101', 5.0, 8, 'Dr. Darwin makes biology accessible and interesting.')")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments) VALUES (3, 5, 'CS350', 7.5, 9, 'Great software engineering course! Very practical skills taught.')")

# Insert sample reviews with scores
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (1, 1, 'CS101', 7.5, 9, 'Great intro course! Dr. Turing explains concepts very clearly.', 92.5)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (2, 2, 'MATH201', 6.0, 8, 'Challenging but rewarding. Dr. Lovelace is very helpful during office hours.', 85.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (1, 5, 'CS201', 8.0, 9, 'Dr. Hopper is an amazing professor. The projects are challenging but you learn so much.', 88.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (2, 4, 'PHYS101', 7.0, 10, 'Dr. Feynman makes physics fascinating! His examples are always interesting.', 78.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (1, 12, 'PHYS101', 8.5, 7, 'Dr. Einstein is brilliant but sometimes hard to follow in lectures.', 91.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (2, 6, 'BIO101', 5.0, 8, 'Dr. Darwin makes biology accessible and interesting.', 82.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (3, 5, 'CS350', 7.5, 9, 'Great software engineering course! Very practical skills taught.', 89.0)")

# Add more sample reviews to ensure each professor has reviews for their courses
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (3, 1, 'CS310', 9.0, 10, 'Dr. Turing is a genius! Database Systems is a must-take course.', 95.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (1, 2, 'MATH101', 6.5, 8, 'Dr. Lovelace makes algebra fun and engaging.', 87.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (2, 2, 'MATH315', 7.0, 9, 'Linear Algebra is tough but rewarding. Dr. Lovelace is very supportive.', 84.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (3, 4, 'PHYS220', 8.0, 10, 'Quantum Mechanics is mind-blowing! Dr. Hawking is amazing.', 93.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (1, 10, 'ENG210', 5.0, 7, 'Creative Writing is a relaxing and enjoyable course.', 88.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (2, 3, 'CHEM101', 6.0, 8, 'General Chemistry is challenging but Dr. Curie is very helpful.', 80.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (3, 7, 'PSYCH101', 7.0, 9, 'Intro to Psychology is fascinating. Dr. Goodall is an excellent professor.', 85.0)")
cur.execute("INSERT INTO reviews (student_id, professor_id, course_code, difficulty_rating, professor_rating, comments, score) VALUES (1, 6, 'BIO335', 8.0, 9, 'Genetics is a tough course but Dr. Darwin makes it interesting.', 90.0)")

# Insert sample tags
cur.execute("INSERT INTO tags (tag_name) VALUES ('Challenging')")
cur.execute("INSERT INTO tags (tag_name) VALUES ('Recommended')")
cur.execute("INSERT INTO tags (tag_name) VALUES ('Easy')")
cur.execute("INSERT INTO tags (tag_name) VALUES ('Project-based')")
cur.execute("INSERT INTO tags (tag_name) VALUES ('Lecture-heavy')")
cur.execute("INSERT INTO tags (tag_name) VALUES ('Great Professor')")

# Tag reviews
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (1, 2)")  # Review 1 tagged as Recommended
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (2, 1)")  # Review 2 tagged as Challenging
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (3, 4)")  # Review 3 tagged as Project-based
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (3, 6)")  # Review 3 tagged as Great Professor
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (4, 2)")  # Review 4 tagged as Recommended
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (4, 6)")  # Review 4 tagged as Great Professor
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (5, 1)")  # Review 5 tagged as Challenging
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (6, 3)")  # Review 6 tagged as Easy
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (7, 4)")  # Demo user's review tagged as Project-based



# Commit and close
connection.commit()
connection.close()