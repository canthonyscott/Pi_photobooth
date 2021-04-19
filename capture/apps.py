from django.apps import AppConfig
import logging
from views import

class CaptureConfig(AppConfig):
    name = 'capture'

    def ready(self):
        print("Appconfig Ready called")
