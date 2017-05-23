from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.staticfiles.templatetags.staticfiles import static
import subprocess
import os
import time
from Pi_photobooth.settings import BASE_DIR
import logging
import datetime


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

        # filename = 'test.jpg' # TESTING FOR DEV
        # generate file name
        file_loc = '/home/pi/PHOTOBOOTH/photos/%s' % filename
        # capture image and save to static dir
        # todo handle error of photo not capturing because user is too close
        subprocess.call([script_loc, file_loc])

        # copy to external HDD
        try:
            subprocess.call([copy_script, file_loc])
            logging.info(str(datetime.datetime.now()) + ": file coped to external drive")

        except:
            logging.error(str(datetime.datetime.now()) + ": Failed to copy %s to drive" % file_loc)

            print("Can't copy file")

        url = '/photos/' + filename
        logging.info(str(datetime.datetime.now()) + ": sending url: %s" % url)

        return HttpResponse(url)
