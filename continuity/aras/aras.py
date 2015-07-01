#!/usr/bin/python

# Debug
from logging import getLogger, FileHandler, Formatter, INFO
handler = FileHandler('/tmp/log')
logger = getLogger('audio_date_formatter')
formatter = Formatter( '%(asctime)s - %(lineno)s: %(levelname)s %(message)s' )
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(INFO)
# End Debug

from os import listdir, makedirs, remove, rename
from os.path import dirname, exists, join, splitext
from subprocess import check_output
from datetime import date

class NoAudioFile(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NoFileDestinationDir(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Aras(object):

    def __init__(self, program = None, path_config_file = None,
                 audio_tags = None):
        """Class constructor"""
        self.program = program
        self.path_config_file = path_config_file
        self.audio_tags = audio_tags
        self.list_broadcasts = []
        self.path_broadcasts = self._get_file_destination_dir()

    def _get_file_destination_dir(self):
        """Parses aras.block and gets the path where store the file"""
        for line in open(self.path_config_file,'r').readlines():
            if self.program in line:
                return dirname(line.split()[2].replace('file://', ''))
        raise NoFileDestinationDir(self.program)

    def _get_audio_type(self, path_file):
        "Returns either .mp3 or .ogg"
        file_type = check_output(['file', path_file]).split(': ')[1].strip()
        if any(tag in file_type for tag in self.audio_tags['mp3']):
            return '.mp3'
        elif any(tag in file_type for tag in self.audio_tags['ogg']):
            return '.ogg'
        raise NoAudioFile(path_file)

    # https://docs.djangoproject.com/en/1.8/topics/http/file-uploads/
    def write_file(self, f, date_prefix):
        """Writes to disk audio file uploaded via web form then checks type"""
        #path = self._get_file_destination_dir()
        #path_file = '%s/%s' %(path, f)
        path_file = '%s/%s' %(self.path_broadcasts, f)
        if not exists(dirname(path_file)):
            makedirs(dirname(path_file))
        with open(path_file, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        # Now I check that file is either .mp3 or .ogg. If not remove it
        try:
            extension = self._get_audio_type(path_file)
        except NoAudioFile, e:
            remove(path_file)
            raise
        else:
            # File is either .mp3 or .ogg. Let's rename it
            formatted_filename = '%s-%s%s' %(date_prefix, self.program, extension)
            #rename(path_file, join(path, formatted_filename))
            rename(path_file, join(self.path_broadcasts, formatted_filename))
        return formatted_filename
 
    def get_broadcasts(self):
        """Returns a list of all broadcasts of the program"""
        try:
            # No idea why list is not sorted
            list = listdir(self.path_broadcasts)
        except OSError, e:
            return []
        list.sort()
        return list
