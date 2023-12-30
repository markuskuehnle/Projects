import sqlite3
import logging

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file. """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    """ Create the table if it doesn't exist. """
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS listings (
            data_id text PRIMARY KEY,
            title text,
            address text,
            kaltmiete real,
            living_space real,
            rooms real,
            secondary_criteria text,
            date text
        );
        """
        cur = conn.cursor()
        cur.execute(sql_create_table)
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")

def check_listing_exists(conn, data_id, extraction_date):
    """ Check if a listing with the same ID and date already exists. """
    try:
        cur = conn.cursor()
        cur.execute("SELECT data_id FROM listings WHERE data_id = ? AND date = ?", (data_id, extraction_date))
        return cur.fetchone() is not None
    except sqlite3.Error as e:
        logging.error(f"Error checking listing existence: {e}")
        return False

def insert_listing(conn, listing):
    """ Insert a new listing into the listings table. """
    try:
        query = ''' 
        INSERT OR IGNORE INTO listings(data_id, title, address, kaltmiete, living_space, rooms, secondary_criteria, date)
        VALUES(?,?,?,?,?,?,?,?) 
        '''
        cur = conn.cursor()
        cur.execute(query, listing)
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error inserting listing: {e}")