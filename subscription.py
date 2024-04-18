# subscription.py
import psycopg2
from psycopg2 import sql

class Subscription:
    def __init__(self, id, user_id, neo_id, active, db_host, db_port, db_name, db_user, db_password):
        self.id = id
        self.user_id = user_id
        self.neo_id = neo_id
        self.active = active
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

        # Insert a new subscription into the database
        cur.execute(sql.SQL("INSERT INTO subscriptions (id, user_id, neo_id, active) VALUES (%s, %s, %s, %s);"), (self.id, self.user_id, self.neo_id, self.active))

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

        # Update an existing subscription in the database
        cur.execute(sql.SQL("UPDATE subscriptions SET user_id = %s, neo_id = %s, active = %s WHERE id = %s;"), (self.user_id, self.neo_id, self.active, self.id))

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

        # Fetch the subscription from the database
        cur.execute(sql.SQL("SELECT * FROM subscriptions WHERE id = %s;"), (id,))

        # Fetch the result
        result = cur.fetchone()

        # Close the connection
        cur.close()
        conn.close()

        # Return a new Subscription object
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

        # Delete the subscription from the database
        cur.execute(sql.SQL("DELETE FROM subscriptions WHERE id = %s;"), (self.id,))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()