-- Drop tables if they exist
DROP TABLE IF EXISTS review_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS course_professors;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS performance;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS departments;

-- Table: students

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    academic_details TEXT
);

-- Table: courses

CREATE TABLE courses (
    course_code TEXT PRIMARY KEY,
    course_name TEXT NOT NULL, 
    department_id TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
   
);


-- Table: reviews
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_code TEXT NOT NULL,
    difficulty_rating REAL CHECK (difficulty_rating BETWEEN 0 AND 10),    
    professor_rating INTEGER,
    comments TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
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

-- Table: professors

CREATE TABLE professors (
    professor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Table: course_professors
CREATE TABLE course_professors (
    course_code TEXT NOT NULL,
    professor_id INTEGER NOT NULL,
    PRIMARY KEY (course_code, professor_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code),
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
);

-- Table: departments

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT UNIQUE
);

-- Table: tags
CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT UNIQUE
);


-- Table: review_tags
CREATE TABLE review_tags (
    review_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (review_id, tag_id),
    FOREIGN KEY (review_id) REFERENCES reviews(review_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- Table: posts

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);