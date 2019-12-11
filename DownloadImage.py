# -*- coding: utf-8 -*-

import io
import uuid
import os
import requests
from PIL import Image

class DownloadImage:

    def makeFilename(self, imgUrl):
        ext = os.path.splitext(imgUrl)
        uniqueid = uuid.uuid1()

        filename = str(uniqueid) + ext[1]

        path = self.makePath()

        return {'re_filename':path['re_path'] +'/'+filename, 'ab_filename' : path['ab_path'] +'/'+filename}


    def makePath(self):
        path = os.getcwd() + '/cover';

        if not os.path.exists(path):
            os.mkdir(path)

        return {'re_path':path, 'ab_path':'/cover'}


    def download(self, imgUrl):
        try:
            response = requests.get(imgUrl)
            image = Image.open(io.BytesIO(response.content))

            file = self.makeFilename(imgUrl)

            image.save(file['re_filename'])

            return file['ab_filename']
        except Exception as err:
            #这里会出错 图片读取不到的时候 会报错 还有就是报cannot write mode RGBA as JPEG
            print(err)
            return None

if __name__ == '__main__':
    do = DownloadImage()
    url = 'http://www.shuquge.com/files/article/image/83/83129/83129s.jpg'
    do.download(url)
