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

        script_loc = os.path.join(BASE_DIR, 'dummy_capture.sh')

        # get string timestamp
        # timestamp = str(int(time.time()))
        # filename = 'image-' + timestamp + '.jpg'
        filename = 'test.jpg' # TESTING FOR DEV
        # generate file name
        file_loc = '/home/anthony/deploy/photos/%s' % filename
        # capture image and save to static dir
        subprocess.call([script_loc, file_loc])

        url = static(filename)
        return HttpResponse(url)
