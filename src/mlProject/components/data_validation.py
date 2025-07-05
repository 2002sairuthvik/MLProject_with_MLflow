import os
import urllib.request as request
import zipfile
from mlProject.logger import logger
from mlProject.entity.config_entity import DataValidationConfig


import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            # Load data and schema
            data = pd.read_csv(self.config.unzip_data_dir)
            data_columns = list(data.columns)
            schema_columns = list(self.config.all_schema.keys())
            schema_dtypes = self.config.all_schema

            validation_status = True
            messages = []

            # 1. Check for missing columns
            missing_cols = [col for col in schema_columns if col not in data_columns]
            if missing_cols:
                validation_status = False
                messages.append(f"Missing columns: {missing_cols}")

            # 2. Check for extra columns
            extra_cols = [col for col in data_columns if col not in schema_columns]
            if extra_cols:
                validation_status = False
                messages.append(f"Extra columns: {extra_cols}")

            # 3. Check column data types
            for col in schema_columns:
                if col in data.columns:
                    actual_dtype = str(data[col].dtype)
                    expected_dtype = schema_dtypes[col]
                    if actual_dtype != expected_dtype:
                        validation_status = False
                        messages.append(f"Column '{col}' has dtype '{actual_dtype}', expected '{expected_dtype}'.")

            # Write status to file
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}\n")
                for msg in messages:
                    f.write(msg + "\n")

            return validation_status

        except Exception as e:
            # Optionally log or write error to status file
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation failed due to error: {str(e)}\n")
            raise
