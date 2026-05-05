import boto3
import json
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

bucket_name = "my-static-site-1810-khushbu"  # change if needed

# Create bucket
try:
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'}
    )
    print("Bucket created")
except ClientError as e:
    print(e)

# Upload file
try:
    s3.upload_file("index.html", bucket_name, "index.html",
                   ExtraArgs={'ContentType': 'text/html'})
    print("File uploaded")
except ClientError as e:
    print(e)

# Enable website hosting
s3_resource = boto3.resource('s3')
website = s3_resource.BucketWebsite(bucket_name)

website.put(
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'index.html'}
    }
)

# Make public
policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{bucket_name}/*"
    }]
}

s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))

print("Website ready!")

print(f"http://{bucket_name}.s3-website.ap-south-1.amazonaws.com")
