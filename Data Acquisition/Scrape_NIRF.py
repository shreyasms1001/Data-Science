import requests
from bs4 import BeautifulSoup
import sqlite3

def create_db():
    """Create a SQLite database and table if it doesn't exist"""
    conn = sqlite3.connect('nirf_rankings.db')
    cursor = conn.cursor()

    # Create table to store scraped data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS institutions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rank TEXT,
        institution_name TEXT,
        city TEXT,
        state TEXT,
        score TEXT
    )
    ''')

    conn.commit()
    return conn, cursor

def clear_table(cursor):
    """Clear existing data in the institutions table"""
    cursor.execute('DELETE FROM institutions')

def insert_data(cursor, rank, name, city, state, score):
    """Insert scraped data into the database"""
    cursor.execute('''
    INSERT INTO institutions (rank, institution_name, city, state, score)
    VALUES (?, ?, ?, ?, ?)
    ''', (rank, name, city, state, score))

def scrape_and_store(url, cursor):
    """Scrape data and store it in the database"""
    # Send request and parse the page content with BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table by class name (or another appropriate attribute)
    table = soup.find('table', {'id': 'tbl_overall'})
    
    # Extract all rows from the table
    rows = table.find_all('tr')[1:]  # Skip the header row
    
    # Iterate through each row and extract the required data
    for row in rows:
        cols = row.find_all('td')
        
        if len(cols) < 10:
            continue
        
        # Extracting the required details
        rank = cols[-1].text.strip()  # Last column is the rank
        name = cols[1].text.strip().split('More')[0].strip()  # Get name before "More"
        percent = cols[9].text.strip()  # Percent is in the 10th column
        city = cols[7].text.strip()  # City
        state = cols[8].text.strip()  # State

        # Insert the data into the database
        insert_data(cursor, rank, name, city, state, percent)

def display_data(cursor):
    """Fetch and display the data from the database"""
    cursor.execute('SELECT * FROM institutions ORDER BY CAST(rank AS INTEGER)')
    rows = cursor.fetchall()

    for row in rows:
        print(f"Rank: {row[1]}, Institution: {row[2]}, City: {row[3]}, State: {row[4]}, Score: {row[5]}")

# Main execution
if __name__ == "__main__":
    nirf_url = "https://www.nirfindia.org/Rankings/2024/EngineeringRanking.html"

    # Create database and table
    conn, cursor = create_db()

    # Clear the existing data in the table
    clear_table(cursor)

    # Scrape and store data
    scrape_and_store(nirf_url, cursor)

    # Display stored data
    display_data(cursor)

    # Commit changes and close the database connection
    conn.commit()
    conn.close()
