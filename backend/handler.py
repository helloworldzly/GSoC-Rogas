#coding = utf-8

from tornado import web
import config
from rogas import queryConsole
from rogas import configManager
from rogas.resultManager import QueryResult
import json

class BaseHandler(web.RequestHandler):
    """ base of handlers
    """
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.render(config.MAIN_HTML, setting_dict=configManager.getConfigDict())

class QueryHandler(BaseHandler):
    def post(self):
        actResult = dict() 
        tab_index = 0
        try:
            query = self.get_argument('query')
            tab_index = self.get_argument('tab_index')

            queryResult = queryConsole.start(query)
            actResult = {'tab_index': tab_index, 'result': queryResult.asReturnResult()}
        except Exception as reason: 
            actResult['tab_index'] = tab_index 
            actResult['result'] = QueryResult('string', str(reason)).asReturnResult()
            
        self.write(actResult)

class LoadResultHandler(BaseHandler):
    def post(self):
        actResult = dict() 
        tab_index = 0
        try:
            query_id = int(self.get_argument('query_id'))
            is_next = int(self.get_argument('is_next'))
            tab_index = self.get_argument('tab_index')

            queryResult = queryConsole.fetch(query_id, is_next)
            actResult = {'tab_index': tab_index, 'result': queryResult.asReturnResult()}
        except Exception as reason: 
            actResult['tab_index'] = tab_index 
            actResult['result'] = QueryResult('string', str(reason)).asReturnResult()

        self.write(actResult)

class ConfigHandler(BaseHandler):
    def post(self):
        try:
            config_dict_str = self.get_argument('config')
            config_dict = json.loads(config_dict_str)
            configManager.updateConfig(config_dict)
        except Exception as reason: 
            print 'update config error:', reason
        self.write({"state": "done"})

class RelationCoreInfoHandler(BaseHandler):
    def post(self):
        actResult = dict() 
        tab_index = 0
        try:
            tab_index = self.get_argument('tab_index')
            queryResult = queryConsole.getRelationCoreInfo()
            actResult = {'tab_index': tab_index, 'result': queryResult.asReturnResult()}
        except Exception as reason: 
            actResult['tab_index'] = tab_index 
            actResult['result'] = QueryResult('string', str(reason)).asReturnResult()

        self.write(actResult)

class GraphicalViewInfoHandler(BaseHandler):
    def post(self):
        actResult = dict() 
        tab_index = 0
        try:
            tab_index = self.get_argument('tab_index')
            queryResult = queryConsole.getGraphicalViewInfo()
            actResult = {'tab_index': tab_index, 'result': queryResult.asReturnResult()}
        except Exception as reason: 
            actResult['tab_index'] = tab_index 
            actResult['result'] = QueryResult('string', str(reason)).asReturnResult()

        self.write(actResult)

class RelationTableInfoHandler(BaseHandler):
    def post(self):
        actResult = dict() 
        tab_index = 0
        try:
            tab_index = self.get_argument('tab_index')
            table_name = self.get_argument('table_name')
            queryResult = queryConsole.getRelationTableInfo(table_name)
            actResult = {'tab_index': tab_index, 'result': queryResult.asReturnResult()}
        except Exception as reason: 
            actResult['tab_index'] = tab_index 
            actResult['result'] = QueryResult('string', str(reason)).asReturnResult()

        self.write(actResult)

class GraphicalGraphInfoHandler(BaseHandler):
    def post(self):
        actResult = dict() 
        tab_index = 0
        try:
            tab_index = self.get_argument('tab_index')
            queryResult = queryConsole.getGraphicalGraphInfo()
            actResult = {'tab_index': tab_index, 'result': queryResult.asReturnResult()}
        except Exception as reason: 
            actResult['tab_index'] = tab_index 
            actResult['result'] = QueryResult('string', str(reason)).asReturnResult()

        self.write(actResult)
