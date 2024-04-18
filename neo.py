# neo.py
import psycopg2
from psycopg2 import sql

class NEO:
    def __init__(self, id, name, estimated_diameter, impact_probability, potential_impact_date, sentry_object, last_updated):
        self.id = id
        self.name = name
        self.estimated_diameter = estimated_diameter
        self.impact_probability = impact_probability
        self.potential_impact_date = potential_impact_date
        self.sentry_object = sentry_object
        self.last_updated = last_updated

    def save(self):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(database="your_database", user="your_username", password="your_password", host="localhost", port="5432")
        cur = conn.cursor()

        # Insert a new NEO into the database
        cur.execute(sql.SQL("INSERT INTO neos (id, name, estimated_diameter, impact_probability, potential_impact_date, sentry_object, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s);"), (self.id, self.name, self.estimated_diameter, self.impact_probability, self.potential_impact_date, self.sentry_object, self.last_updated))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

    def update(self):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(database="your_database", user="your_username", password="your_password", host="localhost", port="5432")
        cur = conn.cursor()

        # Update an existing NEO in the database
        cur.execute(sql.SQL("UPDATE neos SET name = %s, estimated_diameter = %s, impact_probability = %s, potential_impact_date = %s, sentry_object = %s, last_updated = %s WHERE id = %s;"), (self.name, self.estimated_diameter, self.impact_probability, self.potential_impact_date, self.sentry_object, self.last_updated, self.id))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()