# alertmanager.py
import psycopg2
from discord import Webhook, RequestsWebhookAdapter
from alert import Alert  # Import the Alert class

class AlertManager:
    def __init__(self, db_conn_str, discord_webhook_url):
        self.db_conn_str = db_conn_str
        self.discord_webhook_url = discord_webhook_url

    def monitor_data_changes(self):
        # Connect to the database
        conn = psycopg2.connect(self.db_conn_str)
        cur = conn.cursor()

        # Query to check for new or updated NEOs
        query = """
        SELECT * FROM neos
        WHERE last_updated >= NOW() - INTERVAL '10 minutes';
        """

        # Execute the query
        cur.execute(query)

        # Fetch all the rows
        rows = cur.fetchall()

        # Close the database connection
        cur.close()
        conn.close()

        # If there are new or updated NEOs, trigger alerts
        if rows:
            self.trigger_alerts_to_users(rows)

    def trigger_alerts_to_users(self, neos):
        # Create a webhook instance
        webhook = Webhook.from_url(self.discord_webhook_url, adapter=RequestsWebhookAdapter())

        # Loop through the NEOs and send an alert for each one
        for neo in neos:
            # Format the message
            message = f"Alert! NEO {neo[1]} has been updated. Impact probability: {neo[3]}"

            # Send the message
            webhook.send(message)

            # Log the alert
            self.log_alert(neo[0], message)

    def log_alert(self, neo_id, message):
        # Connect to the database
        conn = psycopg2.connect(self.db_conn_str)
        cur = conn.cursor()

        # Prepare an SQL INSERT statement to add a new alert record to the `alerts` table
        query = """
        INSERT INTO alerts (subscription_id, message)
        VALUES (%s, %s);
        """

        # Execute the SQL statement with the alert's data
        cur.execute(query, (neo_id, message))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()