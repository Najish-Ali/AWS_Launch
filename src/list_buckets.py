def list_s3_buckets(s3_client):
    """List all buckets in the S3 account"""
    try:
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return buckets
    except Exception as e:
        print(f"Error listing buckets: {e}")
        return []
