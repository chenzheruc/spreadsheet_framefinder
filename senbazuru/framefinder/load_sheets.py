'''
Created on Jan 10, 2012

@author: cz
'''
import xlrd, datetime
import string


class MySheet:
    def __init__(self):
        self.sheetdict = {}
        self.mergerowdict = {}
        self.maxcolnum = 0
        self.maxrownum = 0
        self.nrownum = 0 
        self.ncolnum = 0
         
        self.txt = ''
         
        self.mergestrarr = []
        self.mergecellset = []
    
    def add_merge_cell(self, row1, row2, col1, col2):
        for rownum in range(row1, row2):
#                for colnum in range(col1, col2):
            self.mergerowdict[rownum] = True
            for colnum in range(col1, col2):
                self.mergecellset.append((rownum, colnum))
        
    def insert_cell(self, rownum, colnum, nrownum, ncolnum, mtype, indents, alignstyle, \
                        borderstyle, bgcolor, boldflag, height, italicflag, underlineflag, value):
        self.nrownum, self.ncolnum = nrownum, ncolnum
        if rownum > self.maxrownum:
            self.maxrownum = rownum
        if colnum > self.maxcolnum:
            self.maxcolnum = colnum
        
        mycell = MyCell()
        mycell.init(value, mtype, indents, alignstyle, boldflag, \
                    borderstyle, bgcolor, height, italicflag, underlineflag)
        
        self.sheetdict[(rownum, colnum)] = mycell
        if mtype == 'str':
            self.txt += value+' '
     
   
        
class MyCell():
    
    def init(self, value, mtype, indents, alignstyle, boldflag, \
                    borderstyle, bgcolor, height, italicflag, underlineflag):
        self.cstr = value
        self.mtype = mtype
        self.indents = self.get_indents(indents)
        
        
        self.centeralign_flag, self.leftalign_flag, self.rightalign_flag = False, False, False
        if alignstyle == 1:
            self.leftalign_flag = True
        elif alignstyle == 2:
            self.centeralign_flag = True
        elif alignstyle == 3:
            self.rightalign_flag = True
        
        self.boldflag = False
        if boldflag == 1:
            self.boldflag = True
        
        self.bottomborder, self.upperborder, self.leftborder, self.rightborder = False, False, False, False
        if borderstyle[0] == '1':
            self.bottomborder = True
        if borderstyle[1] == '1':
            self.upperborder = True
        if borderstyle[2] == '1':
            self.leftborder = True
        if borderstyle[3] == '1':
            self.rightborder = True
            
        self.bgcolor = bgcolor
        self.height = height
        self.italic = italicflag
        self.underline = underlineflag
        
        self.mergecellcount = 1
        self.startcol = 0
    
    def writestr_alignstyle(self):
        if self.leftalign_flag:
            return '1'
        elif self.centeralign_flag:
            return '2'
        elif self.rightalign_flag:
            return '3'
        return '0'
    
    def writestr_bordstyle(self):
        cstr = ''
        if self.bottomborder:
            cstr += '1'
        else:
            cstr += '0'
        if self.upperborder:
            cstr += '1'
        else:
            cstr += '0'
        if self.leftborder:
            cstr += '1'
        else:
            cstr += '0'
        if self.rightborder:
            cstr += '1'
        else:
            cstr += '0'
        return cstr
        
    def get_indents(self, indents):
        if len(self.cstr) == 0:
            return 0
        for i in range(len(self.cstr)):
            if self.cstr[i] == ' ' or (self.cstr[i] in string.punctuation):
                continue
            else:
                break
        return i+indents*2
    
        
    def print_info(self):
        print self.cstr, self.mtype, self.indents
        print 'bold', self.boldflag
        print 'align', self.leftalign_flag, self.centeralign_flag, self.rightalign_flag
        print 'border', self.bottomborder, self.upperborder, self.leftborder, self.rightborder

    


