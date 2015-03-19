'''
Created on Nov 20, 2011

@author: cz
'''

import re, string

        
        
class Feature_SheetRow:
    
    def __init__(self):
        self.naset = set(['(na)', 'n/a', '(n/a)', '(x)', '-', '--', 'z', '...'])
        self.spcharset = set(['<', '#', '>', ';', '$']) 
        self.myformat = FeatureFormat()
        self.goodrowset = []
        
    def generate_singular_feature_crf(self, mysheet, filename, sheetname):
        feadict = {}
        for crow in range(mysheet.nrownum):
            rowcelldict = {}
            for ccol in range(mysheet.ncolnum):
                if mysheet.sheetdict.has_key((crow, ccol)):
                    mycell = mysheet.sheetdict[(crow, ccol)]
                    rowcelldict[ccol] = mycell
#                remove all the blank lines
            if len(rowcelldict) == 0:
                continue
#            crowname = self.get_rowname(filename, sheetname, crow)
            if feadict.has_key(crow-1):
                blankflag = False
            else:
                blankflag = True
            feadict[crow] = self.generate_feature_by_row_crf(crow, rowcelldict, mysheet, blankflag)
            
        return feadict
    
    def generate_feature_by_row_crf(self, crow, rowcelldict, mysheet, blankflag):

        feavec = []        
        clinetxt = ''
        for ccol, mycell in rowcelldict.items():
            clinetxt += mycell.cstr + ' '      

#        layout features
        feavec.append(blankflag)
        feavec.append(self.feature_has_merge_cell(crow, mysheet))
        feavec.append(self.feature_reach_right_bound(crow, rowcelldict, mysheet.maxcolnum))
        feavec.append(self.feature_reach_left_bound(rowcelldict))
        feavec.append(self.feature_is_one_column(rowcelldict))
        feavec.append(self.feature_has_center_align_cell(crow, rowcelldict))
        feavec.append(self.feature_has_left_align_cell(crow, rowcelldict))
        feavec.append(self.feature_has_bold_font_cell(crow, rowcelldict))
        feavec.append(self.feature_indentation(clinetxt))
#        textual features
        feavec.append(self.feature_start_with_table(clinetxt))
        feavec.append(self.feature_start_with_punctation(clinetxt))
        feavec.append(self.feature_number_percent_high(rowcelldict))
        feavec.append(self.feature_digital_percent_high(rowcelldict))
        feavec.append(self.feature_alphabeta_all_capital(clinetxt))
        feavec.append(self.feature_alphabeta_start_with_capital(rowcelldict))
        feavec.append(self.feature_alphabeta_start_with_lowercase(rowcelldict))
        feavec.append(self.feature_alphabeta_cellnum_percent_high(rowcelldict))
        feavec.append(self.feature_alphabeta_percent_high(clinetxt))
        feavec.append(self.feature_contain_special_char(clinetxt))
        feavec.append(self.feature_contain_colon(clinetxt))
        feavec.append(self.feature_year_range_cellnum_high(rowcelldict))
        feavec.append(self.feature_year_range_percent_high(rowcelldict))
        feavec.append(self.feature_word_length_high(rowcelldict))
        
        return feavec

    def feature_one_variable_txt(self, predicate, rowname, flag):
        if flag==True:
            return self.myformat.onevariable(predicate, rowname)
        return None

