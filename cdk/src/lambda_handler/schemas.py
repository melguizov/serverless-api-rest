class Schemas:
    @staticmethod
    def get_hired_employees_schema() -> dict:
        """
        Return the schema for hired employees in Avro format.

        Returns:
            dict: The Avro schema for hired employees.
        """
        return {
            "type": "record",
            "name": "CSVRecord",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "name", "type": "string"},
                {"name": "datetime", "type": "string"},
                {"name": "department_id", "type": "int"},
                {"name": "job_id", "type": "int"}
            ]
        }

    @staticmethod
    def get_departments_schema() -> dict:
        """
        Return the schema for departments in Avro format.

        Returns:
            dict: The Avro schema for departments.
        """
        return {
            "type": "record",
            "name": "CSVRecord",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "department", "type": "string"}
            ]
        }

    @staticmethod
    def get_jobs_schema() -> dict:
        """
        Return the schema for jobs in Avro format.

        Returns:
            dict: The Avro schema for jobs.
        """
        return {
            "type": "record",
            "name": "CSVRecord",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "job", "type": "string"}
            ]
        }