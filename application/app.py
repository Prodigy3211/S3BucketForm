from flask import Flask, render_template, request, redirect, url_for, jsonify
import boto3
import os

app = Flask(__name__)

# Initialize the S3 client without credentials (will use task role)
s3 = boto3.client('s3')
adspeedEndpoint = "https://api.adspeed.com/"
ADSPEED_KEY = os.getenv('ADSPEED_KEY')

@app.route('/health')
def health():
    return jsonify({"status": "healthy!!"})


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

    try:
        s3.upload_fileobj(file, bucket_name, file.filename)
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        file_URL = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{file.filename}"
        return f"Uploaded Successfully! URL: {file_URL}"
    except Exception as e:
        return f"Error uploading file: {str(e)}"
            
        form_data = {
            "file_url": file_URL,
            "adspeed_key" : ADSPEED_KEY,
            "other_fields": request.form.get('business','adDescription')
        }
        adspeed_response = send_to_adspeed(form_data)

        if adspeed_response:
            return f"Uploaded Successfully to S3 and adSpeed! Adspeed Response: {adspeed_response}"
        else:
            return f"Uploaded to S3 but Adspeed upload failed."
    except Exception as e:
        return f"Error uploading file: {str(e)}"

def send_to_adspeed(data):

    try: 
        response = requests.post(adspeedEndpoint, json=data, headers = {"Authorization": f"Bearer {ADSPEED_KEY}"})

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Adspeed API Error: {response.status_code}, {response.text}")
        return None
    except requests.RequestException as e:
        print(f"Error communicating with Adspeed: {e}")
    return None


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
