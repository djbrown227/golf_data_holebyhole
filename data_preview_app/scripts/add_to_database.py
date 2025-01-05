import os
import django

# Set the Django settings module for the current environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_preview_app.settings')

# Setup Django
django.setup()

# Import the model after setting up Django
from data_manager.models import GolfFile

# Function to add a golf file to the database
def add_golf_file(name, file_path):
    # Create a GolfFile instance and save it to the database
    golf_file = GolfFile(name=name, file=file_path)
    golf_file.save()
    print(f"Added {name} to the database.")

# Example usage of the function to add files
if __name__ == "__main__":
    add_golf_file('sample1.csv', '/Users/danielbrown/Desktop/WebApps/data_preview_app/media/golf_files/ZOZO_CHAMPIONSHIP_2024.csv')
