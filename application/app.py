from flask import Flask, render_template, request, redirect
import boto3
import os

app = Flask(__name__)

# Initialize the S3 client without credentials (will use task role)
s3 = boto3.client('s3')


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"

    # Get the bucket name from environment 
    bucket_name = os.getenv('AWS_BUCKET_NAME')

    if file:
        try:
            s3.upload_fileobj(file, bucket_name, file.filename)
            aws_region = os.getenv('AWS_REGION', 'us-east-1')
            file_URL = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{file.filename}"
            return f"Uploaded Successfully! URL: {file_URL}"
        except Exception as e:
            return f"Error uploading file: {str(e)}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
