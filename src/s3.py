import logging
import boto3
import os
from botocore.exceptions import ClientError


class S3Sync:

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None):
        """

        :param aws_access_key_id:
        :param aws_secret_access_key:
        """
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.s3_client = boto3.client('s3', aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key)

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name)
            print(f"uploaded {file_name} to {bucket}")
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_dir(self, local_dir, s3_bucket, prefix):
        """

        :param local_dir: Local directory that has to be uploaded
        :param s3_bucket: Bucket to upload into.
        :return:
        """

        files = [f for f in os.listdir(local_dir) if os.path.isfile(os.path.join(local_dir, f))]
        for file in files:
            file_name = file.split("/")[-1]
            print(local_dir+'/'+file, prefix+"/"+file_name)
            self.upload_file(local_dir+'/'+file, s3_bucket, prefix+"/"+file_name)

    def upload(self, local_log_path, local_video_dir, s3_bucket, s3_log_path, s3_video_prefix):
        """

        :param local_log_path: Path to download log on local machine
        :param local_video_dir: Path to video buffer on local machine
        :param s3_bucket: S3 bucket to upload into
        :param s3_log_path: download log path in S3
        :param s3_video_prefix: Video buffer on S3
        :return:
        """
        self.upload_file(file_name=local_log_path, bucket=s3_bucket, object_name=s3_log_path)
        self.upload_dir(local_dir=local_video_dir, s3_bucket=s3_bucket, prefix=s3_video_prefix)

    def download_dir(self, bucket, prefix, local):
        """

        :param bucket: s3 bucket with target contents
        :param prefix: pattern to match in s3
        :param local: local path to folder in which to place files
        :return:
        """

        keys = []
        dirs = []
        next_token = ''
        base_kwargs = {
            'Bucket': bucket,
            'Prefix': prefix,
        }
        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != '':
                kwargs.update({'ContinuationToken': next_token})
            results = self.s3_client.list_objects_v2(**kwargs)
            contents = results.get('Contents')
            if not contents:
                print("Empty Directory ", prefix)
                return None
            for i in contents:
                k = i.get('Key')
                if k[-1] != '/':
                    keys.append(k)
                else:
                    dirs.append(k)
            next_token = results.get('NextContinuationToken')
        for d in dirs:
            dest_pathname = os.path.join(local, d)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
        for k in keys:
            dest_pathname = os.path.join(local, k.split("/")[-1])
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            self.s3_client.download_file(bucket, k, dest_pathname)

    def download(self, local_log_path, local_video_dir, bucket, s3_log_path, s3_video_prefix):
        """

        :param local_log_path: Download log on local machine
        :param local_video_dir: Video buffer on local machine
        :param bucket: S3 bucket to upload into
        :param s3_log_path: Download log path on S3
        :param s3_video_prefix: Video buffer path on S3
        :return:
        """

        print("Downloading ", s3_log_path)
        self.s3_client.download_file(bucket, s3_log_path, local_log_path)
        if not os.path.exists(local_video_dir):
            os.mkdir(local_video_dir)
        print("Downloading ", s3_video_prefix)
        self.download_dir(bucket=bucket, prefix=s3_video_prefix, local=local_video_dir)

    def empty_buffer(self, bucket, prefix):
        """

        :param bucket: S3 bucket
        :param prefix: prefix path that needs to be deleted
        :return:
        """

        s3 = boto3.resource('s3', aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key)
        bucket_obj = s3.Bucket(bucket)
        bucket_obj.objects.filter(Prefix=prefix).delete()

