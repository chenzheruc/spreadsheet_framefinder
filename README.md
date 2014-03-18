Senbazuru spreadsheet framefinder
=======================

Introduction
-----------------------
Senbazuru is a prototype spreadsheet database management system (SSDBMS), which is able to extract relational information from spreadsheets. It opens up opportunities for integration among spreadsheets and with relational sources.
Senbazuru allows users to search for relevant spreadsheets in a large corpus, probabilistically constructs a relational version of the data, and offers relational operations over the resulting extracted data (including select and join).

The goal of the Senbazuru spreadsheet framefinder is to identify the value region and the top
and left attribute regions in a spreadsheet. 
This program takes a raw spreadsheet and assigns each row of the spreadsheet
to one of the following categories: title, header, data or footnote. 

For more information please visit: http://www.eecs.umich.edu/db/sheets/

Dependencies
-----------------------
Please install the following packages first:

CRF++: http://crfpp.googlecode.com/svn/trunk/doc/index.html
xlrd python package: https://pypi.python.org/pypi/xlrd

How to use
-----------------------

1, Please specify the installed CRF++ directory in senbazuru/framefinder/const/

E.g. _crfppdir = '/home/cz/tools/CRF++-0.58'

2, Run the program by type the following commands: 

cd senbazuru/framefinder/

python framefinder.py

3, The program runs successfully if you can see the row prediction results in 
/senbazuru/data/predictsheets. 




