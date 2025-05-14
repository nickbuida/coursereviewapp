-- Drop tables if they exist
DROP TABLE IF EXISTS course_professors;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS performance;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS users;

-- Table: users (moved up since students will reference it)
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: students (modified to include user_id)
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table: departments
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT UNIQUE
);

-- Table: courses
CREATE TABLE courses (
    course_code TEXT PRIMARY KEY,
    course_name TEXT NOT NULL, 
    department_id TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Table: professors
CREATE TABLE professors (
    professor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Table: reviews
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    professor_id INTEGER,
    course_code TEXT NOT NULL,
    difficulty_rating REAL CHECK (difficulty_rating BETWEEN 0 AND 10),    
    professor_rating INTEGER,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    score REAL CHECK (score BETWEEN 0 AND 100),
    course_rating REAL CHECK (course_rating BETWEEN 0 AND 5),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code),
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
);

-- Table: performance
CREATE TABLE performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_code TEXT NOT NULL,
    score REAL,
    grade TEXT,
    attendance REAL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
);

-- Table: course_professors
CREATE TABLE course_professors (
    course_code TEXT NOT NULL,
    professor_id INTEGER NOT NULL,
    PRIMARY KEY (course_code, professor_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code),
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
);