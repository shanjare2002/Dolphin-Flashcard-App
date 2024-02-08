""" Provides a class to interact with the database """
import json
#from backend.database.database_abstract import DatabaseAbstract
from database_abstract import DatabaseAbstract

class LocalDatabase(DatabaseAbstract):
    """ Write to local files for development """
    def __init__(self, filename="data.json"):
        self.filename = filename
        try:
            # Load existing JSON data
            with open(filename, "r") as file:
                self.json_data = json.load(file)
        except FileNotFoundError:
            # If file doesn't exist, create an empty dictionary
            self.json_data = {}

    def _load_from_file(self):
        """Load JSON data from the file specified by self.filename"""
        try:
            with open(self.filename, 'r') as file:
                self.json_data = json.load(file)
        except FileNotFoundError:
            print(f"File '{self.filename}' not found. Initializing with an empty dictionary.")

    def _traverse_path(self, path):
        """Traverse the JSON structure according to the given path

        Args:
            path (str): The path to traverse

        Returns:
            dict: The dictionary corresponding to the path
        """
        keys = path.split("/")
        current = self.json_data

        # Traverse the JSON structure according to the given path
        for key in keys:
            current = current[key]

        return current

    def _remove_trailing_slash(self, string: str):
        """Remove the trailing slash from a string

        Args:
            string (str): The string to remove the trailing slash from
        """
        if string[-1] == "/":
            return string[:-1]
        return string

    def write(self):
        """Save self.json_data to a file in JSON format"""
        with open(self.filename, 'w') as file:
            json.dump(self.json_data, file, indent=4)

    def get(self, path):
        """Get data from self.json_data based on the path

        Args:
            path (str): The path to retrieve data from

        Returns:
            Any: The data at the specified path
        """
        self._load_from_file()
        path = self._remove_trailing_slash(path)
        return self._traverse_path(path)

    def save(self, path, data):
        """ Update data in self.json_data based on the path """
        self._load_from_file()
        path = self._remove_trailing_slash(path)
        keys = path.split("/")
        current = self.json_data

        # Traverse the JSON structure according to the given path
        for key in keys[:-1]:
            current = current.setdefault(key, {})

        # Update the data at the final key in the path
        current[keys[-1]] = data
        self.write()

    def increment(self, path, increment_amount) :
        """ Increment a number stored as a string from a path in the database """
        print ("Incrementing " + path + " by " + str(increment_amount))

db = LocalDatabase()

db.save("user/userID/Va1l/e1", {'name': 'John'})
print (db.get("user/userID/Val/"))
