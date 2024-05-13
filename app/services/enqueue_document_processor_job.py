import boto3
import json


class EnqueueDocumentProcessorJob:
    def __init__(self, document_url):
        from config import (
            ACCOUNT_ID,
            REGION_NAME,
        )
        self.document_url = document_url
        self.session = boto3.Session(profile_name='sqs', region_name=REGION_NAME)
        self.queue_name = 'document_processor'
        self.queue_url = f"https://sqs.{REGION_NAME}.amazonaws.com/{ACCOUNT_ID}/{self.queue_name}"


    def enqueue_sqs(self):
        sqs = self.session.client('sqs', region_name=REGION_NAME)

        try:
            message_body = json.dumps({
                'document_url': self.document_url,
            })
            sqs.send_message(QueueUrl=self.queue_url, MessageBody=message_body)
        except Exception as e:
            print(e)


    def perform(self):
        self.enqueue_sqs()
