from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.staticfiles.templatetags.staticfiles import static
import subprocess
import os
import time
from Pi_photobooth.settings import BASE_DIR


@method_decorator(csrf_exempt, name='dispatch')
class CapturePhoto(View):

    def get(self, request):
        # todo render template containing a Big Button with some JS, and pass a photo:no context to template

        return render(request, 'capture/capture.html', {'photo':False})


    def post(self, request):

        script_loc = os.path.join(BASE_DIR, 'capture_photo.sh')
        copy_script = os.path.join(BASE_DIR, 'copy_photo.sh')

        # get string timestamp
        timestamp = str(int(time.time()))
        filename = 'IMAGE-' + timestamp + '.jpg'
        # filename = 'test.jpg' # TESTING FOR DEV
        # generate file name
        file_loc = '/home/pi/PHOTOBOOTH/photos/%s' % filename
        # capture image and save to static dir
        subprocess.call([script_loc, file_loc])

        # copy to external HDD
        try:
            subprocess.call([copy_script, file_loc])
        except:
            print("Can't copy file")

        url = '/photos/' + filename
        return HttpResponse(url)