#########################################################
####    row features
#########################################################

    def feature_is_row(self, rowname):
        return self.myformat.onevariable('IsRow', rowname)
    
    def feature_word_repeat_high(self, clinetxt, csheettxt):
        wordarr = re.split('[^A-Za-z]', clinetxt)
        reptcount, wordcount = 0, 0
        for cword in wordarr:
            if len(cword) == 0:
                continue
            wordcount += 1
            reptcount += csheettxt.count(cword)
        if wordcount == 0:
            return False
        if float(reptcount)/wordcount >= 2:
            return True
        return False
    
    def feature_word_length_high(self, rowcelldict):
        if len(rowcelldict) != 1:
            return False
        for crow, mycell in rowcelldict.items():
            cval = mycell.cstr
            if len(cval) > 40:
                return True
        return False
        
    
    def feature_indentation(self, clinetxt):
        for i in range(len(clinetxt)):
            if clinetxt[i] >= 'A' and clinetxt[i] <= 'Z':
                break
            if clinetxt[i] >= 'a' and clinetxt[i]<= 'z':
                break
            if clinetxt[i] >= '0' and clinetxt[i] <= '9':
                break
        if i > 0:
            return True
        return False

    def feature_has_merge_cell(self, crow, mysheet):
        if mysheet.mergerowdict.has_key(crow):
                return True
        return False
        
    def feature_reach_right_bound(self, crow, rowcelldict, ncolnum):
        if rowcelldict.has_key(ncolnum):
            return True
        return False
    
    def feature_reach_left_bound(self, rowcelldict):
        if rowcelldict.has_key(0):
            return True
        return False
    
#    rowcelldict[ccol] = (value, mtype, centerFlag, leftFlag, boldFlag)
    def feature_number_percent_high(self, rowcelldict):
        if len(rowcelldict) == 0:
            return False
        digitalcount = 0
#        print rowcelldict
        for ccol, mycell in rowcelldict.items():
            cstr = mycell.cstr
            if self.has_digits(cstr):
                digitalcount += 1
            elif self.is_na(cstr):
                digitalcount += 1
        if float(digitalcount)/len(rowcelldict) >= 0.6:
            return True
        return False
    
    def feature_digital_percent_high(self, rowcelldict):
        if len(rowcelldict) == 0:
            return False
        digitalcount = 0
#        print rowcelldict
        for ccol, mycell in rowcelldict.items():
            cstr = mycell.cstr
            if self.is_number(cstr):
                digitalcount += 1
            elif self.is_na(cstr):
                digitalcount += 1
        if float(digitalcount)/len(rowcelldict) >= 0.6:
            return True
        return False
    
    def feature_year_range_cellnum_high(self, rowcelldict):
        if len(rowcelldict) == 0:
            return False
        yearcount = 0
#        print rowcelldict
        for ccol, mycell in rowcelldict.items():
            cstr = mycell.cstr
            digitarr = self.get_numset(cstr)
            for item in digitarr:
                if item >= 1800 and item <= 2300:
                    yearcount += 1
        if yearcount >= 3:
            return True
        return False
    
    def feature_year_range_percent_high(self, rowcelldict):
        if len(rowcelldict) == 0:
            return False
        yearcount, totalcount = 0, 1
#        print rowcelldict
        for ccol, mycell in rowcelldict.items():
            cstr = mycell.cstr
            digitarr = self.get_numset(cstr)
            totalcount += len(digitarr)
            for item in digitarr:
                if item >= 1800 and item <= 2300:
                    yearcount += 1
        if float(yearcount)/totalcount >= 0.7:
            return True
        return False
    
    def feature_alphabeta_start_with_capital(self, rowcelldict):
        for ccol, mycell in rowcelldict.items():
            cstr, mtype = mycell.cstr, mycell.mtype
            if mtype != 'str':
                continue
            if len(cstr) == 0:
                continue
            if self.has_letter(cstr) and not (cstr[0]>='A' and cstr[0]<='Z'):
                return False
        return True
    
    def feature_alphabeta_start_with_lowercase(self, rowcelldict):
        ccol = min(rowcelldict.keys())
        cstr = rowcelldict[ccol].cstr
        if len(cstr) == 0:
            return False
        if self.has_letter(cstr) and cstr[0]>='a' and cstr[0]<='z':
            return True
        return False
    
    def feature_alphabeta_all_capital(self, clinetxt):
        capitalcount = 0
        for i in range(len(clinetxt)):
            if clinetxt[i]>='A' and clinetxt[i]<='Z':
                capitalcount += 1
            elif clinetxt[i]>='a' and clinetxt[i]<='z':
                return False
        if capitalcount > 0:
            return True
        return False
    
    def feature_alphabeta_cellnum_percent_high(self, rowcelldict):
        pattern = re.compile('[A-Za-z]', re.IGNORECASE)
        count = 0;
        for ccol, mycell in rowcelldict.items():
            cstr, mtype = mycell.cstr, mycell.mtype
            if mtype != 'str':
                continue
            if pattern.search(unicode(cstr)):
                count += 1
        if float(count)/len(rowcelldict) >= 0.6:
            return True
        return False
     
    def feature_alphabeta_percent_high(self, clinetxt):
        count = 0
        for i in range(len(clinetxt)):
            if clinetxt[i]>='A' and clinetxt[i]<='Z':
                count += 1
            elif clinetxt[i]>='a' and clinetxt[i]<='z':
                count += 1
        if float(count)/len(clinetxt) >= 0.6:
            return True
        return False
    
    
    def feature_contain_colon(self, clinetxt):
        if string.find(clinetxt, ':') >=0 :
            return True
        return False
    
    
    def feature_contain_special_char(self, clinetxt):
        for i in range(len(clinetxt)):
            if clinetxt[i] in self.spcharset:
                return True
        return False
    
    def feature_is_one_column(self, rowcelldict):
        if len(rowcelldict) == 1:
            return True
        return False
    
