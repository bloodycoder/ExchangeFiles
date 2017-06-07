#coding=utf-8 
# -*- coding:cp936 -*-
import re
import urls
from cgi import parse_qs
#from model import Model
class application:
    """
    造轮子计划1073(a clean python web frame):
    使用方法
    常量:self.method,用来判断是post,get
    内置的几个方法:getTemplate,getPost
    如果要访问数据库,
    Model.build_connect 
    Model.exec_ins()
    Model.close()
    """
    def __init__(self,environ,start_response):
        self.environ = environ
        self.start = start_response
        self.status = '200 OK'
        self.response_headers = [('Content-type','text/html')]
        self.urls = urls.urls
    def __iter__(self):
        self.method = self.environ['REQUEST_METHOD']
        content = self.getPage()
        self.start(self.status,self.response_headers)
        yield content
    def getPage(self):
        path = self.environ['PATH_INFO']
        for pattern in self.urls:
            m = re.match(pattern[0],path)
            if m:
                function = getattr(self,pattern[1])
                return function()
        return '404 not found'
    def getTemplate(self,tem_name,rep=0):
        #这个函数返回内容,tem_name是文件名字
        #参数rep是一个字典，默认为0
        f = open('template/'+tem_name)
        html = f.read()
        if(rep!=0):
            for to_replace in rep:
                strinfo = re.compile('\{\%\s*'+str(to_replace)+'\s*\%\}')
                html = strinfo.sub(rep[to_replace],html)
        return html
    def getPost(self,item):
        if(self.environ['REQUEST_METHOD'] == 'POST'):
            request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
            request_body = self.environ['wsgi.input'].read(request_body_size)
            d = parse_qs(request_body)
            return d.get(item,[])[0]
    """
    *********************************************
    *add your function here.                    *
    *For example                                *
    *def func_index(self):                      *
    *    self.status = '200 OK'                 *
    *    return self.getTemplate('about_me.htm')*
    *********************************************
    """
    def func_index(self):
        self.status = '200 OK'
        return self.getTemplate('about_me.htm')
    def func_comment(self):
        self.status = '200 OK'
        return self.getTemplate('about_me.htm',{'pig':'lol'})
    def get_environ(self):
        self.status = '200 OK'
        html = ''
        for x in self.environ:
            html = html + str(x) + ':::'+str(self.environ[x]) + '<br>'
        return html
    def get_majong(self):
        self.status = '200 OK'
        majongData = '{"init":[[1,17,4,3,23,25,26,18,7,2,17,7,25],[11,16,6,28,17,19,16,18,19,26,14,1,15],[8,3,35,27,27,16,29,22,6,28,35,14,26]],"rules":[2,0,63],"dow":2,"zhuang":400151,"huntile":35,"huangpai":0,"huuser":[400216],"u400163":{"ting":0,"wintype":0,"roundscore":-2,"score":[13,0,-2],"totalscore":-2,"xiapao":[1,1]},"u400151":{"ting":0,"wintype":0,"roundscore":-4,"score":[13,0,-4],"totalscore":-4,"xiapao":[3,3]},"u400216":{"ting":0,"wintype":0,"roundscore":6,"score":[13,0,6],"totalscore":6,"xiapao":[0,0]},"uids":[400163,400151,400216],"rounds":[[400151,0,25],[400151,13,1],[400216,0,4],[400216,13,22],[400163,0,14],[400163,13,1],[400151,0,13],[400151,13,28],[400216,0,9],[400216,13,9],[400163,0,7],[400163,13,14],[400151,0,14],[400151,13,11],[400216,0,1],[400216,13,1],[400163,0,12],[400163,13,12],[400151,0,9],[400151,13,9],[400216,0,23],[400216,13,23],[400163,0,11],[400163,13,11],[400151,0,8],[400151,13,8],[400216,0,21],[400216,13,21],[400163,0,1],[400163,13,23],[400151,0,12],[400151,13,6],[400216,0,21],[400216,13,21],[400163,0,4],[400163,13,17],[400151,0,28],[400151,13,28],[400216,0,11],[400216,13,11],[400163,0,11],[400163,13,11],[400151,0,2],[400151,13,2],[400216,0,15],[400216,13,8],[400163,0,5],[400163,13,1],[400151,0,6],[400151,13,6],[400216,0,3],[400216,10,-1]]}'
        js = 'setReplayData('+majongData+');'
        return js
    def post_test(self):
        self.status = '200 OK'
        if(self.method == 'GET'):
            return self.getTemplate('post.html')
        elif(self.method == 'POST'):
            html = ''+self.getPost('fname')+'<br>'
            for x in self.environ:
                html = html + str(x) + ':::'+ str(self.environ[x])+'<br>'
            return html
