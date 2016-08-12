'''
The databaseInfoProcessor is to manage the database info, including realtion core and graphical view

@author: Yan Xiao
'''

import subprocess
import config
import StringIO 
from resultManager import QueryResult, TableResult

def getRelationCoreInfo():
    cmd = "psql -d " + config.DB + " -c '\d'"
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    infoString = pipe.read()
    inputStream = StringIO.StringIO(infoString)
    relationCoreLines = inputStream.readlines()
    print relationCoreLines
    
    queryResult = QueryResult()
    if len(relationCoreLines) < 2:
        queryResult.setType("string")
        queryResult.setContent("Empty relation core information")
    else:
        queryResult.setType("table")
        #table header
        tableHeader = relationCoreLines[1]
        tableHeaderLst = [str(col).strip() for col in tableHeader.split('|')]
        #table content
        rowsContent = []
        for index in xrange(3, len(relationCoreLines)-2):
            oneRowContent = [str(col).strip() for col in relationCoreLines[index].split('|')]
            rowsContent.append(oneRowContent)
        queryResult.setContent(TableResult(tableHeaderLst, rowsContent))

    return queryResult
