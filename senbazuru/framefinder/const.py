'''
Created on Sep 26, 2012

@author: cz
'''


# directory to store the original spreadsheets
_sheetdir = '../data/testsheets'
# directory to store the output:
# each spreadsheet labeled with semantic labels for each row
_outputdir = '../data/predictsheets'

# directories to store intermediate results
_crftempdir = '../data/temp'
_crffeadir = _crftempdir + '/crf_fea'
_crfpredictdir = _crftempdir + '/crf_predict'

# template file for CRF++ to parse the provided features
_crfpptemplatepath = '../data/template'
# training data provided for 100 spreadsheets downloaded from http://www.census.gov/
_crftraindatapath = '../data/saus_train.data'

##################################################
# please specifiy the directory of CRF++
##################################################
# directory of installed CRF++
_crfppdir = '/home/cz/tools/CRF++-0.58'


