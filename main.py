
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
        reviews = conn.execute('SELECT * FROM reviews WHERE course_code = ?', (course_code,)).fetchall()
        
        if course:
            department = conn.execute('SELECT department_name FROM departments WHERE department_id = ?', (course['department_id'],)).fetchone()
            department_name = department['department_name'] if department else "Unknown Department"
        else:
            abort(404)

        
        return render_template('course_detail.html', course=course, reviews=reviews, department_name=department_name)

@app.route('/course/<course_code>/add_review', methods=('GET', 'POST')) 
def add_review(course_code):
    if request.method == 'POST':
        comments = request.form['comments']
        difficulty_rating = request.form['difficulty_rating']
        professor_rating = request.form['professor_rating']

        conn = get_db_connection()
        conn.execute('INSERT INTO reviews (course_code, student_id, comments, difficulty_rating, professor_rating) VALUES (?, ?, ?, ?, ?)',
                     (course_code, 1, comments, difficulty_rating, professor_rating))
        conn.commit()
        conn.close()
        return redirect(url_for('course_detail', course_code=course_code))

    return render_template('add_review.html')





if __name__ == '__main__':
    app.run(debug=True)
