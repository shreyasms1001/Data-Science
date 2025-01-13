import sqlite3

def fetch_students():
    """Fetch students from the database and calculate their total scores."""
    conn = sqlite3.connect("students_college.db")
    cursor = conn.cursor()

    # Fetch required student data including additional columns
    cursor.execute("""
    SELECT id, name, cgpa, project_score, internships, extracurricular_score, department, field, outcome
    FROM students;
    """)
    students = cursor.fetchall()
    conn.close()

    # Calculate total scores
    student_scores = []
    for student in students:
        total_score = (
            student[2] * 4 +        # CGPA weight: 4
            student[3] * 2 +        # Project Score weight: 2
            student[4] * 1.5 +      # Internships weight: 1.5
            student[5] * 1          # Extracurricular Score weight: 1
        )
        student_scores.append((
            student[0],  # ID
            student[1],  # Name
            student[2],  # CGPA
            student[3],  # Project Score
            student[4],  # Internships
            student[5],  # Extracurricular Score
            student[6],  # Department
            student[7],  # Field
            student[8],  # Outcome
            total_score  # Total Score
        ))

    # Sort by total score in descending order
    return sorted(student_scores, key=lambda x: x[9], reverse=True)

def fetch_institutions():
    """Fetch institutions from the database, sorted by rank."""
    conn = sqlite3.connect("nirf_rankings.db")
    cursor = conn.cursor()

    # Fetch institution data
    cursor.execute("SELECT id, institution_name, rank FROM institutions ORDER BY CAST(rank AS INTEGER);")
    institutions = cursor.fetchall()
    conn.close()
    return institutions

def map_students_to_institutions(students, institutions):
    """Map students to institutions based on cutoff scores."""
    mappings = []
    num_institutions = len(institutions)
    students_per_institution = len(students) // num_institutions

    for i, institution in enumerate(institutions):
        start_idx = i * students_per_institution
        end_idx = start_idx + students_per_institution

        # Assign students within the range to the current institution
        for student in students[start_idx:end_idx]:
            mappings.append((
                student[1],  # Student Name
                student[2],  # CGPA
                student[3],  # Project Score
                student[4],  # Internships
                student[5],  # Extracurricular Score
                student[9],  # Total Score
                student[6],  # Department
                student[7],  # Field
                student[8],  # Outcome
                institution[1],  # Institution Name
                institution[2]   # Institution Rank
            ))

    # Handle remaining students if any
    remaining_students = students[num_institutions * students_per_institution:]
    for i, student in enumerate(remaining_students):
        institution = institutions[i % num_institutions]
        mappings.append((
            student[1],  # Student Name
            student[2],  # CGPA
            student[3],  # Project Score
            student[4],  # Internships
            student[5],  # Extracurricular Score
            student[9],  # Total Score
            student[6],  # Department
            student[7],  # Field
            student[8],  # Outcome
            institution[1],  # Institution Name
            institution[2]   # Institution Rank
        ))

    return mappings

def save_mappings_to_db(mappings, db_name="mapped_data.db"):
    """Save the mapped data into a new SQLite database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS student_institution_mappings;")

    # Create the new table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_institution_mappings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        cgpa REAL,
        project_score REAL,
        internships INTEGER,
        extracurricular_score REAL,
        total_score REAL,
        department TEXT,
        field TEXT,
        outcome TEXT,
        institution_name TEXT,
        institution_rank INTEGER
    );
    """)
    



    # Insert data into the table
    cursor.executemany("""
    INSERT INTO student_institution_mappings (
        student_name, cgpa, project_score, internships, extracurricular_score, 
        total_score, department, field, outcome, institution_name, institution_rank
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, mappings)

    # Commit and close the connection
    conn.commit()
    conn.close()

def display_mappings(mappings):
    """Display the student-to-institution mappings."""
    print("\nStudent-to-Institution Mappings:\n")
    for mapping in mappings:
        print(
            f"Student: {mapping[0]}, CGPA: {mapping[1]:.2f}, Project Score: {mapping[2]:.2f}, "
            f"Internships: {mapping[3]}, Extracurricular Score: {mapping[4]:.2f}, "
            f"Total Score: {mapping[5]:.2f}, Department: {mapping[6]}, Field: {mapping[7]}, "
            f"Outcome: {mapping[8]}, Institution: {mapping[9]}, Rank: {mapping[10]}"
        )

# Main Execution
if __name__ == "__main__":
    # Fetch students and institutions
    students = fetch_students()
    institutions = fetch_institutions()

    # Perform mapping
    student_institution_mappings = map_students_to_institutions(students, institutions)

    # Save mappings to a new database
    save_mappings_to_db(student_institution_mappings)

    # Display mappings
    display_mappings(student_institution_mappings)
