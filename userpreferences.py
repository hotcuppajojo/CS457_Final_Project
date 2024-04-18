# userpreferences.py
import psycopg2
from psycopg2 import sql

class UserPreferences:
    def __init__(self, id, user_id, alert_threshold, receive_email_alerts, db_host, db_port, db_name, db_user, db_password):
        self.id = id
        self.user_id = user_id
        self.alert_threshold = alert_threshold
        self.receive_email_alerts = receive_email_alerts
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def save(self):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        cur = conn.cursor()

        # Insert a new user preference into the database
        cur.execute(sql.SQL("INSERT INTO user_preferences (id, user_id, alert_threshold, receive_email_alerts) VALUES (%s, %s, %s, %s);"), (self.id, self.user_id, self.alert_threshold, self.receive_email_alerts))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

    def update(self):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        cur = conn.cursor()

        # Update an existing user preference in the database
        cur.execute(sql.SQL("UPDATE user_preferences SET user_id = %s, alert_threshold = %s, receive_email_alerts = %s WHERE id = %s;"), (self.user_id, self.alert_threshold, self.receive_email_alerts, self.id))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

    @classmethod
    def fetch(cls, id, db_host, db_port, db_name, db_user, db_password):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cur = conn.cursor()

        # Fetch the user preference from the database
        cur.execute(sql.SQL("SELECT * FROM user_preferences WHERE id = %s;"), (id,))

        # Fetch the result
        result = cur.fetchone()

        # Close the connection
        cur.close()
        conn.close()

        # Return a new UserPreferences object
        return cls(*result, db_host, db_port, db_name, db_user, db_password)

    def delete(self):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        cur = conn.cursor()

        # Delete the user preference from the database
        cur.execute(sql.SQL("DELETE FROM user_preferences WHERE id = %s;"), (self.id,))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()