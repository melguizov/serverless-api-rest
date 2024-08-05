
from flask import Flask, request, jsonify
from utils import validate_csv, upload_to_s3
from Schemas import get_departments_schema, get_hired_employees_schema, get_jobs_schema
from datetime import datetime
import boto3
import awsgi
import os


# Formatear la fecha y hora como una cadena
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

app = Flask(__name__)

# Configurar las credenciales de AWS y el bucket
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = 'Bucket_api_rest_flask'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

AVRO_SCHEMAS = {
    'hired_employees.csv': get_hired_employees_schema,
    'departments.csv': get_departments_schema,
    'jobs.csv': get_jobs_schema
}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file'] 
    
    request_file = file.filename
    file_name, file_extension = os.path.splitext(request_file)

    avro_schema = AVRO_SCHEMAS[request_file]()
    

    if request_file not in AVRO_SCHEMAS:
        return jsonify({'error': 'Unsupported file format'}), 400

    valid, df = validate_csv(file, avro_schema)
    if not valid:
        return jsonify({'error': 'Invalid file structure'}), 400

    # Obtener la fecha y hora actual
    avro_buffer = generate_avro_buffer(avro_schema, records)

    # Obtener la fecha y hora actual
    current_time = datetime.now().strftime("%Y%m%d_%H_%M_%S")

    # Definir el prefijo (nombre del archivo)
    file_name = f"{file_name}/{current_time}.avro"

    try:
        upload_to_s3(S3_BUCKET_NAME, file_name, avro_buffer)
        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def handler(event, context):
    return awsgi.response(app, event, context)

