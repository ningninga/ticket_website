import requests
import json
import re
from pyquery import PyQuery as pq
from pymongo import MongoClient

url = "https://www.hackerrank.com/dashboard"
client = MongoClient('mongodb+srv://jenniejing:99V15wIaMVxFunYL@cluster0.cghskf9.mongodb.net/?retryWrites=true&w=majority')

db = client['hackerRank']  # Create a new database called 'mydatabase'
hackerRank_info_collection = db['hackerRank'] 

cookies = {
    'referrer': 'https://www.google.com/',
    '_fcdscst': 'MTY4Mzk3NTY0NDkwNw==',
    'homepage_variant': 'https://www.hackerrank.com/',
    '_gcl_au': '1.1.215987108.1683975645',
    '_gid': 'GA1.2.1021538427.1683975646',
    '_fcdscv': 'eyJDdXN0b21lcklkIjoiOWUyMDZiMGQtMDAxNC00MmI5LThkMzktYzJiOTA5NGEyNzMxIiwiVmlzaXRvciI6eyJFbWFpbCI6bnVsbCwiRXh0ZXJuYWxWaXNpdG9ySWQiOiIxNDNiZGM4MS1hODYzLTQ0ZGQtYTMyYi05N2IxZmEzZWYyOTUifSwiVmlzaXRzIjpbXSwiQWN0aXZpdGllcyI6W10sIkRpYWdub3N0aWNNZXNzYWdlIjpudWxsfQ==',
    'cebs': '1',
    '_ce.s': 'v~7869413a957caf897409bfa682ea0800a5e55383~lcw~1683975645715~vpv~0~lcw~1683975645716',
    '_gd_visitor': 'cae95fa5-2e83-4be8-8cdc-1bccb2bc76e4',
    '_gd_session': '0df27170-584c-4cd3-8ca6-8affaf33c15a',
    '_wchtbl_uid': '4b8e02fa-68f9-49d6-b262-1cfdf82d07ea',
    '_wchtbl_sid': '73e7278e-9094-4d17-a0e5-afee03117824',
    '_ce.clock_event': '1',
    '_gd_svisitor': 'ce8f655f574f0000e9303063ef020000f16d6800',
    'ln_or': 'eyI0Nzc3MCI6ImQifQ%3D%3D',
    '_hp2_ses_props.547804831': '%7B%22r%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22ts%22%3A1683975645549%2C%22d%22%3A%22www.hackerrank.com%22%2C%22h%22%3A%22%2F%22%7D',
    '_ce.clock_data': '-72%2C109.255.1.196%2C1',
    'mp_bcb75af88bccc92724ac5fd79271e1ff_mixpanel': '%7B%22distinct_id%22%3A%20%222eee00a2-1bc2-4cc9-be5f-1eb57cbac940%22%2C%22%24device_id%22%3A%20%2218814c5289f488-085a1960101825-1d525634-384000-18814c5289f488%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22%24user_id%22%3A%20%222eee00a2-1bc2-4cc9-be5f-1eb57cbac940%22%7D',
    '_uetsid': '6960a630f17d11eda2df0580282a533d',
    '_uetvid': '33d84450b44711edaaac8f01fdd6c381',
    '_mkto_trk': 'id:487-WAY-049&token:_mch-hackerrank.com-1683975658122-76657',
    'cebsp_': '2',
    '_ga': 'GA1.2.791546146.1683975646',
    '_ga_BCP376TP8D': 'GS1.1.1683975645.1.1.1683975663.0.0.0',
    '_ga_X2HP4BPSD7': 'GS1.1.1683975645.1.1.1683975663.0.0.0',
    '_ga_0QME21KCCM': 'GS1.1.1683975645.1.1.1683975663.0.0.0',
    '_ga_4G810X81GK': 'GS1.1.1683975645.1.1.1683975663.0.0.0',
    '_ga_R0S46VQSNQ': 'GS1.1.1683975645.1.1.1683975663.0.0.0',
    '_ga_ZDWKWB1ZWT': 'GS1.1.1683975645.1.1.1683975663.0.0.0',
    'user_type': 'hacker',
    '_pk_id.5.fe0a': '8d15f69c92594735.1683975664.',
    '_pk_ses.5.fe0a': '1',
    'remember_hacker_token': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaGJDRnNHYVFRaDNrRUJJaUlrTW1Fa01UQWtXRWhsVldGdlNUaE1ZbXhpUTJGNGQxazRjVnBDWlVraUZqRTJPRE01TnpVMk9ESXVNemd4TURVNUJqb0dSVVk9IiwiZXhwIjoiMjAyMy0wNS0yN1QxMTowMToyMi4zODFaIiwicHVyIjpudWxsfX0%3D--12b93880b68616f743b52fffd4ab7adb68849d99',
    'hrc_l_i': 'T',
    'metrics_user_identifier': '141de21-774ca942a85398e572c71d3d823e6ccc8b59f2a4',
    '_hrank_session': '781f542b77b69d1a66aaf7de97e8d008',
    'hackerrank_mixpanel_token': 'c739ac9b-54c8-43eb-a7e3-468098f6aa10',
    'react_var': 'false__cnt4',
    'react_var2': 'false__cnt4',
    '_hjFirstSeen': '1',
    '_hjIncludedInSessionSample_2036154': '0',
    '_hjSession_2036154': 'eyJpZCI6ImE5ZGIxNTliLWMyODItNDczYS04NzZiLTM4NjVlMjM1ZDFiNSIsImNyZWF0ZWQiOjE2ODM5NzU2ODY4MTIsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjAbsoluteSessionInProgress': '0',
    'fileDownload': 'true',
    '_hjSessionUser_2036154': 'eyJpZCI6ImE2YWNkODhmLTc5M2MtNTgxNS05OTM3LWM2OWM1ZmZkNWU3ZiIsImNyZWF0ZWQiOjE2ODM5NzU2ODY4MDIsImV4aXN0aW5nIjp0cnVlfQ==',
    '_hp2_id.547804831': '%7B%22userId%22%3A%228202564019542608%22%2C%22pageviewId%22%3A%221122155340450663%22%2C%22sessionId%22%3A%228731422929865247%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D',
}

