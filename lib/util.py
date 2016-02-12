# -*- coding: utf-8 -*
# Filename: util.py

__author__ = 'Piratf'

import os, sys

_ME_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.normpath(os.path.join(_ME_PATH, '..', 'Resource'))
 
def getFilePath(filename=None):
    """ give a file(img, sound, font...) name, return full path name. """
    if filename is None:
        raise ValueError, 'must supply a filename'
 
    fileext = os.path.splitext(filename)[1]
    if fileext in ('.png', '.bmp', '.tga', '.jpg'):
        sub = 'Image'
    elif fileext in ('.ogg', '.mp3', '.wav'):
        sub = 'Media'
    elif fileext in ('.ttf',):
        sub = 'Font'
 
    filePath = os.path.join(DATA_PATH, sub, filename)
    print 'Will read', filePath
 
    if os.path.abspath(filePath):
        return filePath
    else:
        raise ValueError, "Cant open file `%s'." % filePath