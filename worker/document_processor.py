import os
import sys
# insert root directory into python module search path
sys.path.insert(1, os.getcwd())

from aws_sqs_consumer import Consumer, Message
import boto3

from config import (
    ACCOUNT_ID,
    REGION_NAME,
)


class DocumentProcessor(Consumer):
    def handle_message(self, message: Message):
        print("Received message: ", message.Body)
        job_body = json.loads(message.Body)
        document_url = job_body.get("document_url")
        process_result = self.perform(document_url)


    def update_rails_client(self, document_url, process_result):
        rails_client_host = "https://rails_client.in"
        rails_client_url = "/document_processings"
        rails_client_token = os.getenv("RAILS_CLIENT_TOKEN")
        data = {
            "document_processing": {
                "document_url": document_url,
                "extraction": process_result,
            }
        }
        headers = {
            'Authorization': f"Bearer {rails_client_token}"
        }
        r = requests.post(f"{rails_client_host}{rails_client_url}", json=data, headers=headers)


    def perform(self, document_url):
      # TODO: aspose-words client integration
      process_result = None
      self.update_rails_client(document_url, process_result)

      return process_result


session = boto3.Session(profile_name="sqs", region_name=REGION_NAME)
sqs_client = session.client("sqs")
queue_name = 'document_processor'
document_processor = DocumentProcessor(
    queue_url=f"https://sqs.{REGION_NAME}.amazonaws.com/{ACCOUNT_ID}/{queue_name}",
    polling_wait_time_ms=5,
    sqs_client=sqs_client,
)
print("Started DocumentProcessor worker")
document_processor.start()
