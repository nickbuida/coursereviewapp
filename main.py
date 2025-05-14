from flask import session,Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3
import hashlib
from functools import wraps

app = Flask(__name__, template_folder='src/templates')
app.config['SECRET_KEY'] = 'your secret key'

# Add this near your other app configuration
app.config['SECRET_KEY'] = 'thesecretkeyjbnsdjifsdhbfhiasdbf'

# User authentication function
def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# Login route
@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', 
                          (username,)).fetchone()
        conn.close()
        
        if user is None:
            error = 'Invalid username.'
        elif user['password'] != hash_password(password):
            error = 'Invalid password.'
        else:
            session.clear()
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect(url_for('index'))
            
    return render_template('login.html', error=error)

# Register route
@app.route('/register', methods=('GET', 'POST'))
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        conn = get_db_connection()
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif conn.execute('SELECT user_id FROM users WHERE username = ?', 
                        (username,)).fetchone() is not None:
            error = f"User {username} is already registered."
        
        if error is None:
            conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                      (username, hash_password(password), email))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        
        conn.close()
        
    return render_template('register.html', error=error)

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/courses')
@login_required
def courses():
    conn = get_db_connection()

    # Fetch all courses without avg_difficulty
    courses = conn.execute('''
        SELECT c.course_code, c.course_name, c.department_id, d.department_name, 
               cp.professor_id, p.name as professor_name
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.department_id
        LEFT JOIN course_professors cp ON c.course_code = cp.course_code
        LEFT JOIN professors p ON cp.professor_id = p.professor_id
    ''').fetchall()

    # Fetch unique departments
    departments = conn.execute('SELECT department_id, department_name FROM departments').fetchall()

    # Fetch unique professors
    professors = conn.execute('SELECT professor_id, name FROM professors').fetchall()

    conn.close()

    return render_template('courses.html', courses=courses, departments=departments, professors=professors)


@app.route('/course/<course_code>')
@login_required
def course_detail(course_code):
    with get_db_connection() as conn:
        course = conn.execute('SELECT * FROM courses WHERE course_code = ?', (course_code,)).fetchone()
        
        if not course:
            abort(404)
            
        # Get department name
        department = conn.execute('SELECT department_name FROM departments WHERE department_id = ?', 
                                 (course['department_id'],)).fetchone()
        department_name = department['department_name'] if department else "Unknown Department"
        
        # Get reviews with professor names, student info, and course rating
        reviews = conn.execute('''
            SELECT r.*, p.name as professor_name, s.name as student_name, 
                  (r.student_id = ?) as is_own_review, r.course_rating
            FROM reviews r
            LEFT JOIN professors p ON r.professor_id = p.professor_id
            LEFT JOIN students s ON r.student_id = s.student_id
            WHERE r.course_code = ?
            ORDER BY is_own_review DESC, r.review_id DESC
        ''', (session['user_id'], course_code)).fetchall()

        # Calculate average difficulty, rating, and grade
        averages = conn.execute('''
            SELECT 
                AVG(difficulty_rating) as avg_difficulty,
                AVG(course_rating) as avg_rating,
                AVG(score) as avg_grade
            FROM reviews
            WHERE course_code = ?
        ''', (course_code,)).fetchone()
        
    return render_template('course_detail.html', 
                          course=course, 
                          reviews=reviews, 
                          department_name=department_name,
                          averages=averages)

