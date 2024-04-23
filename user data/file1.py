from flask import Flask, render_template, request, send_file
import boto3
from botocore.exceptions import NoCredentialsError
import os

app = Flask(__name__)

# AWS credentials and S3 bucket name
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
S3_BUCKET_NAME = ''

# Configure boto3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

# Route for the home page with the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get user details from the form
    name = request.form['name']
    email = request.form['email']

    # Format data as text
    data = f"Name: {name}\nEmail: {email}"

    # Write data to a temporary text file
    filename = 'user_details.txt'
    with open(filename, 'w') as file:
        file.write(data)

    # Upload file to S3 bucket
    try:
        s3.upload_file(filename, S3_BUCKET_NAME, filename)
        os.remove(filename)  # Remove temporary file after upload
        return render_template('success.html')
    except NoCredentialsError:
        return render_template('error.html')

# Route to handle file download
@app.route('/download')
def download():
    # Specify the file to download
    filename = 'user_details.txt'

    # Download file from S3 bucket
    try:
        s3.download_file(S3_BUCKET_NAME, filename, filename)
        return send_file(filename, as_attachment=True)
    except NoCredentialsError:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
