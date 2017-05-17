from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class CapturePhoto(View):

    def get(self, request):
        # todo render template containing a Big Button with some JS, and pass a photo:no context to template

        return render(request, 'capture/capture.html', {'photo':False})


    def post(self, request):
        # todo capture image, get link to file, render templaet again with photo:yes context.
        return HttpResponse("Post Response")
