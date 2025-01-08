from flask import Flask, render_template, request, redirect
import boto3
import os

app = Flask (__name__)

#Read .env file
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

#initialize the S3 client


s3 = boto3.client('s3',
                AWS_ACCESS_KEY_ID,
                AWS_SECRET_ACCESS_KEY,
                AWS_REGION,
                BUCKET_NAME)

@app.route('/')

def index ():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "" :
        return "No selected file"
    if file:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        file_URL= f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
        return f"Uploaded Successfully! URL: {file_URL}"
if __name__ == "__main__":
    app.run(debug=True)