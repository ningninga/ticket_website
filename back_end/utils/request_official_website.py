import json
import logging
import requests
import smtplib
from email.message import EmailMessage
# 负责构造文本
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pyquery import PyQuery as pq
import xlsxwriter
from datetime import datetime
import os


index_url = 'https://www.cmskchp.com/sailingsJson'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'www.cmskchp.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'Acess-Control-Allow-Origin': '*'
}


def get_data(ticket_info):
    flightDate = ticket_info.get('flightDate', '')
    departureDate = ticket_info.get('departureDate', '')
    arrivalPort = ticket_info.get('arrivalPort', '')
    airlines = ticket_info.get('airlines', '')
    flightNumber = ticket_info.get('flightNumber', '')
    flight_hour = ticket_info.get('flight_hour', '')
    flight_minute = ticket_info.get('flight_minute', '')
    todate2 = departureDate[5:7] + '月'+departureDate[8:] + '日'
    data = {'siteResJson': """{"userType":"LTP001","startSite":"SK","endSite":"%s","toDate":"%s","toDate2":"%s","toWeek":"","backDate":"","backDate2":"","backWeek":"","endSiteName":"","startSiteName":"","sailingType":"0","lineId":"SK-%s","airportTime":null,"lineType":null,"toTime":null,"flightCode":"%s","flightName":"","flightNo":"%s","flightId":"58","flightDate":"%s","flightHours":"%s","flightMinute":"%s","destPlaceId": "", 
"flightUser": null,"chanId":"1","isSeckill":false,"isSeckills":false,"nightFlight":0,"batchNo":null,"hsyLineId":null,"memberId":null}"""
            % (arrivalPort, flightDate, todate2, arrivalPort, airlines, flightNumber, departureDate, flight_hour, flight_minute)}
    return data


def get_ticket_info(ticket_info, is_send_email=True):
    """
    :param ticket_info:
    :param is_send_email: 当查无余票时，默认会发邮件（适用于web页面）；值为False时，为了后续定期监控余票所用
    :return:
    """
    departureDate = ticket_info.get('departureDate', '')
    flightDate = ticket_info.get('flightDate', '')
    email = ticket_info.get('email', '')
    print(111111111111)
    print(email)
    arrivalPort = ticket_info.get('arrivalPort', '')
    for _ in range(3):
        try:
            with requests.Session() as req:
                html = req.post(index_url, headers=headers,
                                data=get_data(ticket_info), timeout=10)

            json_obj = html.json()
            totalRemianTicket = 0
            last_totalRemianTicket = 0  # 最后一班船的余票数量
            ticket_str = ''
            last_ticket_str = ''  # 只有最后一班船票的信息
            if 'status' in json_obj and json_obj['status']:
                message = json_obj['message']
                # 获取附件所需的数据
                data_list = []
                last_data_list = []  # 只有最后一班船票的信息
                for i in range(len(message)):
                    # 只要hasRisk=0的数据，hasRisk=1代表有风险，官网不允许购买
                    hasRisk = int(message[i]['hasRisk'])
                    if hasRisk == 1:
                        continue
                    totalRemianTicket += int(message[i]['totalRemainVolume'])
                    print(totalRemianTicket)
                    putong_price = int(
                        message[i]['seatList'][0]['priceList'][0]['price'])
                    toudeng_price = int(
                        message[i]['seatList'][1]['priceList'][0]['price'])
                    if len(message[i]['seatList']) >= 3:
                        tedeng_price = int(
                            message[i]['seatList'][2]['priceList'][0]['price'])
                    else:
                        tedeng_price = 0
                    go_time = message[i]['goTime']
                    totalRemainVolume = message[i]['totalRemainVolume']
                    putong_num = message[i]['seatList'][0]['num']
                    toudeng_num = message[i]['seatList'][1]['num']
                    if len(message[i]['seatList']) >= 3:
                        tedeng_num = message[i]['seatList'][2]['num']
                    else:
                        tedeng_num = 0
                    ticket_tmp = f"开船时间：{go_time}，共有座位{totalRemainVolume}个。" \
                        f"其中普通座位{putong_num}个，票价{putong_price}元；" \
                        f"头等座位{toudeng_num}个，票价{toudeng_price}元，" \
                        f"特等座位{tedeng_num}个，票价{tedeng_price}元\n"
                    ticket_str += ticket_tmp
                    #  data_list为hasRisk=0的所有班次的船票信息
                    data_list.append([go_time, totalRemainVolume, putong_num, putong_price, toudeng_num, toudeng_price,
                                      tedeng_num, tedeng_price])
                    #  last_data_list为最后一班的船票信息
                    if i == len(message) - 1:
                        last_ticket_str = ticket_tmp
                        last_data_list.append([go_time, totalRemainVolume, putong_num, putong_price, toudeng_num, toudeng_price,
                                               tedeng_num, tedeng_price])
                        last_totalRemianTicket = int(totalRemainVolume)
                # 全天的班次都无余票
                if totalRemianTicket == 0:
                    if is_send_email:  # is_send_email=True, web端点击submit，发送邮件
                        message_subject = '蛇口到{},适用所选{}的船票信息'.format(
                            arrivalPort, departureDate)
                        send_message_ticket_info = '\n共有座位{}个,请持续关注\n'.format(
                            totalRemianTicket)
                        send_email(email, message_subject,
                                   send_message_ticket_info, is_show_atta=False)
                    return True, 0
                else:
                    message_subject = '【日常播报】蛇口到{},适用所选{}的船票信息'.format(
                        arrivalPort, departureDate)

                    # 当用户选择的depart time和flight time不一致时（通常为航班时间为凌晨或早上，须购买上一天班次最晚的船票）
                    if departureDate != flightDate and departureDate and flightDate:
                        totalRemianTicket = last_totalRemianTicket
                        send_message_ticket_info = '适配机票的{}船票时间:{} \n共有座位{}个\n'.format(
                            flightDate, last_data_list[0][0], totalRemianTicket)
                        if last_totalRemianTicket == 0:
                            if is_send_email:
                                send_email(
                                    email, message_subject, send_message_ticket_info, is_show_atta=False)
                            return True, 0
                        send_message_ticket_info += last_ticket_str
                        create_excel(totalRemianTicket, last_data_list)
                    #  departTime = flightTime（大多数人的选择）
                    else:
                        send_message_ticket_info = '\n共有座位{}个\n'.format(
                            totalRemianTicket) + ticket_str
                        create_excel(totalRemianTicket, data_list)
                    send_email(email, message_subject,
                               send_message_ticket_info)

                    return True, 1
                # robot_msg = message_subject
                # robot_message(robot_msg + send_message_ticket_info)
                # return True
        except Exception as e:
            logging.error('访问网站异常: {}'.format(e))
    return False, 0


