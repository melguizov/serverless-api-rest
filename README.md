# Flask CSV Upload API

This is a RESTful API built with Flask that allows uploading CSV files, validates their structure, and stores them in an Amazon S3 bucket. The API accepts the following CSV files:

- `hired_employees.csv` with the following structure:
  - `id` (INTEGER)
  - `name` (STRING)
  - `datetime` (STRING)
  - `department_id` (INTEGER)
  - `job_id` (INTEGER)

- `departments.csv` with the following structure:
  - `id` (INTEGER)
  - `department` (STRING)

- `jobs.csv` with the following structure:
  - `job` (STRING)

## Requirements

- Python 3.6+
- Flask
- Boto3
- Pandas

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/melguizov/serverless-api-rest.git
    cd serverless-api-rest.git
    ```

2. Create a virtual environment and install the dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Configure your AWS credentials in your environment. You can do this by exporting the environment variables:
    ```bash
    export AWS_ACCESS_KEY_ID='<AWS_ACCESS_KEY_ID>'
    export AWS_SECRET_ACCESS_KEY='<AWS_SECRET_ACCESS_KEY>'

    ```

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. In your local machine the API will be available at `http://127.0.0.1:5000`.

3. To upload a CSV file, make a `POST` request to `/upload` with the file attached. Here is an example using `curl`:
    ```bash
    curl -X POST -F 'file=@path/to/your/hired_employees.csv' http://127.0.0.1:5000/upload
    ```

## Project Structure

- `app.py`: Main Flask application file.
- `requirements.txt`: Dependencies file.
- `utils.py`: Utility functions for validating and uploading CSV files to S3.

## File Validation

The API validates that the CSV files have the correct structure according to the expected format. If the structure is incorrect, the API will return an error.

## Upload to S3

If the CSV file is valid, it will be uploaded to the S3 bucket configured in the environment variables.

## Contributing

Contributions are welcome. Please open an issue or pull request to discuss any changes you would like to make.

## License

This project is licensed under the MIT License.
