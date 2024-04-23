from flask import Flask, render_template, request, send_file
import boto3

app = Flask(_name_)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    write_to_s3(data)
    return "Data submitted successfully!"

@app.route('/download')
def download():
    # Download file from S3 Bucket
    s3 = boto3.client('s3')
    bucket_name = 'jenibucket'
    file_name = 'user_data.txt'
    s3.download_file(bucket_name, file_name, file_name)
    return send_file(file_name, as_attachment=True)

def write_to_s3(data):
    # Write data to text file
    with open('user_data.txt', 'w') as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")

    # Upload to S3 Bucket
    s3 = boto3.client('s3')
    bucket_name = 'jenibucket'
    file_name = 'user_data.txt'
    s3.upload_file(file_name, bucket_name, file_name)

if _name_ == '_main_':
    app.run(debug=True)