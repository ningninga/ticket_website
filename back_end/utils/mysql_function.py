import logging
import pymysql
import re
from six import itervalues


logging.basicConfig(
    format='%(asctime)s -[PID:%(process)s]-%(levelname)s-%(module)s-%(funcName)s-%(lineno)d: [ %(message)s ]',
    level=logging.INFO,
    filemode='a',
    datefmt='%Y-%m-%d %H:%M:%S')

db = pymysql.connect(host='localhost',
                     user='root',
                     password='Vvning0219!',
                     database='ticket')

def insert_record(table_name = None, values = {}):
    if table_name and values:
        cur = db.cursor()
        try:
            for key in list(values.keys()):
                value = values[key]
                if isinstance(value, str):
                    value = value.strip()
            _keys = ",".join('{}'.format(k) for k in values)
            _values = ",".join(['%s', ] * len(values))
            sql_insert = "INSERT INTO %s (%s) values (%s)" % ( table_name, _keys, _values)
            logging.info('mysql-[{}]，insert，influence：{}'.format(table_name, cur.execute(sql_insert, list(itervalues(values)))))
            db.commit()
            return True
        except Exception as e:
            logging.error('Error: {}'.format(e))
            return False
        finally:
            cur.close()
            db.close()
    else:
        return False
    