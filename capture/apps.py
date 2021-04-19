from django.apps import AppConfig
import logging
from multiprocessing import Queue
import logging
import boto3
import os
import time
from multiprocessing import Process
from queue import  Empty


class UploadWorker:

    def __init__(self):
        self.queue = Queue()
        self.logger = logging.getLogger()

    def upload_to_s3(self, file_loc, new_loc, filename, logger):
        BUCKET = os.getenv("BUCKET")
        logging.info("Attempting s3 upload")
        try:
            session = boto3.Session(aws_access_key_id=os.getenv("AWSKEY"),
                                    aws_secret_access_key=os.getenv("AWSSECRET"))
            s3 = session.client("s3")

            # upload full size image
            s3.upload_file(file_loc, BUCKET, filename,
                           ExtraArgs={'ACL': 'public-read', 'ContentType': "image/jpeg"})
            # upload thumbnail
            s3.upload_file(new_loc, BUCKET, 'thumbs/%s' % filename,
                           ExtraArgs={'ACL': 'public-read', 'ContentType': "image/jpeg"})
            logging.info("Images successfully uploaded to S3")
        except:
            return False
        return True

    def worker(self, queue: Queue, logger):
        logger.info("Worker started")
        while True:
            try:
                job = self.queue.get(timeout=5)
                logger.info("Got upload job from queue")
                file_loc, new_loc, filename = job
                if self.upload_to_s3(file_loc, new_loc, filename, logger):
                    logger.info("Job successfully uploaded")
                    continue
                else:
                    # Put job back into queue
                    queue.put(job)
                    logger.warn("Failed to upload to S3. Placing job into queue and sleeping for 60 seconds")
                    logger.info(f"Currenty {queue.qsize()} items in the queue")
                    time.sleep(60)
            except Empty:
                continue

    def start_worker(self):
        self.logger.info("Starting worker...")
        process = Process(target=self.worker, args=(self.queue, self.logger), daemon=True)
        process.start()


class CaptureConfig(AppConfig):
    name = 'capture'

    def ready(self):
        pass
