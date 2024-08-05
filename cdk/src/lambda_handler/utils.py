import pandas as pd
from io import BytesIO
from fastavro import writer, parse_schema


def get_expected_columns(avro_schema):
    return [field['name'] for field in avro_schema['fields']]

def validate_csv(file, avro_schema):
    expected_columns = get_expected_columns(avro_schema)
    try:
        df = pd.read_csv(file)
        if list(df.columns) == expected_columns:
            return True, df
        else:
            return False, None
    except Exception as e:
        return False, None

def upload_to_s3(bucket_name, object_name, avro_buffer):

    s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=avro_buffer.getvalue())

    

def generate_avro_buffer(schema, file) -> BytesIO:

    try:
        df = pd.read_csv(file)

        records = df.to_dict(orient='records')

        # Parse the Avro schema
        parsed_schema = parse_schema(schema)
        
        # Create a BytesIO buffer to hold the Avro data
        avro_buffer = BytesIO()
        
        # Write the records to the Avro buffer
        writer(avro_buffer, parsed_schema, records)
        
        # Reset the buffer position to the beginning
        avro_buffer.seek(0)
        
        return avro_buffer
    except Exception as e:
        logging.error(f"Error generating Avro buffer: {e}")
        raise ValueError(f"Error generating Avro buffer: {e}")

