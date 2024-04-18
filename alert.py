# alert.py
import psycopg2
from psycopg2 import sql

class AlertManager:
    def __init__(self, data_manager, bot_manager):
        self.data_manager = data_manager
        self.bot_manager = bot_manager

    def monitor_data_changes(self):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(database="your_database", user="your_username", password="your_password", host="localhost", port="5432")
        cur = conn.cursor()

        # Fetch the latest NEO data
        cur.execute("SELECT * FROM neos ORDER BY last_updated DESC LIMIT 1;")
        latest_neo = cur.fetchone()

        # Check if the latest NEO data has changed
        if latest_neo != self.data_manager.fetch_neo_data():
            self.trigger_alerts_to_users()

        # Close the database connection
        cur.close()
        conn.close()

    def trigger_alerts_to_users(self):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(database="your_database", user="your_username", password="your_password", host="localhost", port="5432")
        cur = conn.cursor()

        # Fetch all active subscriptions
        cur.execute("SELECT * FROM subscriptions WHERE active = TRUE;")
        active_subscriptions = cur.fetchall()

        # For each active subscription, send an alert to the user
        for subscription in active_subscriptions:
            user_id = subscription[1]
            neo_id = subscription[2]

            # Fetch the user's preferences
            cur.execute(sql.SQL("SELECT * FROM user_preferences WHERE user_id = %s;"), (user_id,))
            user_preferences = cur.fetchone()

            # Fetch the NEO data
            cur.execute(sql.SQL("SELECT * FROM neos WHERE id = %s;"), (neo_id,))
            neo_data = cur.fetchone()

            # Check if the NEO's impact probability exceeds the user's alert threshold
            if neo_data[3] > user_preferences[2]:
                # Send an alert to the user
                message = f"NEO {neo_data[1]} has an impact probability of {neo_data[3]}, which exceeds your alert threshold of {user_preferences[2]}."
                self.bot_manager.send_alerts(message)

        # Close the database connection
        cur.close()
        conn.close()