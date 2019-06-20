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


def update_progresss_win(str, svar, root):
    svar.set(str)
    root.update()


y = 0
def DOC(url, svar, root):

    doc_id = get_doc_id(url)
    update_progresss_win('获取页面数据...', svar, root)
    try:
        html = requests.get(url).text
    except Exception as e:
        return False, str(e)
    lists=re.findall('(https.*?0.json.*?)\\\\x22}',html)
    lenth = (len(lists)//2)
    NewLists = lists[:lenth]

    update_progresss_win('分析数据，准备开始下载...', svar, root)

    filename = ''
    for i in range(len(NewLists)):

        base = i*100/len(NewLists)
        percentage = 100/len(NewLists)

        NewLists[i] = NewLists[i].replace('\\','')
        txts=requests.get(NewLists[i]).text
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),',txts)
        for i in range(0,len(txtlists)):

            tip = int(i*percentage/len(txtlists))
            update_progresss_win('已完成 {}%'.format(int(base+tip)), svar, root)

            global y
            # print(txtlists[i][0].encode('utf-8').decode('unicode_escape','ignore'))
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



def PPT(url, svar, root):

    doc_id = get_doc_id(url)
    url = "https://wenku.baidu.com/browse/getbcsurl?doc_id="+doc_id+"&pn=1&rn=99999&type=ppt"
    update_progresss_win('获取页面数据...', svar, root)

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
        update_progresss_win('已完成 {}%'.format(int(i/len(lists))), svar, root)

        img=requests.get(lists[i]).content
        with open(doc_id+'\img'+str(i)+'.jpg','wb') as m:
            m.write(img)
    # print("PPT图片保存在" + doc_id +"文件夹")
    return True, '文档保存在{}'.format(doc_id)


def TXT(url, svar, root):
    doc_id = get_doc_id(url)
    url = "https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id="+doc_id
    update_progresss_win('获取页面数据...', svar, root)

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


def PDF(url, svar, root):
    doc_id = get_doc_id(url)
    url = "https://wenku.baidu.com/browse/getbcsurl?doc_id="+doc_id+"&pn=1&rn=99999&type=ppt"
    update_progresss_win('获取页面数据...', svar, root)

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

        update_progresss_win('已完成 {}%'.format(int(i/len(lists))), svar, root)

        img=requests.get(lists[i]).content
        with open(doc_id+'\img'+str(i)+'.jpg','wb') as m:
            m.write(img)
    # print("FPD图片保存在" + doc_id + "文件夹")
    return True, '文档保存在{}'.format(doc_id)


fetch_dict = {
    'word': DOC,
    'PDF': PDF,
    'PPT': PPT,
    'txt': TXT
}


def fetch(link, doc_type, svar, root):
    try:
        return fetch_dict[doc_type](link, svar, root)
    except Exception as e:
        return False, str(e)
