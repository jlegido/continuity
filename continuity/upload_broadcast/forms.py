# -*- coding: utf-8 -*-

# Debug
from logging import getLogger, FileHandler, Formatter, INFO
handler = FileHandler('/tmp/log')
logger = getLogger('audio_date_formatter')
formatter = Formatter( '%(asctime)s - %(lineno)s: %(levelname)s %(message)s' )
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(INFO)
# End Debug

from django.forms import Form, DateField, FileField, DateInput, ValidationError
from datetime import date
from django.conf import settings
from django.core import validators
from subprocess import check_output, CalledProcessError

from functools import partial
DateInput = partial(DateInput, {'class': 'datepicker'})

today = date.today().strftime(settings.BROADCAST_DATE_FORMAT)

class UploadBroadcastForm(Form):
    broadcast_date = DateField(label = "Data d'emissió del programa",
                               initial = today,
                               input_formats = [
                                               settings.BROADCAST_DATE_FORMAT],
                               widget=DateInput())
    audio_file = FileField(label = "Arxiu d'audio en format .mp3")

    def clean_broadcast_date(self):
        """broadcast_date should be today or future date"""
        data = self.cleaned_data['broadcast_date']
        if data < date.today():
            raise ValidationError("La data d'emissió ha de ser igual o \
                                   posterior a avui")
        return data

    '''
    def clean_audio_file(self):
        """check audio file is .mp3"""
        # Looks like the safer method is to save the file then file(myfile)
        # So I just document here how to do it, but I will not validate
        data = self.cleaned_data['audio_file']
        file_type = data.content_type
        # mp3 -> audio/mpeg ogg -> video/ogg
    '''
