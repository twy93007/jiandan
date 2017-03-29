# coding:utf-8
import requests
from bs4 import BeautifulSoup
import threading
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

index = 1

def get_url(num):
    pagenum = str(num).encode('utf8')
    baseurl = "http://jandan.net/ooxx/page-"
    url = baseurl + pagenum
    return url

def read_html(url):
    href_lst = []
    response = requests.get(url).text
    soup = BeautifulSoup(response,"html.parser")
    img_lst = soup.find_all(name="a",attrs={
        "target":"_blank",
        "class":"view_img_link"
    })
    for i in img_lst:
        a = "http:"+i.attrs['href']
        a = a.encode('utf8')
        href_lst.append(a)
    print u"Getting Address....."
    return href_lst

def get_img(url):
    global index
    response = requests.get(url)
    img = response.content
    name = url[-9:-4].encode('utf8') + '.jpg'
    if response.status_code == 200:
        tu = open(name,'wb').write(img)
        index += 1
        print name.encode('utf8') + u"完成！"

while True:
    Start_num = raw_input(u"Please input the start page or |exit|:").encode('utf8')
    End_num = raw_input(u"Please input the start page or |exit|:").encode('utf8')
    if Start_num == "exit" or End_num == "exit":
        break
    else:
        for num in xrange(int(Start_num),int(End_num)+1):
            pagenum = get_url(num)
            lst = read_html(pagenum)
            threads = []
            for i in lst:
                t = threading.Thread(target=get_img, args=(i,))
                threads.append(t)
            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                t.join()
            print u"图片下载完成！"
