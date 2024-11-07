import os
from airflow.sensors.base import BaseSensorOperator

class FileNotEmptySensor(BaseSensorOperator):
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepath = filepath

    def poke(self, context):
        """
        Poke function that checks if the file is non-empty.
        """
        # Check if the file exists
        if not os.path.exists(self.filepath):
            self.log.info(f"File {self.filepath} does not exist yet.")
            return False
        
        # Check if the file is not empty
        if os.path.getsize(self.filepath) > 0:
            self.log.info(f"File {self.filepath} exists and is not empty.")
            return True
        else:
            self.log.info(f"File {self.filepath} is empty.")
            return False
