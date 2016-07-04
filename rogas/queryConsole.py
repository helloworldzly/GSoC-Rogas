'''
The queryConsole is to read the query input, show query results and display error information

@author: minjian
'''
import psycopg2
import queryParser
import matGraphProcessor
import time
import os
from resultManager import QueryResult, GraphResult, TableResult, TableGraphResult, SingleResultManager
import config

#starts to execute the input query
def execQuery(conn, cur, executeCommand):
    queryResult = QueryResult()
    lowerCaseCommand = executeCommand.lower()
    
    #graph query contains rank, cluster and path operation
    if ("rank" in lowerCaseCommand) or ("cluster" in lowerCaseCommand)or ("path" in lowerCaseCommand):
        startTime = time.time()
        
        newExecuteCommand, graphOperationInfo = queryParser.queryAnalyse(executeCommand, conn, cur)
        #newExecuteCommand = graphProcessor.queryAnalyse(executeCommand, conn, cur)
        #print "Total operation time is: ", (time.time() - startTime)
        #print newExecuteCommand  #for debug
        cur.execute(newExecuteCommand[:]) #remove the first space

        queryResult.setType("table_graph")
        tableResult = SingleResultManager.extractTableResultFromCursor(cur)
        graphResult = GraphResult(graphOperationInfo[0], graphOperationInfo[1], graphOperationInfo[2], graphOperationInfo[3]) 
        graphResult.generateGraph()
        queryResult.setContent(TableGraphResult(tableResult, graphResult))
    
    #query about creating or dropping a materialised graph    
    elif ("create" in lowerCaseCommand or "drop" in lowerCaseCommand) and ("ungraph" in lowerCaseCommand or "digraph" in lowerCaseCommand):
        newExecuteCommand = matGraphProcessor.processCommand(executeCommand, conn, cur)
        eIndex = newExecuteCommand.index("view")
        cur.execute(newExecuteCommand[:]) #remove the first space
        #print newExecuteCommand[:eIndex] + "graph"
        queryResult.setType("string")
        queryResult.setContent("Graph Operation Done")
    
    #normal relational query without any graph functions
    else:
        #print executeCommand[:]
        cur.execute(executeCommand[:])  #remove the first space
        queryResult.setType("table")
        queryResult.setContent(SingleResultManager.extractTableResultFromCursor(cur))

    conn.commit() 
    return queryResult

SingleConnection = psycopg2.connect(database=config.DB, user=config.DB_USER, password=config.DB_PASSWORD, port=config.DB_PORT)

def prepare():
    homeDir = os.environ['HOME']
    memDir = "/dev/shm"
    
    if os.path.exists(homeDir + "/RG_Mat_Graph") == False:
        os.mkdir(homeDir + "/RG_Mat_Graph")
        
    if os.path.exists(memDir + "/RG_Tmp_Graph") == False:
        os.mkdir(memDir + "/RG_Tmp_Graph")    

def start(query):
    cur = SingleConnection.cursor()
    
    start_time = time.time()
    queryResult = QueryResult()
    try:
        queryResult = execQuery(SingleConnection, cur, query)
        #print "Total query time is: ", (time.time() - start_time)
        os.system("rm -fr /dev/shm/RG_Tmp_Graph/*")  #clear graphs on-the-fly
    except Exception as reason:
        queryResult.setType("string")
        queryResult.setContent(str(reason))

    needKeepCursor = False
    if queryResult.result_type == "table":
        needKeepCursor = (queryResult.result_content.is_end == 0)
    elif queryResult.result_type == "table_graph":
        needKeepCursor = (queryResult.result_content.table_result.is_end == 0)
    if needKeepCursor == False:
        cur.close()

    SingleConnection.rollback()

    return queryResult

def fetch(query_id, is_next):
    queryResult = QueryResult()

    queryResult.setType("table")
    queryResult.setContent(SingleResultManager.extractTableResultById(query_id, is_next))

    return queryResult

def readTable(table_name):
    cur = SingleConnection.cursor()
    cur.execute('select * from ' + table_name + ';') 
    tableResult = SingleResultManager.extractTableResultFromCursor(cur, is_all=True)
    cur.close()

    SingleConnection.commit() 
    SingleConnection.rollback()
    return tableResult