headers = {
    'authority': 'www.hackerrank.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookie': 'referrer=https://www.google.com/; _fcdscst=MTY4Mzk3NTY0NDkwNw==; homepage_variant=https://www.hackerrank.com/; _gcl_au=1.1.215987108.1683975645; _gid=GA1.2.1021538427.1683975646; _fcdscv=eyJDdXN0b21lcklkIjoiOWUyMDZiMGQtMDAxNC00MmI5LThkMzktYzJiOTA5NGEyNzMxIiwiVmlzaXRvciI6eyJFbWFpbCI6bnVsbCwiRXh0ZXJuYWxWaXNpdG9ySWQiOiIxNDNiZGM4MS1hODYzLTQ0ZGQtYTMyYi05N2IxZmEzZWYyOTUifSwiVmlzaXRzIjpbXSwiQWN0aXZpdGllcyI6W10sIkRpYWdub3N0aWNNZXNzYWdlIjpudWxsfQ==; cebs=1; _ce.s=v~7869413a957caf897409bfa682ea0800a5e55383~lcw~1683975645715~vpv~0~lcw~1683975645716; _gd_visitor=cae95fa5-2e83-4be8-8cdc-1bccb2bc76e4; _gd_session=0df27170-584c-4cd3-8ca6-8affaf33c15a; _wchtbl_uid=4b8e02fa-68f9-49d6-b262-1cfdf82d07ea; _wchtbl_sid=73e7278e-9094-4d17-a0e5-afee03117824; _ce.clock_event=1; _gd_svisitor=ce8f655f574f0000e9303063ef020000f16d6800; ln_or=eyI0Nzc3MCI6ImQifQ%3D%3D; _hp2_ses_props.547804831=%7B%22r%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22ts%22%3A1683975645549%2C%22d%22%3A%22www.hackerrank.com%22%2C%22h%22%3A%22%2F%22%7D; _ce.clock_data=-72%2C109.255.1.196%2C1; mp_bcb75af88bccc92724ac5fd79271e1ff_mixpanel=%7B%22distinct_id%22%3A%20%222eee00a2-1bc2-4cc9-be5f-1eb57cbac940%22%2C%22%24device_id%22%3A%20%2218814c5289f488-085a1960101825-1d525634-384000-18814c5289f488%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22%24user_id%22%3A%20%222eee00a2-1bc2-4cc9-be5f-1eb57cbac940%22%7D; _uetsid=6960a630f17d11eda2df0580282a533d; _uetvid=33d84450b44711edaaac8f01fdd6c381; _mkto_trk=id:487-WAY-049&token:_mch-hackerrank.com-1683975658122-76657; cebsp_=2; _ga=GA1.2.791546146.1683975646; _ga_BCP376TP8D=GS1.1.1683975645.1.1.1683975663.0.0.0; _ga_X2HP4BPSD7=GS1.1.1683975645.1.1.1683975663.0.0.0; _ga_0QME21KCCM=GS1.1.1683975645.1.1.1683975663.0.0.0; _ga_4G810X81GK=GS1.1.1683975645.1.1.1683975663.0.0.0; _ga_R0S46VQSNQ=GS1.1.1683975645.1.1.1683975663.0.0.0; _ga_ZDWKWB1ZWT=GS1.1.1683975645.1.1.1683975663.0.0.0; user_type=hacker; _pk_id.5.fe0a=8d15f69c92594735.1683975664.; _pk_ses.5.fe0a=1; remember_hacker_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaGJDRnNHYVFRaDNrRUJJaUlrTW1Fa01UQWtXRWhsVldGdlNUaE1ZbXhpUTJGNGQxazRjVnBDWlVraUZqRTJPRE01TnpVMk9ESXVNemd4TURVNUJqb0dSVVk9IiwiZXhwIjoiMjAyMy0wNS0yN1QxMTowMToyMi4zODFaIiwicHVyIjpudWxsfX0%3D--12b93880b68616f743b52fffd4ab7adb68849d99; hrc_l_i=T; metrics_user_identifier=141de21-774ca942a85398e572c71d3d823e6ccc8b59f2a4; _hrank_session=781f542b77b69d1a66aaf7de97e8d008; hackerrank_mixpanel_token=c739ac9b-54c8-43eb-a7e3-468098f6aa10; react_var=false__cnt4; react_var2=false__cnt4; _hjFirstSeen=1; _hjIncludedInSessionSample_2036154=0; _hjSession_2036154=eyJpZCI6ImE5ZGIxNTliLWMyODItNDczYS04NzZiLTM4NjVlMjM1ZDFiNSIsImNyZWF0ZWQiOjE2ODM5NzU2ODY4MTIsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; fileDownload=true; _hjSessionUser_2036154=eyJpZCI6ImE2YWNkODhmLTc5M2MtNTgxNS05OTM3LWM2OWM1ZmZkNWU3ZiIsImNyZWF0ZWQiOjE2ODM5NzU2ODY4MDIsImV4aXN0aW5nIjp0cnVlfQ==; _hp2_id.547804831=%7B%22userId%22%3A%228202564019542608%22%2C%22pageviewId%22%3A%221122155340450663%22%2C%22sessionId%22%3A%228731422929865247%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D',
    'referer': 'https://www.hackerrank.com/auth/login',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

html = requests.get(url=url, cookies=cookies, headers=headers)
html.encoding = 'utf-8'
if html.status_code == 200:
    html_content = pq(html.text)
    # Find the topic names and store it into a list.
    topics = str(html_content(
        'div#content section.dashboard-topics div.topic-name'))
    pattern = r'<div class="topic-name".*?>(.*?)</div>'
    matches = re.findall(pattern, topics)
    topic_name_list = [match.strip() for match in matches]

else:
    print("Error:", html.status_code)

# Processing URLs
for i in range(len(topic_name_list)):
    if topic_name_list[i] == 'C++':
        topic_name_list[i] = 'cpp'
    elif topic_name_list[i] == 'Linux Shell':
        topic_name_list[i] = 'shell'
    elif topic_name_list[i] == 'Functional Programming':
        topic_name_list[i] = 'fp'
    elif topic_name_list[i] == 'Artificial Intelligence':
        topic_name_list[i] = 'ai'
    else:
        topic_name_list[i] = topic_name_list[i].lower().replace(" ", "-")
    topics_url = 'https://www.hackerrank.com/domains/{}'.format(
        topic_name_list[i])
topics = {}
for topic_name in topic_name_list:
    topics[topic_name] = {
        'questions': []
    }
topics['algorithms']['questions'] = ['diagonal-difference']

# get the questions list of each category.
# for topic_name in topics.keys():
#     num = 10
#     while (1):
#         url_algorithms = 'https://www.hackerrank.com/rest/contests/master/tracks/{}/challenges?offset={}&limit=10&track_login=true'.format(
#             topic_name, num)
#         num = num + 10
#         html = requests.get(url=url_algorithms,
#                             cookies=cookies, headers=headers, timeout=10)
#         html.encoding = 'utf-8'

#         if html.status_code == 200:
#             html = html.json()
#             models = html['models']

#             if models and 'models' in html:
#                 for i in range(len(models)):
#                     topics[topic_name]['questions'].append(models[i]['slug'])
#             # print(topics)
#         else:
#             break

hacker_data = {
    "topic_data": []
}
for topic_name in topics.keys():
    print(topic_name)
    # Prepare the structure for the current topic
    topic_data = {
        "topic_name": topic_name,
        "questions": []
    }

    if topic_name not in hacker_data:
        hacker_data['topic_data'].append(topic_data)

    for i in range(len(topics[topic_name]['questions'])):
        question = topics[topic_name]['questions'][i]
        question_data = {
            "question_name": question,
            "languages": {}
        }
        # unclock solutions first:
        unlock_solution_url = 'https://www.hackerrank.com/rest/contests/master/challenges/{}/unlock_solution'.format(
            question)
        unlock_solution_page = requests.get(url=unlock_solution_url, cookies=cookies,
                            headers=headers, timeout=10)

        hacker_url = 'https://www.hackerrank.com/rest/contests/master/challenges/{}/leaderboard?offset=40&limit=40&include_practice=true'.format(
            question)
        html = requests.get(url=hacker_url, cookies=cookies,
                            headers=headers, timeout=10)

        if html.status_code == 200:
            html = html.json()
            models = html['models']
            if models and 'models' in html:
                for model in models:
                    hacker_name = model['hacker']
                    language = model['language']
                    solution_url = 'https://www.hackerrank.com/rest/contests/master/challenges/{}/hackers/{}/download_solution'.format(
                        topics[topic_name]['questions'][i], hacker_name)
                    html = requests.get(url=solution_url,
                                        cookies=cookies, headers=headers, timeout=10)
                    solution = { 
                        'solution_url': solution_url, 
                        'code': html.text
                    }

                    if language not in question_data["languages"]:
                        question_data["languages"][language] = []

                    question_data["languages"][language].append(solution)

        topic_data['questions'].append(question_data)
print(hacker_data)
    
# Insert the topic data into MongoDB
hackerRank_info_collection.insert_one(hacker_data)
