# user.py
import psycopg2
from psycopg2 import sql
from userpreferences import UserPreferences  # Import the UserPreferences class

class User:
    def __init__(self, id, username, email, created_at, preferences, db_host, db_port, db_name, db_user, db_password):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at
        self.preferences = preferences  # This is a UserPreferences object
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

        # Insert a new user into the database
        cur.execute(sql.SQL("INSERT INTO users (id, username, email, created_at) VALUES (%s, %s, %s, %s);"), (self.id, self.username, self.email, self.created_at))

        # Save the user's preferences
        self.preferences.save()

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

        # Update an existing user in the database
        cur.execute(sql.SQL("UPDATE users SET username = %s, email = %s, created_at = %s WHERE id = %s;"), (self.username, self.email, self.created_at, self.id))

        # Update the user's preferences
        self.preferences.update()

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

        # Fetch the user from the database
        cur.execute(sql.SQL("SELECT * FROM users WHERE id = %s;"), (id,))

        # Fetch the result
        result = cur.fetchone()

        # Fetch the user's preferences
        preferences = UserPreferences.fetch(id, db_host, db_port, db_name, db_user, db_password)

        # Close the connection
        cur.close()
        conn.close()

        # Return a new User object
        return cls(*result, preferences, db_host, db_port, db_name, db_user, db_password)

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

        # Delete the user from the database
        cur.execute(sql.SQL("DELETE FROM users WHERE id = %s;"), (self.id,))

        # Delete the user's preferences
        self.preferences.delete()

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()