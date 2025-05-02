
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3

app = Flask(__name__, template_folder='src/templates')
app.config['SECRET_KEY'] = 'your secret key'
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/courses')
def courses():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()

    return render_template('courses.html', courses=courses)


@app.route('/course/<course_code>')
def course_detail(course_code):
    with get_db_connection() as conn:
        course = conn.execute('SELECT * FROM courses WHERE course_code = ?', (course_code,)).fetchone()
        
        if not course:
            abort(404)
            
        # Get department name
        department = conn.execute('SELECT department_name FROM departments WHERE department_id = ?', 
                                 (course['department_id'],)).fetchone()
        department_name = department['department_name'] if department else "Unknown Department"
        
        # Get reviews with professor names
        reviews = conn.execute('''
            SELECT r.*, p.name as professor_name
            FROM reviews r
            LEFT JOIN professors p ON r.professor_id = p.professor_id
            WHERE r.course_code = ?
        ''', (course_code,)).fetchall()
        
    return render_template('course_detail.html', 
                          course=course, 
                          reviews=reviews, 
                          department_name=department_name)

@app.route('/course/<course_code>/add_review', methods=('GET', 'POST')) 
def add_review(course_code):
    with get_db_connection() as conn:
        # Get course details
        course = conn.execute('SELECT * FROM courses WHERE course_code = ?', 
                             (course_code,)).fetchone()
        
        if not course:
            abort(404)
            
        # Get professors who teach this course
        professors = conn.execute('''
            SELECT p.professor_id, p.name
            FROM professors p
            JOIN course_professors cp ON p.professor_id = cp.professor_id
            WHERE cp.course_code = ?
        ''', (course_code,)).fetchall()
        
        if request.method == 'POST':
            comments = request.form['comments']
            difficulty_rating = request.form['difficulty_rating']
            professor_rating = request.form['professor_rating']
            professor_id = request.form['professor_id']
            
            # Insert review with professor_id
            conn.execute('''
                INSERT INTO reviews (course_code, student_id, professor_id, comments, 
                                   difficulty_rating, professor_rating)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (course_code, 1, professor_id, comments, difficulty_rating, professor_rating))
            
            conn.commit()
            return redirect(url_for('course_detail', course_code=course_code))

    return render_template('add_review.html', 
                          course_code=course_code, 
                          course_name=course['course_name'],
                          professors=professors)





if __name__ == '__main__':
    app.run(debug=True)
