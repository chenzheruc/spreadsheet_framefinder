Senbazuru spreadsheet framefinder
=======================

Introduction
-----------------------
Senbazuru is a prototype spreadsheet database management system (SSDBMS), which is able to extract relational information from spreadsheets. It opens up opportunities for integration among spreadsheets and with relational sources.
Senbazuru allows users to search for relevant spreadsheets in a large corpus, probabilistically constructs a relational version of the data, and offers relational operations over the resulting extracted data (including select and join).

For more information please visit: http://www.eecs.umich.edu/db/sheets/

The goal of a spreadsheet framefinder is to identify the value region and the top
and left attribute regions in a spreadsheet. 
This program takes a raw spreadsheet and assigns each row of the spreadsheet
to one of the following categories: title, header, data or footnote. 


You can run it by typing: 


Dependencies
-----------------------

CRF++: http://crfpp.googlecode.com/svn/trunk/doc/index.html