@app.route('/course/<course_code>/add_review', methods=('GET', 'POST'))
@login_required
def add_review(course_code):
    # Get current user's student_id
    with get_db_connection() as conn:
        # First, verify the course exists
        course = conn.execute('SELECT * FROM courses WHERE course_code = ?', 
                             (course_code,)).fetchone()
        if not course:
            abort(404)
            
        # Find the student record for the current user
        student = conn.execute('SELECT student_id FROM students WHERE user_id = ?', 
                             (session['user_id'],)).fetchone()
        
        if not student:
            flash('You need a student profile to add reviews.')
            return redirect(url_for('course_detail', course_code=course_code))
            
        # Get the student_id from the query result
        student_id = student['student_id']
        
        # Get professors who teach this course for the dropdown
        professors = conn.execute('''
            SELECT p.professor_id, p.name
            FROM professors p
            JOIN course_professors cp ON p.professor_id = cp.professor_id
            WHERE cp.course_code = ?
        ''', (course_code,)).fetchall()
        
        if request.method == 'POST':
            professor_id = request.form['professor_id']
            difficulty_rating = request.form['difficulty_rating']
            professor_rating = request.form['professor_rating']
            comments = request.form['comments']
            score = request.form['score']
            course_rating = request.form['course_rating']
            
            conn.execute('''
                INSERT INTO reviews (student_id, professor_id, course_code, 
                                    difficulty_rating, professor_rating, comments, score, course_rating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, professor_id, course_code, 
                 difficulty_rating, professor_rating, comments, score, course_rating))
            
            conn.commit()
            flash('Your review was added successfully!')
            
            return redirect(url_for('course_detail', course_code=course_code))
    
    return render_template('add_review.html', course=course, professors=professors)


@app.route('/review/<int:review_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_review(review_id):
    with get_db_connection() as conn:
        # Get the review and check if it belongs to the current user
        review = conn.execute('SELECT * FROM reviews WHERE review_id = ?', (review_id,)).fetchone()
        
        if not review:
            abort(404)
            
        # Security check - only allow editing your own reviews
        if review['student_id'] != session['user_id']:
            flash('You can only edit your own reviews.')
            return redirect(url_for('course_detail', course_code=review['course_code']))
        
        # Get course info
        course = conn.execute('SELECT * FROM courses WHERE course_code = ?', 
                             (review['course_code'],)).fetchone()
        
        # Get professors who teach this course
        professors = conn.execute('''
            SELECT p.professor_id, p.name
            FROM professors p
            JOIN course_professors cp ON p.professor_id = cp.professor_id
            WHERE cp.course_code = ?
        ''', (review['course_code'],)).fetchall()
        
        if request.method == 'POST':
            # Process form submission
            comments = request.form['comments']
            difficulty_rating = request.form['difficulty_rating']
            professor_rating = request.form['professor_rating']
            professor_id = request.form['professor_id']
            course_rating = request.form['course_rating']
            
            conn.execute('''
                UPDATE reviews
                SET comments = ?, difficulty_rating = ?, professor_rating = ?, professor_id = ?, course_rating = ?
                WHERE review_id = ?
            ''', (comments, difficulty_rating, professor_rating, professor_id, course_rating, review_id))
            
            conn.commit()
            
            flash('Your review has been updated successfully!')
            return redirect(url_for('course_detail', course_code=review['course_code']))
        
    return render_template('edit_review.html', review=review, professors=professors, course=course)

@app.route('/review/<int:review_id>/delete', methods=['GET'])
@login_required
def delete_review(review_id):
    with get_db_connection() as conn:
        # Get the review and check if it belongs to the current user
        review = conn.execute('SELECT * FROM reviews WHERE review_id = ?', (review_id,)).fetchone()
        
        if not review:
            abort(404)
        
        # Get the current user's student_id
        student = conn.execute('SELECT student_id FROM students WHERE user_id = ?', 
                              (session['user_id'],)).fetchone()
        
        if not student or review['student_id'] != student['student_id']:
            flash('You can only delete your own reviews.')
            return redirect(url_for('course_detail', course_code=review['course_code']))
        
        # Delete associated tags first (to maintain referential integrity)
        conn.execute('DELETE FROM review_tags WHERE review_id = ?', (review_id,))
        
        # Then delete the review
        conn.execute('DELETE FROM reviews WHERE review_id = ?', (review_id,))
        conn.commit()
        
        flash('Your review has been deleted.')
        return redirect(url_for('course_detail', course_code=review['course_code']))


@app.route('/professor/<int:professor_id>')
@login_required
def professor_detail(professor_id):
    with get_db_connection() as conn:
        # Get professor details along with department information
        professor = conn.execute('''
            SELECT p.*, d.department_id, d.department_name
            FROM professors p
            LEFT JOIN course_professors cp ON p.professor_id = cp.professor_id
            LEFT JOIN courses c ON cp.course_code = c.course_code
            LEFT JOIN departments d ON c.department_id = d.department_id
            WHERE p.professor_id = ?
        ''', (professor_id,)).fetchone()

        if not professor:
            abort(404)

        # Calculate average and median ratings for the professor across all courses
        ratings = conn.execute('''
            SELECT AVG(professor_rating) as avg_rating, 
                   (SELECT professor_rating FROM reviews WHERE professor_id = ? ORDER BY professor_rating LIMIT 1 OFFSET (SELECT COUNT(*) FROM reviews WHERE professor_id = ?) / 2) as median_rating
            FROM reviews WHERE professor_id = ?
        ''', (professor_id, professor_id, professor_id)).fetchone()

        # Get the list of courses the professor teaches with their average ratings
        courses = conn.execute('''
            SELECT c.course_code, c.course_name, AVG(r.professor_rating) as avg_course_rating
            FROM courses c
            JOIN course_professors cp ON c.course_code = cp.course_code
            LEFT JOIN reviews r ON c.course_code = r.course_code AND r.professor_id = ?
            WHERE cp.professor_id = ?
            GROUP BY c.course_code, c.course_name
        ''', (professor_id, professor_id)).fetchall()

    return render_template('professor_detail.html', professor=professor, ratings=ratings, courses=courses)

@app.route('/department/<int:department_id>')
@login_required
def department_detail(department_id):
    with get_db_connection() as conn:
        # Get department details
        department = conn.execute('SELECT * FROM departments WHERE department_id = ?', (department_id,)).fetchone()
        if not department:
            abort(404)

        # Access department_id using dictionary-style access
        department_id = department['department_id']

        # Get professors in the department with their average ratings
        professors = conn.execute('''
            SELECT p.professor_id, p.name, AVG(r.professor_rating) as avg_rating
            FROM professors p
            JOIN courses c ON c.department_id = ?
            JOIN course_professors cp ON cp.professor_id = p.professor_id AND cp.course_code = c.course_code
            LEFT JOIN reviews r ON r.professor_id = p.professor_id
            GROUP BY p.professor_id, p.name
        ''', (department_id,)).fetchall()

        # Get courses taught by professors in the department
        courses = conn.execute('''
            SELECT c.course_code, c.course_name, p.name as professor_name, p.professor_id
            FROM courses c
            JOIN course_professors cp ON c.course_code = cp.course_code
            JOIN professors p ON cp.professor_id = p.professor_id
            WHERE c.department_id = ?
        ''', (department_id,)).fetchall()

    return render_template('department_detail.html', department=department, professors=professors, courses=courses)

if __name__ == '__main__':
    app.run(debug=True)
