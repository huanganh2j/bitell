# -*- coding: utf-8 -*-
import MySQLdb
class TargetSource(object):
    def __init__(self):
        super(TargetSource, self).__init__()

    @classmethod
    def getTarget(cls):
        conn = MySQLdb.Connect(host='localhost', port=3306, user='root', passwd='923469an', db='reptile_metadata',
                               charset='UTF8');
        target_url=""
        cursor = conn.cursor()
        cursor.execute(" SELECT target_url,user_id from weibo_target_list where is_handle=1 ORDER BY create_time desc limit 1 ")
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