'''
Created on Sep 26, 2012

@author: cz
'''


_sheetdir = '/home/cz/data/saus/trainsheets'
_crffeadir = '/home/cz/data/saus/crf_fea'
_crfpredictdir = '/home/cz/data/saus/crf_predict'

_crfppdir = '/home/cz/tools/CRF++-0.58'
_crfpptemplatepath = '/home/cz/tools/CRF++-0.58/example/sheets/template'
_crftraindatapath_saus = '/home/cz/tools/CRF++-0.58/example/framefinder/saus_train.data'
_crftraindatapath_web = '/home/cz/tools/CRF++-0.58/example/framefinder/web_train.data'

_crftempdir = '/home/cz/tools/CRF++-0.58/example/sheets'




_cube_totalwords = ['total', 'all']
_cube_spcharset = set(['<', '#', '>', ';', '-', '//'])
#_cube_naset = set(['(na)', 'n/a', '(n/a)', '(x)', '-', '--', 'na', 'x', '(a)', '(z)', 'n', 'd'])
_cube_naset = set([ '-', '--', 'na', 'x', '(a)', '(z)', 'n', 'd', 'z', 'r', 'e'])


def _strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


def _parse_filename(cstr):
    filename, sheetname = cstr.split('.xls____')
    filename += '.xls'
    return filename, sheetname
    
def _construct_parse_filename(filename, sheetname):
    return filename + '____' + sheetname
