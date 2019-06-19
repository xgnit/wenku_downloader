import requests
import re
import argparse
import sys
import json
import os


def get_doc_id(url):
    try:
        return re.findall('view/(.*).html', url)[0]
    except Exception:
        raise RuntimeError('无法获取Doc id， url格式错误？')



y = 0
def DOC(url):

    doc_id = get_doc_id(url)
    try:
        html = requests.get(url).text
    except Exception as e:
        return False, str(e)
    lists=re.findall('(https.*?0.json.*?)\\\\x22}',html)
    lenth = (len(lists)//2)
    NewLists = lists[:lenth]
    for i in range(len(NewLists)) :
        NewLists[i] = NewLists[i].replace('\\','')
        txts=requests.get(NewLists[i]).text
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),',txts)
        for i in range(0,len(txtlists)):
            global y
            print(txtlists[i][0].encode('utf-8').decode('unicode_escape','ignore'))
            if y != txtlists[i][1]:
                y = txtlists[i][1]
                n = '\n'
            else:
                n = ''
            filename = doc_id + '.txt'
            with open(filename,'a',encoding='utf-8') as f:
                f.write(n+txtlists[i][0].encode('utf-8').decode('unicode_escape','ignore').replace('\\',''))
        # print("文档保存在"+filename)
        return True, '文档保存在{}'.format(filename)



def PPT(url):

    doc_id = get_doc_id(url)
    url = "https://wenku.baidu.com/browse/getbcsurl?doc_id="+doc_id+"&pn=1&rn=99999&type=ppt"
    try:
        html = requests.get(url).text
    except Exception as e:
        return False, str(e)
    lists=re.findall('{"zoom":"(.*?)","page"',html)
    for i in range(0,len(lists)):
        lists[i] = lists[i].replace("\\",'')
    try:
        os.mkdir(doc_id)
    except:
        pass
    for i in range(0,len(lists)):
        img=requests.get(lists[i]).content
        with open(doc_id+'\img'+str(i)+'.jpg','wb') as m:
            m.write(img)
    # print("PPT图片保存在" + doc_id +"文件夹")
    return True, '文档保存在{}'.format(filename)


def TXT(url):
    doc_id = get_doc_id(url)
    url = "https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id="+doc_id
    try:
        html = requests.get(url).text
    except Exception as e:
        return False, str(e)

    md5 = re.findall('"md5sum":"(.*?)"',html)[0]
    pn = re.findall('"totalPageNum":"(.*?)"',html)[0]
    rsign = re.findall('"rsign":"(.*?)"',html)[0]
    NewUrl = 'https://wkretype.bdimg.com/retype/text/'+doc_id+'?rn='+pn+'&type=txt'+md5+'&rsign='+rsign
    txt = requests.get(NewUrl).text
    jsons = json.loads(txt)
    texts=re.findall("'c': '(.*?)',",str(jsons))
    print(texts)
    filename=doc_id+'.txt'
    with open(filename,'a',encoding='utf-8') as f:
        for i in range(0,len(texts)):
            texts[i] = texts[i].replace('\\r','\r')
            texts[i] = texts[i].replace('\\n','\n')

            f.write(texts[i])
    # print("文档保存在" + filename)
    return True, '文档保存在{}'.format(filename)


def PDF(url):
    doc_id = get_doc_id(url)
    url = "https://wenku.baidu.com/browse/getbcsurl?doc_id="+doc_id+"&pn=1&rn=99999&type=ppt"
    try:
        html = requests.get(url).text
    except Exception as e:
        return False, str(e)

    lists=re.findall('{"zoom":"(.*?)","page"',html)
    for i in range(0,len(lists)):
        lists[i] = lists[i].replace("\\",'')
    try:
        os.mkdir(doc_id)
    except:
        pass
    for i in range(0,len(lists)):
        img=requests.get(lists[i]).content
        with open(doc_id+'\img'+str(i)+'.jpg','wb') as m:
            m.write(img)
    # print("FPD图片保存在" + doc_id + "文件夹")
    return True, '文档保存在{}'.format(filename)


fetch_dict = {
    'word': DOC,
    'PDF': PDF,
    'PPT': PPT,
    'txt': TXT
}


def fetch(link, type):
    try:
        return fetch_dict[type](link)
    except Exception as e:
        return False, str(e)