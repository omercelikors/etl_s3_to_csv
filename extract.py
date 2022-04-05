import configparser
import boto3
from botocore.exceptions import ClientError

class Extract():

	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.cfg')
		self.BUCKET_NAME = config.get('aws_credentials', 'BUCKET_NAME')
		self.AWS_ACCESS_KEY_ID = config.get('aws_credentials', 'AWS_ACCESS_KEY_ID')
		self.AWS_SECRET_ACCESS_KEY = config.get('aws_credentials', 'AWS_SECRET_ACCESS_KEY')
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

			return False
		
		return True

	def download_file(self):
		"""Download a file to an S3 bucket

		:return: True if file was uploaded, else False
		"""

		try:
			# downlaoding informative file from s3
			destination_path = f"{self.BASE_PATH_FOR_DOWNLOADING}{self.INFORMATIVE_FILE_NAME}"
			self.s3_client.download_file(self.BUCKET_NAME, self.INFORMATIVE_FILE_NAME, destination_path)
			# downlaoding indicative file from s3
			destination_path = f"{self.BASE_PATH_FOR_DOWNLOADING}{self.INDICATIVE_FILE_NAME}"
			self.s3_client.download_file(self.BUCKET_NAME, self.INDICATIVE_FILE_NAME, destination_path)
		except Exception as e:

			return False

		return True

	def get_file_objects(self):
		file_objects = {}

		target_path = f"{self.BASE_PATH_FOR_DOWNLOADING}{self.INFORMATIVE_FILE_NAME}"
		with open(target_path, 'r') as fp:
			file_objects[self.INFORMATIVE_FILE_NAME] = fp

		target_path = f"{self.BASE_PATH_FOR_DOWNLOADING}{self.INDICATIVE_FILE_NAME}"
		with open(target_path, 'r') as fp:
			file_objects[self.INDICATIVE_FILE_NAME] = fp

		return file_objects

	def run(self):
		# self.create_s3_bucket_client()
		# self.download_file()
		return self.get_file_objects()

# extract = Extract()
# extract.run()