import sqlite3
import random

class StudentDatabase:
    def __init__(self, db_name="students_college.db"):
        """Initialize the database connection."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Create the students table with an additional 'Field' column."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            enrollment_number TEXT UNIQUE,
            department TEXT,
            cgpa REAL,
            project_score REAL,
            internships INTEGER,
            research_papers INTEGER,
            extracurricular_score REAL,
            outcome TEXT,  -- Column to store predicted outcome ('Selected', 'Rejected', 'No Offer')
            field TEXT     -- New column for IT or Non-IT categorization
        );
        """)

    def clear_table(self):
        """Clear the students table and reset the ID sequence."""
        self.cursor.execute("DELETE FROM students;")  # Clear table data
        self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='students';")  # Reset AUTOINCREMENT
        self.connection.commit()

    def assign_field(self, department):
        """Assign Field based on department."""
        if department in ["Computer Science", "Electronics"]:
            return "IT"
        else:
            return "Non-IT"

    def assign_outcome(self, cgpa, project_score, internships, extracurricular_score):
        """Probabilistic outcome assignment based on weighted score."""
        # Weights for each factor
        cgpa_weight = 0.4
        project_weight = 0.3
        internship_weight = 0.2
        extracurricular_weight = 0.1

        # Calculate weighted score
        weighted_score = (cgpa * cgpa_weight) + (project_score * project_weight) + \
                         (internships * internship_weight * 10) + (extracurricular_score * extracurricular_weight)
        
        
        if weighted_score > 70:
            # Very high chance of "Selected"
            return random.choices(['Selected', 'No Offer', 'Rejected'], weights=[85, 10, 5])[0]
        elif weighted_score < 40:
            # Moderate chance of "Rejected" but still favoring "Selected"
            return random.choices(['Rejected', 'Selected', 'No Offer'], weights=[50, 40, 10])[0]
        else:
            # More balanced but still favoring "Selected"
            return random.choices(['Selected', 'No Offer', 'Rejected'], weights=[60, 30, 10])[0]

    def generate_students(self, names):
        """Generate and insert student data into the database."""
        departments = ["Computer Science", "Mechanical", "Electrical", "Civil", "Electronics"]

        for i, name in enumerate(names):
            enrollment_number = f"EN{1000+i}"  # Unique enrollment number
            department = random.choice(departments)
            cgpa = round(random.uniform(6.0, 10.0), 2)
            project_score = round(random.uniform(50, 100), 1)
            internships = random.randint(0, 3)
            research_papers = random.randint(0, 2)
            extracurricular_score = round(random.uniform(50, 100), 1)

            # Determine the outcome using the probabilistic assignment function
            outcome = self.assign_outcome(cgpa, project_score, internships, extracurricular_score)

            # Assign field based on department
            field = self.assign_field(department)

            self.cursor.execute("""
            INSERT INTO students (name, enrollment_number, department, cgpa, project_score, internships, research_papers, extracurricular_score, outcome, field)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (name, enrollment_number, department, cgpa, project_score, internships, research_papers, extracurricular_score, outcome, field))

        self.connection.commit()

    def display_students(self):
        """Fetch and display all student records."""
        self.cursor.execute("SELECT * FROM students;")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Enrollment No: {row[2]}, Department: {row[3]}, "
                  f"CGPA: {row[4]}, Project Score: {row[5]}, Internships: {row[6]}, "
                  f"Research Papers: {row[7]}, Extracurricular Score: {row[8]}, Outcome: {row[9]}, Field: {row[10]}")
            
    def count_outcomes(self):
        """Count the occurrences of each outcome ('Selected', 'Rejected', 'No Offer')."""
        self.cursor.execute("""
        SELECT outcome, COUNT(*) FROM students GROUP BY outcome;
        """)
        outcome_counts = self.cursor.fetchall()
        outcome_dict = {outcome: count for outcome, count in outcome_counts}
        
        # Ensure all outcomes are accounted for, even if they don't exist
        for outcome in ['Selected', 'Rejected', 'No Offer']:
            outcome_dict.setdefault(outcome, 0)
        
        return outcome_dict

    def close_connection(self):
        """Close the database connection."""
        self.connection.close()


# Usage
if __name__ == "__main__":
    names = [
    "Aayush pandey", "ABhijith", "Abhilash B U", "Achut Anegundi", "Achutha",
    "Adithya T", "Aditya kumar", "Aditya Raj Singh", "Adithya Sharma",
    "Akash Kumar", "Akhil Tendulkar", "Aman Shukla", "Amruthavarshini M",
    "Anand", "Ananya BL", "Anjuru Harshavardhan", "Anshika chaurasia",
    "Archana R", "Aryan Arora", "Ashish Kumar", "Ashok G R",
    "Ashwini Priya K", "Athmika NR", "Athreya Hebbar P", "Avinash Kumar",
    "Ballani Bhavya", "Suhas", "BESTHARAPALLI THUPAKULA INDRASENA",
    "Bhargav V R", "Bhargava P", "Bhavana SR", "Boddu Saieesh",
    "C DEEPAK", "C N NAGABUSHAN", "Chaithra G Bhat", "Charana P L",
    "chetan M Halageri", "Chidananda", "praneeth.D", "Deekshith", "Dhanush",
    "Dhanush C O", "Eashan patil", "Ganesh", "G Raghu", "GORTHI HARSHA VARDHAN",
    "Goutham M", "G V Jayasree Keerthana", "Saiteja", "Gurudeep G H",
    "Harsha", "HARSH RAJ", "Harshith C Gowda", "Harshitha S K",
    "Jagadheeswaran", "Kadambari K", "Kannali pc eswar", "Kariyappa",
    "Karthik C S", "Karthik Murthy S", "kartik pagad", "Kavya", "Kavya k g",
    "Keerti Machali", "Kriti Gupta", "Kruthik s Reddy", "Lakshmishree V S",
    "Likhith M Y", "Luqmaan Mujahid Mohamed", "Madhu shree M", "Madhush M",
    "Hareeswar Reddy", "Manoj Hegde", "Abhiram", "Minni kumari", "Moksha P",
    "Monica", "Monisha B", "Nadiminti Rakesh Rohan", "Nandan N",
    "Nanshi Kumari", "Neha Annie S", "Nishant Anand", "Nishanth Kotiyan",
    "Nishchith M Krishna", "Nitin sreepad kolekar", "Nitin Singh",
    "Nivedita Bhat", "Pallavi V N", "Pamujula Dhurjata", "Parth Kumthekar",
    "Paul Abhishek B", "Pavan naik", "Pooja Kadri", "Poorvika Muralapur",
    "PRADEEP S L", "Prajwal G", "Pratham Bhat", "Priyabrata Pramanick",
    "Rahul", "Raj Srivastava", "Raja Raman", "Rakshith K R", "Raktim Banerjee",
    "Ramanuja", "Ranyil John", "Rayyan Ahmed Sharief", "Rayyan Mohammed",
    "REENAL SONY PINTO", "Rekha sree.T", "Revanth O G", "Reynold John JS",
    "Risha Tomer", "Rithwik", "Rohan K", "Rohit", "S Goutham", "Kritika",
    "S R Shreya", "S Rahul", "S Vrajesh", "Sai Achuth", "Sai Kiran V",
    "Sai Likith P", "Sakshi priya", "Sakshi Singh", "Samyuktha Premkumar",
    "sangamesh", "SANJANA", "Sankara Balaji", "Santhosh P", "Satya Dev",
    "Shaikh Mohammad javeed akhtar", "Zubair", "Shantanu Kudva", "Shashank B C",
    "Shivam Kashinath Shalake", "SHRAVANKUMAR BABU MALAKAGOND", "Shreeya B Naik",
    "SHREYAS M S", "Shubha K", "Siddarth M Kerudi", "Siddharth P Scindya",
    "Shiva", "Somesh S Golabhanvi", "Spoorthi Anjaneya", "Shrujan Kumar",
    "Srusti S K", "Sudeeksha K", "SUDHARSHAN K", "Sufiyan Ahmed Khan",
    "Sughosh V", "Sumanth Reddy M", "Sumeet Pujeri", "Supriya ray",
    "Swati Pujari", "Syed Arfaan", "Tapan G Hegde", "Aishwarya Thota",
    "Sai Manoj thota", "Toushifraza Darur", "Vanshika Gaba", "VARSHA P",
    "Vasupraneetha H", "Veekshitha", "Velidandla Chathurima", "Bindumati",
    "Vinith U", "VISHAL RATHOD", "Vishwa", "Vivek", "Y.Sri Vamsi Bhargav",
    "Yash Mathur", "Anusha G K", "Dhaatri Prasanna", "Shubham", "Arya S G",
    "Lavanya K", "Arpith", "Priyanka", "Vaibhav", "Swathi Y.V", "ANJANEYYA",
    "DEEKSHITH BH", "Dhanush kumar M K", "Dileep kumar S", "GIRISH N",
    "HANUMANAIK L", "Kavita T K", "NAVEEN S", "PRASHANTHA B", "Rajesh k",
    "Sanjay J C", "SHASHANKA L R", "Shreyas Nayak", "Siddesh h k", "Tarun V",
    "VENKATESH S S", "Vinay DH"
]

    # Extend the names to generate at least 600 records
    extended_names = names * (600 // len(names) + 1)
    final_names = extended_names[:600]

    # Initialize database
    db = StudentDatabase()

    # Clear existing data to avoid duplicates
    db.clear_table()

    # Generate new student records
    db.generate_students(final_names)

    print("Student data generated and stored successfully!\n")
    print("Displaying all students:\n")

    # Display the latest data
    db.display_students()
    
    outcome_counts = db.count_outcomes()
    print("\nOutcome counts:")
    for outcome, count in outcome_counts.items():
        print(f"{outcome}: {count}")

    # Close the database connection
    db.close_connection()
