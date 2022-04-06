import configparser
import boto3
from botocore.exceptions import ClientError
import settings

class Extract:

	def __init__(self):
		config = configparser.ConfigParser()
		config.read('etl.cfg')

		self.BUCKET_NAME = settings.BUCKET_NAME
		self.AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
		self.AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY

		self.INFORMATIVE_FILE_NAME = config.get('files', 'INFORMATIVE_FILE_NAME')
		self.INDICATIVE_FILE_NAME = config.get('files', 'INDICATIVE_FILE_NAME')
		self.BASE_PATH_FOR_DOWNLOADING = config.get('path', 'BASE_PATH_FOR_DOWNLOADING')
		
	def create_s3_bucket_client(self):
		"""Create an S3 client

		:return: True if client created, else False
		"""

		try:
			self.s3_client = boto3.client("s3",
										  aws_access_key_id=self.AWS_ACCESS_KEY_ID, 
										  aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)
		except ClientError as e:
			print(e)
			return False
		
		return True

	def download_file(self):
		"""Download file from an S3 bucket

		:return: True if file was downloaded, else False
		"""

		try:
			# downlaoding informative file from s3
			destination_path = f"../{self.BASE_PATH_FOR_DOWNLOADING}{self.INFORMATIVE_FILE_NAME}"
			self.s3_client.download_file(self.BUCKET_NAME, self.INFORMATIVE_FILE_NAME, destination_path)
			# downlaoding indicative file from s3
			destination_path = f"../{self.BASE_PATH_FOR_DOWNLOADING}{self.INDICATIVE_FILE_NAME}"
			self.s3_client.download_file(self.BUCKET_NAME, self.INDICATIVE_FILE_NAME, destination_path)
		except Exception as e:
			print(e)
			return False

		return True

	def run(self):
		if self.create_s3_bucket_client():
			if self.download_file():
				return True
			else:
				return False
		return False