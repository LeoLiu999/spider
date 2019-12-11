# -*- coding: utf-8 -*-

import redis
import urllib3
from bloom_filter import BloomFilter
from lxml import etree
import Constant
import threading
import hashlib
import json
import time
from Factory import Factory

class Crawl:

    def __init__(self):

        self.originUrl = Constant.ORIGIN_URL

        self.bloomFilterUrlQueue = BloomFilter(1024*1024*16, 0.01)

        self.maxDepth = Constant.MAX_DEPTH

        redisPool = redis.ConnectionPool(host=Constant.REDIS_HOST, port=Constant.REDIS_PORT)

        self.redis = redis.Redis(connection_pool=redisPool)

        self.currentQueue = 'spider_current_queue'

        self.maxThreads = Constant.MAX_THREADS

        self.threadDelay = Constant.THREAD_DELAY

        self.requestHeader = {
            'host': Constant.HEADER_HOST,
            'connection': "keep-alive",
            'cache-control': "no-cache",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6"
        }

        self.threads = []

        self.siteName = Constant.SITE_NAME


    def enQueue(self, url, depth):
        if( hashlib.md5(url.encode('utf-8')).hexdigest() not in self.bloomFilterUrlQueue and  depth < self.maxDepth ):
            self.bloomFilterUrlQueue.add(hashlib.md5(url.encode('utf-8')).hexdigest())
            self.redis.lpush( self.currentQueue, json.dumps({'url':url, 'depth': depth}) )
            print('depth:', depth, '当前入队url:', url)

    def deQueue(self):
        try:
            val = self.redis.rpop(self.currentQueue)
            return json.loads(val)
        except:
            print('queue is none')
            return None

    def initQueue(self):
        self.enQueue(self.originUrl, 0)


    def parseHref(self, pageContent, depth):
        if pageContent is not None:

            html=etree.HTML(pageContent)
            hrefs = html.xpath(u"//a[@href]")

            for href in hrefs:

                link = href.attrib['href']

                if link.find("javascript:") != -1:
                    continue
                elif link.startswith('/') is True:
                    link = self.originUrl + link
                elif link.startswith(self.originUrl) is False:
                    continue

                self.enQueue(link, depth + 1)

    def parseContent(self, pageContent, currentUrl):
        if pageContent is not None:
            params = {'content':pageContent, 'url' :currentUrl}
            factory = Factory()
            return factory.parseContent(self.siteName, params)



    def crawlPage(self, currentUrl, depth):
        print('当前抓取url', currentUrl, ', 当前depth', depth)
        try:

            content = self.getContent(currentUrl, depth)

            self.parseHref(content, depth)

            self.parseContent(content, currentUrl)

        except Exception as err:
            print(err)
            return None


    def getContent(self, currentUrl, depth):

        try:

            http = urllib3.PoolManager()

            r = http.request('get', currentUrl, headers=self.requestHeader)

            content = r.data

            return content.lower().decode('utf-8')

        except IOError as err:
            raise err

        except Exception as err:
            raise err


    def startCrawl(self):
        while True:
            linkInfo = self.deQueue()

            if linkInfo is None:
                print('empty queue')
                #等待线程池里的线程结束
                for th in self.threads:
                    th.join()

                time.sleep(self.threadDelay)
                continue

            while True:

                for th in self.threads:
                    if not th.is_alive():
                        self.threads.remove(th)

                if len(self.threads) >= self.maxThreads:
                    time.sleep(self.threadDelay)
                    continue

                try:

                    thread = threading.Thread(target=self.crawlPage, name=None, args=(linkInfo['url'], linkInfo['depth']))
                    self.threads.append(thread)

                    thread.setDaemon(True)
                    thread.start()
                    time.sleep(self.threadDelay)
                    break
                except Exception as err:
                    print('ERROR:unable to start thread', err)
                    raise




if __name__ == '__main__':

    spider = Crawl()

    spider.initQueue()

    spider.startCrawl()








