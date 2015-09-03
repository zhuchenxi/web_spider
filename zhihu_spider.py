# coding=utf-8
'''

@author: zhu
'''

import urllib2
import urllib
import re
import codecs
import threading
import Queue
import os
import time

# class DownLoadImgThread(threading.Thread):
#     def __init__(self, real_url, i, path_name):
#         self.real_url = real_url
#         self.i = i
#         self.path_name = path_name
#     
#     def run(self):
#         print "it is started"
#         data = urllib.urlopen(self.real_url).read()
#         img_name = "img" + str(self.i) + ".jpg"
#         file_name = self.path_name + img_name
#         f = open(file_name, "wb")
#         f.write(data)
#         f.close()

def download_img(real_url, i, path_name):
    mytime = 0
    while True:
        time.sleep(5)
        try:
            request = urllib.urlopen(real_url)
            data = request.read()
            request.close()
            break
        except:
            print "it should sleep." + str(mytime)
            mytime += 1
                                    
    img_name = "img" + str(i) + ".jpg"
    file_name = path_name + img_name
    f = open(file_name, "wb")
    f.write(data)
    f.close()

def store_data(number, img_list):
    path_name = "d:/ziyuan/" + number + "/"
    os.makedirs(path_name) 
    thread_list = []
    for i, img_url in enumerate(img_list):
        real_url = "http:" + img_url
        print "img_url: %s" %real_url
        t = threading.Thread(target=download_img, args=(real_url, i, path_name))
        #t = DownLoadImgThread(real_url, i, path_name)
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join(60)
        
            
def check_question(number):
    path = "d:/ziyuan/" + number + "/"
    if os.path.exists(path):
        return False
    else:        
        return True

def parse_question(number):
    if not check_question(number):
        return
    url = "http://www.zhihu.com/question/" + number
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    page = response.read().decode('utf-8')
    #f = codecs.open("aaa", "w", "utf-8")
    #f.write(page)
    #sf.close()
    title_pattern = re.compile(r'<h2 class="zm-item-title zm-editable-content">(.*?)</h2>', re.S)
    m = re.search(title_pattern, page)
    title = m.groups()[0].strip()
    print title
    answer_pattern = re.compile(r'<div class="fixed-summary zm-editable-content clearfix">(.*?)</div>', re.S)
    answer_list = re.findall(answer_pattern, page)
    img_pattern = re.compile(r'actualsrc="(.*?\.(jpg|png))"', re.S)
    img_list = []
    for answer in answer_list:
        answer = answer.strip()
        m = re.findall(img_pattern, answer)
        if m:
            img_list.extend([seq[0] for seq in m])
    store_data(number, img_list)
    
def parse_collection(number):
    #url = "http://www.zhihu.com/collection/61633672"
    url = "http://www.zhihu.com/collection/" + number
    index = 1
    while 1:
        url_newpage = url + "?page=" + str(index)
        request = urllib2.Request(url_newpage)
        response = urllib2.urlopen(request)
        page = response.read().decode('utf-8')
        #print page
        #<div class="zu-list-empyt-place-holder zg-r5px">.*?
        stop_pattern = re.compile(u'该收藏夹还没有任何内容', re.S)
        m = re.search(stop_pattern, page)
        if m:
            print "stop"
            break
        else:
            question_pattern = re.compile(r'href="/question/(\d+?)"', re.S)
            question_list = re.findall(question_pattern, page)
            for question in question_list:
                print "question: %s" %question
                parse_question(question)
            index += 1
            
    
# class SpiderThread(threading.Thread):
#     def __init__(self):
#         pass
#     
#     def run(self):
#         pass
#     
# class StaticVar:
#     href_queue = Queue.Queue()
#     queue_lock = threading.Lock()
    

if __name__ == '__main__':
    parse_collection("38624707")
    #zhihu_test()