# datamanager.py
import requests
from psycopg2 import sql
from neo import NEO  # Import the NEO class

class DataManager:
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.sentry_api_url = "https://ssd-api.jpl.nasa.gov/sentry.api"

    def fetch_NEO_data(self, mode, **kwargs):
        params = {"mode": mode}
        params.update(kwargs)
        response = requests.get(self.sentry_api_url, params=params)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        return response.json()

    def update_NEO_data_in_db(self, data):
        # Update the NEO data in the database
        for neo_data in data:
            neo = NEO.from_dict(neo_data)
            neo.db_host = self.db_host
            neo.db_port = self.db_port
            neo.db_name = self.db_name
            neo.db_user = self.db_user
            neo.db_password = self.db_password
            neo.save()

    def check_data_updates(self):
        # Fetch the latest data from the Sentry API
        latest_data = self.fetch_NEO_data("projected")

        # Update the NEO data in the database
        self.update_NEO_data_in_db(latest_data)

    def fetch_NEO_from_db(self, id):
        # Fetch the NEO from the database
        neo = NEO.fetch(id, self.db_host, self.db_port, self.db_name, self.db_user, self.db_password)
        return neo