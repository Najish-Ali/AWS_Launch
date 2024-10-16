import json

def load_aws_credentials():
    with open('secrets.json') as f:
        secrets = json.load(f)
    return secrets['AWS_ACCESS_KEY_ID'], secrets['AWS_SECRET_ACCESS_KEY'], secrets['AWS_REGION']
