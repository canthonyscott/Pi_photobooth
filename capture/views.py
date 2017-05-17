from django.shortcuts import render, redirect, HttpResponse
from django.views import View


# Create your views here.
class CapturePhoto(View):

    def get(self, request):
        # todo render template containing a Big Button with some JS, and pass a photo:no context to template

        return render(request, 'capture/capture.html', {'photo':False})

    def post(self, request):
        # todo capture image, get link to file, render templaet again with photo:yes context.
        pass