class LoadSheets:
    def __init__(self, filepath):
        self.wb = xlrd.open_workbook(filepath, formatting_info=True)
        
    def load_sheetdict(self):
        sheetdict = {}
        
        for sheet_name in self.wb.sheet_names():
            
            cmysheet = MySheet()
            
            csheet = self.wb.sheet_by_name(sheet_name)

            for crange in csheet.merged_cells:
                row1, row2, col1, col2 = crange
                cmysheet.add_merge_cell(row1, row2, col1, col2)
    
            for rownum in range(csheet.nrows):
                for colnum in range(csheet.ncols):
                    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                    cell_type = csheet.cell_type(rownum, colnum)
                    if cell_type == 0 or cell_type >= 5:
                        continue
                    # Grab the cell
                    curcell = csheet.cell(rownum, colnum)
                    ctype = self.get_value_type(curcell)
                    if ctype is not None:
                        cstr = ''
                        if cell_type == 3:
                            try:
                                cstr = str(datetime.datetime(*xlrd.xldate_as_tuple(curcell.value, self.wb.datemode)))
                            except:
                                pass
                        else:
                            cstr = str(curcell.value).replace('\n', ' ')
                        
#                         print cstr
                            
                        indents = int(self.feature_indentation(csheet, rownum, colnum))
                        alignstyle = int(self.feature_align_style(csheet, rownum, colnum))
                        borderstyle = self.feature_border_style(csheet, rownum, colnum)
                        bgcolor = int(self.feature_font_bgcolor(csheet, rownum, colnum))
                        boldflag = int(self.feature_font_bold(csheet, rownum, colnum))
                        height = int(self.feature_font_height(csheet, rownum, colnum))
                        italicflag = int(self.feature_font_italic(csheet, rownum, colnum))
                        underlineflag = int(self.feature_font_underline(csheet, rownum, colnum))
                        
                        cmysheet.insert_cell(rownum, colnum, csheet.nrows, csheet.ncols, 
                                             ctype, indents, alignstyle, borderstyle, bgcolor, 
                                             boldflag, height, italicflag, underlineflag, cstr)
                        
            sheetdict[sheet_name] = cmysheet
                        
        return sheetdict
        
        
    def feature_indentation(self, csheet, rownum, colnum):
        cell_xf = self.wb.xf_list[csheet.cell_xf_index(rownum, colnum)]
        return str(cell_xf.alignment.indent_level)
        
#        0, 1, 2, 3
    def feature_align_style(self, csheet, rownum, colnum):
        cell_xf = self.wb.xf_list[csheet.cell_xf_index(rownum, colnum)]
        return str(cell_xf.alignment.hor_align)
        
    
    def feature_font_bold(self, csheet, rownum, colnum):
        cell_xf = self.wb.xf_list[csheet.cell_xf_index(rownum, colnum)]
        if self.wb.font_list[cell_xf.font_index].bold:
            return '1'
        return '0'
    
    def feature_font_height(self, csheet, rownum, colnum):
        cell_xf = self.wb.xf_list[csheet.cell_xf_index(rownum, colnum)]
        return str(self.wb.font_list[cell_xf.font_index].height)
    
    def feature_font_underline(self, csheet, rownum, colnum):
        cell_xf = self.wb.xf_list[csheet.cell_xf_index(rownum, colnum)]
        if self.wb.font_list[cell_xf.font_index].underline_type:
            return '1'
        return '0'
        
    def feature_font_italic(self, csheet, rownum, colnum):
        cell_xf = self.wb.xf_list[csheet.cell_xf_index(rownum, colnum)]
        if self.wb.font_list[cell_xf.font_index].italic:
            return '1'
        return '0'
    
    def feature_font_bgcolor(self, csheet, rownum, colnum):
        cell_xf = self.wb.xf_list[csheet.cell_xf_index(rownum, colnum)]
        bgx = cell_xf.background.pattern_colour_index
        return str(bgx)
    
    def feature_border_style(self, csheet, rownum, colnum):
        cell_xf = self.wb.xf_list[csheet.cell_xf_index(rownum, colnum)]
        
        borderstr = ''
        if cell_xf.border.top_line_style > 0:
            borderstr += '1'
        else:
            borderstr += '0'
            
        if cell_xf.border.bottom_line_style > 0:
            borderstr += '1'
        else:
            borderstr += '0'
            
        if cell_xf.border.left_line_style > 0:
            borderstr += '1'
        else:
            borderstr += '0'
        
        if cell_xf.border.right_line_style > 0:
            borderstr += '1'
        else:
            borderstr += '0'
        
        return borderstr
    
    def get_value_type(self, cell):
        val = cell.value
        try:
            if len(val.strip()) == 0:
                return None
            else:
                return 'str'
        except:
            pass
               
        try:
            if int(val)==float(val):
                return 'int'
        except:
            pass
        
        try:
            return 'float'
        except:
            return None 

