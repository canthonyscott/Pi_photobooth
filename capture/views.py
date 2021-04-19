from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import subprocess
import os
import time
from Pi_photobooth.settings import BASE_DIR
import logging
import datetime
import boto3
from PIL import Image
from multiprocessing import Process, Queue

logging.basicConfig(filename=os.path.join(BASE_DIR, 'logging.txt'), level=logging.INFO)


@method_decorator(csrf_exempt, name='dispatch')
class CapturePhoto(View):

    def get(self, request):
        logging.info(str(datetime.datetime.now()) + ": CapturePhoto View - GET called")

        return render(request, 'capture/capture.html', {'photo':False})

    def post(self, request):
        logging.info(str(datetime.datetime.now()) + ": CapturePhoto View - POST called")


        script_loc = os.path.join(BASE_DIR, 'capture_photo.sh')
        copy_script = os.path.join(BASE_DIR, 'copy_photo.sh')

        # get string timestamp
        timestamp = str(int(time.time()))
        filename = 'IMAGE-' + timestamp + '.jpg'
        logging.info(str(datetime.datetime.now()) + ": Filename generated: " + filename)

        # generate file name
        file_loc = '/home/pi/PHOTOBOOTH/photos/%s' % filename

        # capture image and save to static dir
        proc = subprocess.Popen([script_loc, file_loc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, errs = proc.communicate(timeout=15)

        errs = str(errs)
        if errs.find('ERROR') != -1:
            # todo handle this error of not focusing
            logging.error(str(datetime.datetime.now()) + ": Camera couldn't focus")
            return HttpResponse(1)
        elif errs.find('No camera found') != -1:
            logging.error(str(datetime.datetime.now()) + ": CAMERA NOT FOUND")
            return HttpResponse(2)

        # copy to external HDD
        # try:
        #     subprocess.call([copy_script, file_loc])
        #     logging.info(str(datetime.datetime.now()) + ": file coped to external drive")
        #
        # except:
        #     logging.error(str(datetime.datetime.now()) + ": Failed to copy %s to drive" % file_loc)

        # create thumbnail for quick display
        logging.info(str(datetime.datetime.now()) + ": Creating thumbnail and saving")
        new_loc = '/home/pi/PHOTOBOOTH/photos/thumbs/%s' % filename
        image = Image.open(file_loc)
        new_image = image.resize((600, 400))
        new_image.save(new_loc)

        # upload photo to AWS bucket
        logging.info(str(datetime.datetime.now()) + ": Connecting to AWS")
        queue = Queue
        p = Process(target=self.upload_to_s3, args=(file_loc, new_loc, filename,))
        p.start()

        logging.info(str(datetime.datetime.now()) + ": generating url for display")
        url = '/photos/' + filename
        logging.info(str(datetime.datetime.now()) + ": sending url: %s" % url)

        return HttpResponse(url)

    def upload_to_s3(self, file_loc, new_loc, filename):
        BUCKET = 'myphotobooth.live'
        try:
            logging.info("Attempting s3 upload")
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
        except Exception as e:
            logging.error("Error uploading to S3")
            logging.error(e)
            return False

        return True

