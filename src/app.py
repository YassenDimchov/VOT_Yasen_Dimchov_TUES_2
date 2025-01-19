from flask import Flask, request, jsonify, send_file
import boto3
from keycloak import KeycloakOpenID
from io import BytesIO
import botocore.exceptions

app = Flask(__name__)

minio_client = boto3.client(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)


bucket_name = 'my-bucket'

def create_bucket_if_not_exists(bucket_name):
    try:
        response = minio_client.list_buckets()
        existing_buckets = [bucket['Name'] for bucket in response['Buckets']]
        
        if bucket_name not in existing_buckets:
            minio_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} created.")
        else:
            print(f"Bucket {bucket_name} already exists.")
    except botocore.exceptions.EndpointConnectionError as e:
        print(f"Error connecting to MinIO: {e}")

create_bucket_if_not_exists(bucket_name)

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/auth/",
    client_id="my-client",
    realm_name="my-realm",
    client_secret_key="my-client-secret"
)

def verify_token(token):
    try:
        print(f"Verifying token: {token}")
        keycloak_openid.userinfo(token)
        return True
    except Exception as e:
        print(f"Error verifying token: {e}")
        return False


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask app!"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    token = request.headers.get('Authorization')
    if not token or 'Bearer ' not in token:
        return jsonify({"error": "Token missing or invalid"}), 400
    token = token.split(' ')[-1]
    if not verify_token(token):
        return jsonify({"error": "Unauthorized"}), 401

    file = request.files['file']
    minio_client.put_object(
        Bucket=bucket_name,
        Key=file.filename,
        Body=file,
        ContentType=file.content_type
    )
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    token = request.headers.get('Authorization')
    if not token or 'Bearer ' not in token:
        return jsonify({"error": "Token missing or invalid"}), 400
    token = token.split(' ')[-1]
    if not verify_token(token):
        return jsonify({"error": "Unauthorized"}), 401

    response = minio_client.get_object(Bucket=bucket_name, Key=file_id)
    file_stream = BytesIO(response['Body'].read())
    return send_file(file_stream, attachment_filename=file_id)

@app.route('/update/<file_id>', methods=['PUT'])
def update_file(file_id):
    token = request.headers.get('Authorization')
    if not token or 'Bearer ' not in token:
        return jsonify({"error": "Token missing or invalid"}), 400
    token = token.split(' ')[-1]
    if not verify_token(token):
        return jsonify({"error": "Unauthorized"}), 401

    file = request.files['file']
    minio_client.put_object(
        Bucket=bucket_name,
        Key=file_id,
        Body=file,
        ContentType=file.content_type
    )
    return jsonify({"message": "File updated successfully"}), 200

@app.route('/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    token = request.headers.get('Authorization')
    if not token or 'Bearer ' not in token:
        return jsonify({"error": "Token missing or invalid"}), 400
    token = token.split(' ')[-1]
    if not verify_token(token):
        return jsonify({"error": "Unauthorized"}), 401

    minio_client.delete_object(Bucket=bucket_name, Key=file_id)
    return jsonify({"message": "File deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
