# -*- coding: utf-8 -*-
import MySQLdb
from scrapy.utils.project import get_project_settings


class TargetSource(object):
    def __init__(self):
        super(TargetSource, self).__init__()

    @classmethod
    def getTarget(cls):
        settings = get_project_settings()
        # conn = MySQLdb.Connect(host='localhost', port=3306, user='root', passwd='923469an', db='reptile_metadata',
        #                        charset='UTF8');
        conn = MySQLdb.Connect(host=settings["MYSQL_HOST"], port=3306, user=settings["MYSQL_USER"], passwd=settings["MYSQL_PASSWORD"], db=settings["MYSQL_DBNAME"],
                               charset='UTF8');
        target_url=""
        cursor = conn.cursor()
        cursor.execute(" SELECT target_url,user_id from weibo_target_list where is_handle=1 ORDER BY create_time limit 1 ")
        data = cursor.fetchone()
        if data is not None and len(data):
            target_url = data[0]
            user_id=data[1]
            # 修改处理状态
            cursor.execute(" update weibo_target_list set is_handle=2,handle_time=now() where user_id="+user_id)
        conn.commit()
        cursor.close()
        conn.close()
        return target_url