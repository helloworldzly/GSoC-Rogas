#coding = utf-8

from tornado import web
import config
from rogas import queryConsole

class BaseHandler(web.RequestHandler):
    """ base of handlers
    """
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.render(config.MAIN_HTML)

class QueryHandler(BaseHandler):
    def post(self):
        query = self.get_argument('query')
        tab_index = self.get_argument('tab_index')

        queryResult = queryConsole.start(query)
        actResult = {'tab_index': tab_index, 'result': queryResult.asDict()}
        self.write(actResult)

class LoadResultHandler(BaseHandler):
    def post(self):
        query_id = int(self.get_argument('query_id'))
        is_next = int(self.get_argument('is_next'))
        tab_index = self.get_argument('tab_index')

        queryResult = queryConsole.fetch(query_id, is_next)
        actResult = {'tab_index': tab_index, 'result': queryResult.asDict()}
        self.write(actResult)
