from django.apps import AppConfig
import logging

class CaptureConfig(AppConfig):
    name = 'capture'

    def ready(self):
        print("Appconfig Ready called")
