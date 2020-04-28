# app.py
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET

#Set up the S3 bucket with our credentials
# Add your own key and id
s3 = boto3.resource('s3', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

app = Flask(__name__)
Bootstrap(app)

# here is how we are handling routing with flask:
@app.route('/')
def index():
    return render_template('index.html')
    #return "Hello World!", 200

@app.route('/files')
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()

    return render_template('files.html', my_bucket=my_bucket, files=summaries)

if __name__ == '__main__':
    app.run()
