#! python3
# -*- coding: UTF-8 -*-
#coding: UTF-8
#获取torrent的相关图片

##from bs4 import BeautifulSoup
import requests,queue,threading

import gettorrentlink4
from getFiles4 import getFiles
from concurrent.futures import ThreadPoolExecutor
linksQueue = queue.Queue()

def getTandI_thread(tp,torrentsPath,save_mode,enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "获取torrent的相关图片"
    #tp: {'title':title,'link':fullLink}
    #torrentsPath: torrent保存根目录
    
    proxies = {}
    timeout = 15
    picFilename = ''

##    while True:
##        try:
##            tp = myQueue.get_nowait()
##            j = myQueue.qsize()
##        except Exception as e:
##            break

    ##    n = 0
    ##    for tp in linksList:
    btsList = []
    imgsList = []
##    n=n+1
    print(tp['link'])
    tResDict = gettorrentlink4.get_torrentlink(myreq_url = str(tp['link']), enable_proxy = enable_proxy, proxy_string = proxy_string)
    n = 0

    #文件保存到各自目录下
    if save_mode == 'd':
        out_dir = str(torrentsPath + r'/' +tResDict['title'])
    elif save_mode == 'f':
        out_dir = torrentsPath

    for imgLink in tResDict['imgsList']:
         #outfilename = imgLink[imgLink.rfind('/')+1:len(imgLink)]
    ##   outfilename = imgLink[imgLink.rfind('/')+1:] #获取原文件名
        #图片文件名替换为title+序号格式，如must1.jpg must2.jpg ...，和torrent文件统一文件名
        n = n+1
        outfilename = tResDict['title']+ '_' + str(n) + imgLink[imgLink.rfind('.'):]
        a = {'link':imgLink,'ofile':outfilename,'oDir':out_dir}
        imgsList.append(a)
    if tResDict['btCode'] != 'notExist':
        b = {'link':tResDict['btCode'],'ofile':str(tResDict['title'])+'.torrent','oDir':out_dir}
        btsList.append(b)

    '''
    #保存所有文件到torrents目录下
    if save_mode == 'f':
        out_dir = torrentsPath
        for imgLink in tResDict['imgsList']:
    ##        outfilename = imgLink[imgLink.rfind('/')+1:]
            #图片文件名替换为title+序号格式，如must1.jpg must2.jpg ...，和torrent文件统一文件名
            n = n+1
            outfilename = tResDict['title']+ '_' + str(n) + imgLink[imgLink.rfind('.'):]
            #change path to 'torrents'
            a = {'link':imgLink,'ofile':outfilename,'oDir':out_dir}
            imgsList.append(a)
        if tResDict['btCode'] != 'notExist':
            b = {'link':tResDict['btCode'],'ofile':str(tResDict['title'])+'.torrent','oDir':out_dir}
            btsList.append(b)
    '''
    
        
    if len(btsList) >0:
        getFiles(fileList = btsList,m = 'p')
    if len(imgsList) >0:
        getFiles(fileList = imgsList,m = 'g')

def getTrAndImgs(linksList,torrentsPath,save_mode):
    #以线程方式获取单网页并获取torrent和img的链接
    #linksList: [{'title':title,'link':fulllink},]
    #torrentsPath: torrent保存根目录
    
##    for tp in linksList:
##        linksQueue.put(tp)
##    threadN = 100
##    jqueue = linksQueue.qsize()
##    print('total ',jqueue,' items')
##    if jqueue < threadN:
##        threadN = jqueue
##
##    if jqueue > 0:
##        threads = []
##        for i in range(0,threadN):
##            thread = threading.Thread(target = getTandI_thread, args = (linksQueue,torrentsPath,))
##            threads.append(thread)
##            thread.start()
##        for thread1 in threads:
##            thread1.join()

    with ThreadPoolExecutor(max_workers = 50) as pool:
        [pool.submit(getTandI_thread,item,torrentsPath,save_mode) for item in linksList]

if __name__ == '__main__':
    outfilename,imgContent = getImg()
    outfile = open(outfilename,'wb')
    outfile.write(imgContent)
    outfile.close()
    print(outfilename,' be saved')
