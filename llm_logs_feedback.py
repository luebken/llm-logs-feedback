from typing import List, Tuple, Optional
import sqlite3

import click
import llm


DB_PATH = llm.user_dir() / "logs.db"

@llm.hookimpl
def register_commands(cli):
    @cli.command(name="feedback+1")
    @click.argument("comment", required=False, default=None)
    @click.option("prompt_id", "--prompt_id", help="Optional prompt_id for the feedback. Default is the last.", default="None")
    def feedback_positive(comment, prompt_id):
        """
        Provide positive feedback to the last prompt / response. 
        Add an optional comment.
           
        Example usage:
        \b
          llm feedback+1 "nice. worked great during refactoring."
        """
        create_feedback_table()
        insert_feedback("+1", comment, prompt_id)
        print_all_feedback()
    @cli.command(name="feedback-1")
    @click.argument("comment", required=False, default='')
    @click.option("prompt_id", "--prompt_id", help="Optional prompt_id for the feedback. Default is the last.", default="None")
    def feedback_negative(comment, prompt_id):
        """
        Provide negative feedback to the last prompt / response. 
        Add an optional comment.
        
        Example usage:
        \b
          llm feedback-1 "not helpful. too lengthy."
        """
        create_feedback_table()
        insert_feedback("-1", comment, prompt_id)
        print_all_feedback()

# TODO Create a timestamp
def create_feedback_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        response_id TEXT NOT NULL,
        datetime_utc TIMESTAMP DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
        feedback TEXT NOT NULL,
        comment TEXT
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()
    
def insert_feedback(feedback, comment, response_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # Get the latest response ID if not provided
    if response_id == "None":  # Default value from the feedback command
        cursor.execute('SELECT id FROM responses ORDER BY datetime_utc DESC LIMIT 1')
        result = cursor.fetchone()
        if result:
            response_id = result[0]
        else:
            print("No responses found in the database")
            connection.close()
            return
    
    cursor.execute('''
        INSERT INTO feedback (feedback, comment, response_id) VALUES (?, ?, ?)
    ''', (feedback, comment, response_id))
    connection.commit()
    connection.close()
    print("Feedback added successfully.")
    

def print_all_feedback():
    print("Here are the latest feedbacks:\n")

    query = '''
        SELECT f.feedback, f.comment, r.prompt 
        FROM feedback f
        JOIN responses r ON f.response_id = r.id
        ORDER BY f.id DESC
        LIMIT 5;
    '''
    results = fetch_data_from_db(query)
    for row in results:
        feedback, comment, prompt = row
        print(f" Prompt: {prompt}")
        print(f"  Feedback: {feedback}, Comment: {comment}\n")
        
def fetch_data_from_db(query):
    connection = None
    results = []

    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if connection:
            connection.close()

    return results