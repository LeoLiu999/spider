# -*- coding: utf-8 -*-

import re
from lxml import etree
import Dbmanager
import time

class BaseSite:

    def parseContent(self, params):
        pass


class ShuqugeSite(BaseSite):

    def parseContent(self, params):

        bookDict =  self.matchBookUrl(params['url'])
        if bookDict is not None:
            return self.matchBookContent(bookDict, params['content'])

        articleDict = self.matchArticleUrl(params['url'])
        if articleDict is not None:
            return self.matchArticleContent(articleDict, params['content'])


    def matchBookUrl(self, url):
        matchs = re.search('/txt/(\d+)/index.html', url)

        if matchs is not None:
            return {'book_id': matchs.group(1)}

        return None

    def matchBookContent(self, bookDict, content):

        #匹配内容

        bookId = bookDict['book_id']

        html=etree.HTML(content)

        h2 = html.xpath(u"/html/body/div[@class='book']/div[@class='info']/h2/text()")

        bookname = h2[0]

        descShow = html.xpath(u"/html/body/div[@class='book']/div[@class='info']/div[@class='intro']/text()")
        descHide = html.xpath(u"/html/body/div[@class='book']/div[@class='info']/div[@class='intro']/span[@class='noshow']/text()")

        desc = descShow[1] + descHide[0]

        info = html.xpath(u"/html/body/div[@class='book']/div[@class='info']/div[@class='small']/span/text()")

        author = info[0][3:]

        category = info[1][3:]

        state = info[2][3:]

        words = info[3][3:]

        img = html.xpath(u"/html/body/div[@class='book']/div[@class='info']/div[@class='cover']/img/@src")

        cover = img[0]

        intoMysqlParams = {
            'name' : str(bookname),
            'relation_flag': int(bookId),
            'origin_site': 'shuquge',
            'author' : str(author),
            'category' : str(category),
            'words' : int(words),
            'state' : self.makeState(state),
            'description': str(desc),
            'cover' : str(cover)
        }

        #进数据库
        db = Dbmanager.Dbmanager()
        db.addBook(intoMysqlParams)


    def makeState(self, state):
        if state == '连载中':
            return 'writing'
        else:
            return 'finish'


    def matchArticleUrl(self, url):
        matchs = re.search('/txt/(\d+)/(\d+).html', url)

        if matchs is not None:
            return {'book_id': matchs.group(1), 'article_id': matchs.group(2)}

        return None

    def matchArticleContent(self, articleDict, content):

        #匹配内容
        html = etree.HTML(content)

        h1 = html.xpath(u"/html/body/div[contains(@class, 'book')]/div[@class='content']/h1/text()")

        title = h1[0]

        content = html.xpath(u"/html/body/div[contains(@class, 'book')]/div[@class='content']/div[@id='content']/text()")

        content = ''.join(content[0:-3])

        #进数据库
        intoMysqlParams = {
            'relation_flag': int(articleDict['article_id']),
            'parent_flag' : int(articleDict['book_id']),
            'origin_site': 'shuquge',
            'title': str(title),
            'content': str(content),
            'sort_weight' : int(articleDict['article_id']),
            'create_time': int(time.time())
        }

        db = Dbmanager.Dbmanager()
        db.addArticle(intoMysqlParams)




