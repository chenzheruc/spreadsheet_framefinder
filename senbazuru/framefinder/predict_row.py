'''
Created on Feb 5, 2012

@author: cz
'''

import os

from framefinder.load_sheets import LoadSheets
from framefinder.feature_crf import Feature_SheetRow
from framefinder.const import _crffeadir, _crfpredictdir, _crfppdir,\
    _crftraindatapath, _crftempdir, _crfpptemplatepath, _sheetdir, _outputdir

class RunCRFppCommands:

    def __init__(self):
        self.crftrainscript = _crfppdir + '/crf_learn'
        self.crftestscript = _crfppdir + '/crf_test'
        self.crfmodelpath = _crftempdir + '/model'

    def train(self):
        print 'Training CRF++ model... '
        cmd = self.crftrainscript+' -c 4.0 '+_crfpptemplatepath+' ' + _crftraindatapath + ' '+self.crfmodelpath
        os.system(cmd)

    def predict(self):
        for elt in os.listdir(_crffeadir):
            elt = elt.replace(' ', '\\ ')
            
            print 'Predicting sheet row labels for:', elt
            
            featurepath = _crffeadir + '/'+elt
            predictpath = _crfpredictdir + '/'+elt
            try:
                cmd = self.crftestscript+' -m ' +self.crfmodelpath+' '+ featurepath+' > '+predictpath
                os.system(cmd)
            except:
                raise
            
            break

    
 
class PredictSheetRows:
    def __init__(self):
        self.fea_row = Feature_SheetRow()
    
    def generate_from_sheetdir(self):

        'clean temp folder'
        cmd = 'rm '+_crftempdir+'/*/*'
        os.system(cmd)
            
        count = 0
        for elt in os.listdir(_sheetdir):
            if elt.find('xls') < 0:
                continue
            
#             if elt != '44.xls':
#                 continue
            
            try:
                print 'Processing', elt
                self.generate_from_sheetfile(elt)
                count += 1
                if count % 100 == 0:
                    print 'CURRENT:', count
            except:
                print 'Error processing', elt
                raise

    def generate_from_sheetfile(self, filename):
        filepath = _sheetdir+'/'+filename

        loadsheet = LoadSheets(filepath)
        sheetdict = loadsheet.load_sheetdict()

        for sheetname, mysheet in sheetdict.items():
            feadict = self.fea_row.generate_singular_feature_crf(mysheet, filename, sheetname)
            
            outpath = _crffeadir + '/' + filename+'____'+sheetname
            fout = open(outpath, 'w+')
            for row, feavec in feadict.items():
                fout.write(filename+'____'+sheetname.replace(' ', '__')+'____'+str(row)+' ')
                for item in feavec:
                    if item is True:
                        fout.write('1 ')
                    else:
                        fout.write('0 ')
                fout.write('Title\n')
            fout.close() 
            

class TransformOutput:
    def run(self):
        for elt in os.listdir(_crfpredictdir):
            predictpath = _crfpredictdir + '/' + elt
            outpath = _outputdir + '/' + elt
            fin = open(predictpath)
            fout = open(outpath, 'w+')
            
            for line in fin:
                strarr = line.strip().split()
                if len(strarr) == 0:
                    continue
                ckey = strarr[0]
                clabel = strarr[len(strarr)-1]
                
                strarr = ckey.strip().split('____')
                crow = int(strarr[len(strarr)-1])
                
                fout.write(str(crow+1)+'\t'+clabel+'\n')
            
            fout.close()
            fin.close()
            
if __name__ == '__main__':
    
    
    predict = PredictSheetRows()
    predict.generate_from_sheetdir()
     
    runcrfpp = RunCRFppCommands()
    runcrfpp.train()
    runcrfpp.predict()
    
    trans = TransformOutput()
    trans.run()