#    rowcelldict[ccol] = (value, mtype, centerFlag, leftFlag, boldFlag)
    def feature_has_center_align_cell(self, crow, rowcelldict):
        for ccol, mycell in rowcelldict.items():
            if mycell.centeralign_flag:
                return True
        return False
    
    def feature_has_left_align_cell(self, rownum, rowcelldict):
#        print rowcelldict
        for ccol, mycell in rowcelldict.items():
            if mycell.leftalign_flag:
                return True
        return False
    
    def feature_has_bold_font_cell(self, rownum, rowcelldict):
        for ccol, mycell in rowcelldict.items():
            if mycell.boldflag:
                return True
        return False
    
    def feature_start_with_table(self, clinetxt):
        if len(clinetxt) == 0:
            return False
        if clinetxt.strip().startswith("Table"):
            return True
        return False
    
    def feature_start_with_punctation(self, clinetxt):
        if len(clinetxt) == 0:
            return False
        
        cchar = clinetxt[0]
        if self.has_digits(cchar):
            return False
        if self.has_letter(cchar):
            return False
        return True 
    
    def feature_end_with_and(self, clinetxt):
        if len(clinetxt) == 0:
            return False
        if clinetxt.strip().lower().endswith("and"):
            return True
        if clinetxt.strip().endswith(','):
            return True
        return False 
    
    def feature_is_first_row(self, rownum):
        if rownum == 0:
            return True
        return False
    
    def feature_is_last_row(self, rownum, maxrownum):
        if rownum == maxrownum:
            return True
        return False
    
#########################################################

           
    def is_number(self, cstr):
        try:
            float(cstr) # for int, long and float
        except:
            return False        
        return True

    def has_letter(self, cstr):
        for cchar in cstr: 
            if cchar >= 'a' and cchar <= 'z':
                return True
            if cchar >= 'A' and cchar <= 'Z':
                return True
        return False

    def has_digits(self, cstr):
        for cchar in cstr:
            if cchar >= '0' and cchar <= '9':
                return True
        return False
    
    def is_na(self, cstr):
        if cstr.strip().lower() in self.naset:
            return True
        return False
    
    def get_numset(self, cstr):
        carr = cstr.split(' ')
        numset = []
        for item in carr:
            try:
                numset.append(float(item))
            except:
                pass
        return numset
    
    def get_rowname(self, filename, csheetname, rownum):
        pfilename = filename.replace('.', '_')
        psheetname = csheetname.replace(' ', '_')
        return 'S'+pfilename+'____'+psheetname+'____'+str(rownum)
    
    def parseFilename(self, filepath):
        iarr = filepath.split('/')
        return iarr[len(iarr)-1]

         

class FeatureFormat():
    def __init__(self):
        pass
    def onevariable(self, name, vari1):
        return name+'('+vari1+')\n'
    def twovariable(self, name, vari1, vari2):
        return name+'('+vari1+','+vari2+')\n'


    
