# eventlog.py
import psycopg2
from psycopg2 import sql

class EventLog:
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def log_event(self, user_id, event_type, event_description):
        # Connect to the database
        conn = self.connect_to_db()
        cur = conn.cursor()

        # Prepare the SQL INSERT statement
        insert_sql = sql.SQL("""
            INSERT INTO event_logs (user_id, event_type, event_description)
            VALUES (%s, %s, %s)
        """)

        # Execute the SQL statement with the provided parameters
        cur.execute(insert_sql, (user_id, event_type, event_description))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()

    def connect_to_db(self):
        conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        return conn