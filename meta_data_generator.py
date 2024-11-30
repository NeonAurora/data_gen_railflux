# MetaDataGenerator.py
import firebase_setup  # Ensure Firebase is properly set up
from firebase_admin import db
import os

class MetaDataGenerator:
    def __init__(self):
        # Firebase reference to the metadata node
        self.metadata_ref = db.reference('/Metadata')

    def fetch_and_write_metadata(self):
        """Fetch metadata from Firebase and write it to metadata.py file."""
        fetched_data = self.metadata_ref.get()
        if not fetched_data:
            print("No metadata found in Firebase.")
            return

        # Generate the Python content that will be written to metadata.py
        content = "# metadata.py\n\n"
        content += "# This file is automatically generated by MetaDataGenerator.py\n\n"
        for key, value in fetched_data.items():
            # Convert dictionary entries into Python variable assignments
            content += f"{key.upper()} = {value}\n"

        # Write the content into metadata.py file
        with open("metadata.py", "w") as file:
            file.write(content)

        print("Metadata has been successfully written to metadata.py.")

if __name__ == "__main__":
    generator = MetaDataGenerator()
    generator.fetch_and_write_metadata()