def send_email(mail_receiver, subject_content, body_content, is_show_atta=True):
    """
    :param mail_receivers: 邮箱地址列表 ["123", "456"]
    :param subject_content: 邮件标题
    :param body_content: 邮件内容
    :param is_show_atta: 默认显示附件
    :return:
    """
    try:

        sender = "jjianing@outlook.com"
        message = body_content

        email = EmailMessage()
        email["From"] = sender
        email["To"] = mail_receiver
        email["Subject"] = subject_content
        email.set_content(message)
        if is_show_atta:
            with open('ticket.xlsx', 'rb') as content_file:
                content = content_file.read()
                email.add_attachment(content, maintype='application', subtype='xlsx', filename='ticket.xlsx')

        smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        smtp.starttls()
        smtp.set_debuglevel(1)
        smtp.login(sender, "Vvning0219!!!")
        try:
            smtp.sendmail(sender, mail_receiver, email.as_string())
            print('SUCCESS!')
        except Exception as e:
            print(e)
        smtp.quit()

    except Exception as e:
        return False


def create_excel(totalTicket, data_list):
    """
    创建船票信息excel
    :param totalTicket:
    :param data_list:
    :return:
    """
    workbook = xlsxwriter.Workbook('ticket.xlsx')
    worksheet = workbook.add_worksheet('ticket_info')
    merge_format = workbook.add_format({
        'bold':     True,
        'border':   6,
        'align':    'center',  # 水平居中
        'valign':   'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
    })
    merge_format_title = workbook.add_format({
        'bold':     True,
        'align':    'center',  # 水平居中
        'valign':   'vcenter',  # 垂直居中
        'fg_color': '#85888b',  # 颜色填充
    })
    merge_format_cell = workbook.add_format({
        'align':    'center',  # 水平居中
        'valign':   'vcenter',  # 垂直居中
    })
    worksheet.merge_range(
        'A1:H1', '船票信息如下,共有{}个座位'.format(totalTicket), merge_format)
    title = ['Time', 'ticket number', 'general ticket', 'price',
             'vip ticket', 'price', 'vvip ticket', 'price']  # 设置表头
    worksheet.write_row(
        'A2', title, cell_format=merge_format_title)  # 从A1单元格开始写入表头

    start_number = 3
    for index, data in enumerate(data_list):
        worksheet.write_row('A{}'.format(start_number + index),
                            data, cell_format=merge_format_cell)
    workbook.close()
