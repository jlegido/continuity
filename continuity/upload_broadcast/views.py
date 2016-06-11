# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forms import UploadBroadcastForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.conf import settings
#from aras import aras
#from aras.aras import Aras

# Debug
from logging import getLogger, FileHandler, Formatter, INFO
handler = FileHandler('/tmp/log')
logger = getLogger('audio_date_formatter')
formatter = Formatter( '%(asctime)s - %(lineno)s: %(levelname)s %(message)s' )
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(INFO)
# End Debug

@login_required
def upload_broadcast_form(request):
    """Prints/process the form to upload broadcast"""
    #logger.info(request.user)
    d = {}
    from aras.aras import Aras, NoAudioFile
    aras = Aras(str(request.user), settings.ARAS_CONF['block_path'],
                settings.ARAS_CONF['audio_tags'])
    if request.method == 'POST': # If the form has been submitted...
        # A form bound to the POST data
        d['form'] = UploadBroadcastForm(request.POST, request.FILES)
        if d['form'].is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # request.user is a SimpleLazyObject
            date_prefix = d['form'].cleaned_data['broadcast_date'].\
                                                   strftime(settings.ARAS_CONF\
                                                          ['file_date_format'])
            try:
                formatted_filename = aras.write_file(
                                                   request.FILES['audio_file'],
                                                   date_prefix)
            except NoAudioFile, e:
                d['result'] = (1, "L'arxiu no s'ha grabat perquè no és ni mp3\
                               ni ogg.")
            else:
                d['result'] = (0, "L'arxiu s'ha pujat correctament amb el nom\
                               %s" %(formatted_filename))
        else:
            # At least one form field validation failed
            pass
    else:
        d['form'] = UploadBroadcastForm() # An unbound form
    d['broadcast_list'] = aras.get_broadcasts()
    return render_to_response('upload_broadcast_form.html',d,\
           context_instance=RequestContext(request))

def logout(request):
    return redirect('/login/')
    #return HttpResponse("Hello, world!")
