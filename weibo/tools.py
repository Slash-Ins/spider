import datetime
from datetime import datetime, timedelta, timezone
import xlrd
import xlwt
from xlutils.copy import copy
from pymongo import MongoClient
# import configparser
# import os



def get_time_today_string():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    # print(utc_dt)
    # astimezone()将转换时区为北京时间:
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    bj_dt_string = bj_dt.strftime('%Y-%m-%d')
    return bj_dt_string

def get_time_yesterday_string():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    # print(utc_dt)
    # astimezone()将转换时区为北京时间:
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    bj_dt_y = bj_dt + timedelta(-1)
    bj_dt_y_string = bj_dt_y.strftime('%Y-%m-%d')
    # print(bj_dt_y)
    return bj_dt_y_string


# file = 'test.xlsx'
# print(search_excel_row_col(file, 'abc'))
def init_excel_by_input_date(file):


    for i in range(0,3):
        rb = xlrd.open_workbook(file)
        wb = copy(rb)
        ws = wb.get_sheet(i)

        ws.write(0, 0, 'id')
        ws.write(0, 1, 'date')
        ws.write(0, 2, 'type')
        ws.write(0,3,'comment_counts')
        # ws.write(0,4,'text')

        # date_list = get_date_between_days(start_date_string, end_date_string)
        # print(date_list)
        # date_list.append('count')
        #
        # for i in range(len(date_list)):
        #     # ws = wb.get_sheet(0)
        #     ws.write(0, i + 2, date_list[i])
        wb.save(file)
    print('init excel success...')





def create_excel_by_automation():
    # 创建工作簿
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建工作表
    wbk.add_sheet('kp', cell_overwrite_ok=True)
    wbk.add_sheet('hot', cell_overwrite_ok=True)
    wbk.add_sheet('summary', cell_overwrite_ok=True)
    wbk.add_sheet('others', cell_overwrite_ok=True)
    excel = r"kp_comments_type_counts_automation.xls"
    # excel = r"qun_comments_data_new.xlsx"
    wbk.save(excel)
    print('create the excel and add sheets...')
    return excel



# cf = configparser.ConfigParser()
# cf.read('configure.conf')
def get_db():
    # path = os.path.abspath(os.curdir)
    # cf = configparser.ConfigParser()
    # print(path + '/configure.conf')
    # cf.read(path + '/configure.conf')
    # host = cf.get('db', 'HOST')
    # port = int(cf.get('db', 'PORT'))
    host = '35.221.155.198'
    port = 27017
    conn = MongoClient(host, port)
    # connect db
    db = conn.QunWeibo
    return db, conn


def get_kp_comments(new_db):
    # conn = get_db()
    db = new_db[0]
    # my_collection = db['kp_weibo']
    my_collection = db['kp_weibo']
    kp_list = []
    hot_list = []
    summary_list = []
    others_list = []
    kp_cursor = my_collection.find({'type':'kp'},{'_id': 0}).sort('id', -1)
    hot_cursor = my_collection.find({'type':'hot'},{'_id': 0}).sort('id', -1)
    summary_cursor = my_collection.find({'type':'summary'},{'_id': 0}).sort('id', -1)
    others_cursor = my_collection.find({'type':'others'},{'_id': 0}).sort('id', -1)
    for temp in kp_cursor:
        kp_list.append(temp)
    for temp in hot_cursor:
        hot_list.append(temp)
    for temp in summary_cursor:
        summary_list.append(temp)
    for temp in others_cursor:
        others_list.append(temp)
    return kp_list, hot_list, summary_list, others_list


def close_db(conn):
    conn.close()

def kp_write_to_excel(file, sheet_index, data_list):
    rb = xlrd.open_workbook(file)
    wb = copy(rb)
    # sheet_index = 0
    ws = wb.get_sheet(sheet_index)
    max_row = len(data_list)
    for i in range(max_row):
        ws.write(i + 1, 0, str(data_list[i]['id']))
        ws.write(i + 1, 1, data_list[i]['format_create_time'])
        ws.write(i + 1, 2, data_list[i]['type'])
        ws.write(i + 1, 3, data_list[i]['comments_count'])
        # ws.write(i+1, 4, data_list[i]['text'])
        wb.save(file)


# write to excel
new_db = get_db()
data_tuple = get_kp_comments(new_db)
kp_list = data_tuple[0]
hot_list = data_tuple[1]
summary_list = data_tuple[2]
others_list = data_tuple[3]
close_db(new_db[1])

file = create_excel_by_automation()
init_excel_by_input_date(file)


kp_write_to_excel(file, 0, kp_list)
kp_write_to_excel(file, 1, hot_list)
kp_write_to_excel(file, 2, summary_list)
kp_write_to_excel(file, 3, others_list)
