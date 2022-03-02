import boto3
from botocore.exceptions import ClientError

class Storage:
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def login(self,is_lambda=False):#Todo: Find a way to check access to S3 is corect

        if is_lambda==True:
            self.s3_client = boto3.client("s3")
        else:
                access_key = input("Enter your AWS access key ID: ")
                secret_key = input("Enter your AWS secret key: ")
                self.s3_client = boto3.client("s3", aws_access_key_id=access_key,
                                         aws_secret_access_key=secret_key)
                is_lambda=True
        return self.s3_client

    def list_objects_by_bucket_name(self, bucket_name=None):
        try:
            bucket_names = self.list_bucket_names()
            if bucket_name:
                if bucket_name in bucket_names:
                    self.list_bucket_objects(bucket_name)
                else:
                    print("The requested bucket could not be found")
            else:
                for bucket_name in bucket_names:
                    self.list_bucket_objects(bucket_name)

        except ClientError as e:
            raise Exception(f"Could not connect to storage: {e}")

    def list_bucket_objects(self, bucket_name):
        bucket_objects = self.s3_client.list_objects(Bucket=bucket_name).get('Contents')
        print(f"Bucket {bucket_name}")
        for obj in bucket_objects:
            print(f"\tFilename {obj.get('Key')}")

    def list_bucket_names(self) -> list:
        return [bucket.get('Name') for bucket in self.s3_client.list_buckets().get('Buckets')]

    def put_object(self, bucket, file_path, object_name=None) -> bool:
        # Upload the file
        try:
            if not object_name:
                object_name = file_path.split("/")[-1]
            self.s3_client.upload_file(file_path, bucket, object_name)
            #TOdo: if file exit, ask user to preform to diffrent file
            print("File uploaded successfully")
        except ClientError as e:
            print(f'Could not upload to storage: {e}')
            return False
        return True

    def delete_object(self, bucket, object_name):
        # Delete the file
        try:
            self.s3_client.delete_object(Bucket=bucket, Key=object_name)
            print("File successfully deleted")
        except ClientError as e:
            print(f'Could not delete from storage: {e}')
            return False
        return True



