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
from capture.apps import UploadWorker

logging = logging.getLogger()
upload_worker = UploadWorker()
upload_worker.start_worker()

@method_decorator(csrf_exempt, name='dispatch')
class CapturePhoto(View):

    def get(self, request):
        logging.info(str(datetime.datetime.now()) + ": CapturePhoto View - GET called")

        return render(request, 'capture/capture.html', {'photo':False})

    def post(self, request):
        logging.info(str(datetime.datetime.now()) + ": CapturePhoto View - POST called")


        script_loc = os.path.join(BASE_DIR, 'capture_photo.sh')

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

        # create thumbnail for quick display
        logging.info(str(datetime.datetime.now()) + ": Creating thumbnail and saving")
        new_loc = '/home/pi/PHOTOBOOTH/photos/thumbs/%s' % filename
        image = Image.open(file_loc)
        new_image = image.resize((388, 259))
        new_image.save(new_loc)

        # upload photo to AWS bucket
        logging.info("Putting file in queue...")
        upload_worker.queue.put((file_loc, new_loc, filename))

        logging.info(str(datetime.datetime.now()) + ": generating url for display")
        url = '/photos/' + filename
        logging.info(str(datetime.datetime.now()) + ": sending url: %s" % url)

        return HttpResponse(url)


