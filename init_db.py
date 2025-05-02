import sqlite3

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

# Insert sample students
cur.execute("INSERT INTO students (student_id, name, academic_details) VALUES (1, 'Alice Smith', 'Senior')")
cur.execute("INSERT INTO students (student_id, name, academic_details) VALUES (2, 'Bob Johnson', 'Junior')")

# Insert sample professors
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Alan Turing')")
cur.execute("INSERT INTO professors (name) VALUES ('Dr. Ada Lovelace')")

# Insert sample courses
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('CS101', 'Intro to Computer Science', 1)")
cur.execute("INSERT INTO courses (course_code, course_name, department_id) VALUES ('MATH201', 'Calculus II', 2)")

# Associate professors with courses
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('CS101', 1)")
cur.execute("INSERT INTO course_professors (course_code, professor_id) VALUES ('MATH201', 2)")

# Insert sample performance data
cur.execute("INSERT INTO performance (student_id, course_code, score, grade, attendance) VALUES (1, 'CS101', 92.5, 'A-', 95.0)")
cur.execute("INSERT INTO performance (student_id, course_code, score, grade, attendance) VALUES (2, 'MATH201', 85.0, 'B+', 87.0)")

# Insert sample reviews
cur.execute("INSERT INTO reviews (student_id, course_code, difficulty_rating, professor_rating, comments) VALUES (1, 'CS101', 7.5, 9, 'Great intro course!')")
cur.execute("INSERT INTO reviews (student_id, course_code, difficulty_rating, professor_rating, comments) VALUES (2, 'MATH201', 6.0, 8, 'Challenging but rewarding.')")

# Insert sample tags
cur.execute("INSERT INTO tags (tag_name) VALUES ('Challenging')")
cur.execute("INSERT INTO tags (tag_name) VALUES ('Recommended')")

# Tag reviews
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (1, 2)")  # Review 1 tagged as Recommended
cur.execute("INSERT INTO review_tags (review_id, tag_id) VALUES (2, 1)")  # Review 2 tagged as Challenging

#Insert sample post
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", ('First post', 'This is the content of the first post.'))
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", ('Second post', 'Here is the content of my second post.'))

# Commit and close
connection.commit()
connection.close()
