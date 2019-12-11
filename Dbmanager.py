# -*- coding: utf-8 -*-

import mysql.connector
import Constant
from DownloadImage import DownloadImage

class Dbmanager:

    def __init__(self):

        self.dbconfig = {
            'host' : Constant.MYSQL_HOST,
            'user' : Constant.MYSQL_USER,
            'password' : Constant.MYSQL_PASSWORD,
            'database' : Constant.MYSQL_DB
        }
        self.maxThreadNum = Constant.MAX_THREADS
        try:

            self.connector = mysql.connector.connect(pool_name='mypool', pool_size=self.maxThreadNum, **self.dbconfig)
            self.cursor = self.connector.cursor()
        except mysql.connector.Error as err:
            print(err)
            exit(1)



    def addBook(self, params):

        try:

            sql = "SELECT * FROM book WHERE relation_flag = %s LIMIT 1"
            vals = (params['relation_flag'], )
            self.cursor.execute(sql, vals)

            one  = self.cursor.fetchone()

            if one is not None:
                return

            do = DownloadImage()
            cover = do.download(params['cover'])

            if cover is None:
                cover = params['cover']

            sql ="INSERT INTO book(`name`,`relation_flag`,`origin_site`,`author`,`category`,`words`,`state`,`description`,`cover`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (params['name'], params['relation_flag'], params['origin_site'],params['author'], params['category'], params['words'], params['state'], params['description'], cover)

            self.cursor.execute(sql, values)
            self.connector.commit()

        except mysql.connector.Error as err:
            print('dbmanager:mysqlerror:',err)
            exit(1)
        except Exception as err:
            print('dbmanager:error:',err)
            exit(1)
        finally:
            self.cursor.close()
            self.connector.close()



    def addArticle(self, params):

        try:

            sql = "SELECT * FROM article WHERE relation_flag = %s LIMIT 1"
            vals = (params['relation_flag'], )
            self.cursor.execute(sql, vals)

            one  = self.cursor.fetchone()

            if one is not None:
                return

            sql ="INSERT INTO article(`relation_flag`,`parent_flag`,`origin_site`,`title`,`content`,`sort_weight`,`create_time`) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            values = (
                        params['relation_flag'], params['parent_flag'], params['origin_site'],
                        params['title'], params['content'], params['sort_weight'],
                        params['create_time']
                      )

            self.cursor.execute(sql, values)
            self.connector.commit()

        except mysql.connector.Error as err:
            print(err)
            exit(1)
        except Exception as err:
            print('error:',err)
            exit(1)
        finally:
            self.cursor.close()
            self.connector.close()

if __name__ == '__main__':
    db = Dbmanager()

    params = {'name': '明朝败家子', 'relation_flag': '83138', 'origin_site': 'shuquge', 'author': '上山打老虎额', 'category': '历史军事',
     'words': '6815203', 'state': 'writing',
     'description': '\n         弘治十一年。这是一个美好的清晨。此时朱厚照初成年。此时王守仁和唐伯虎磨刀霍霍，预备科举。r/>    此时小冰河期已经来临，绵长的严寒肆虐着大地。此时在南和伯府里，地主家的傻儿子，南和伯的嫡传继承人方继藩……开始了他没羞没躁的败家人生。',
     'cover': 'http://www.shuquge.com/files/article/image/83/83138/83138s.jpg'}
    db.addBook(params)