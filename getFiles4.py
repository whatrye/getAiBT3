#! python3
# -*- coding: UTF-8 -*-
#coding: UTF-8
#获取torrent及相关图片
#使用ThreadPoolExecutor替代threading，以简化代码

#from bs4 import BeautifulSoup
import os,requests
#import queue,threading
from concurrent.futures import ThreadPoolExecutor

#filesQueue = queue.Queue()
##lock = threading.Lock()
##lock.acquire()
##lock.release()

def getFile(ft, m = 'g', enable_proxy = False, tcode = 'vic8w2AM', proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "下载单独文件"
    #ft: {'link':fullurl,'ofile':outPutfilename,'oDir':outdir}
    #m:请求方式 "g"et 或者 "p"ost
    
    proxies = {}
    timeout = 15
    picFilename = ''
    picFilename = ft['ofile']
    fileLink = ft['link']
    #print(m)

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

    outdir1 = ft['oDir']
    os.makedirs(outdir1, exist_ok=True)
    picFullpath = str(outdir1 + r'/' + picFilename)
    print(picFullpath)

    try:
        save = 0
        if m == 'p':
            tcode = fileLink
            formdata={'code':tcode}
            #print('start get torrent',tcode)
            try:
                r1 = requests.post('http://www.jandown.com/fetch.php',data = formdata, headers = headers)
            except Exception as e:
                print('error:',e)
                return 2
            if b'<html>' in r1.content:
                #r1.content = b''
                save = 0
                #print('not torrent')
            else:
                save = 1
                #print('good')
        elif m == 'g':
            #print('start get img ',picFilename)
            try:
                fileLinkHttps = fileLink.replace('http://','https://')
                r1 = requests.get(fileLinkHttps, headers = headers,proxies = proxies,timeout = timeout)
            except Exception as e:
                print('error:',e)
                return 3
            save = 1
            
        imgContent = r1.content
        if len(imgContent) > 0 and save == 1:
            if os.path.exists(picFullpath) and os.path.isfile(picFullpath) and os.access(picFullpath,os.R_OK):
                print('file exist, skip')
            else:
                ofile = open(picFullpath,'wb')
                ofile.write(imgContent)
                ofile.close()
    except Exception as e:
        print('error:',e)
        return 4
    return 1

def getFiles(fileList,m):
    #fileList:[{'link':fullurl,'ofile':outPutfilename,'oDir':outdir},]
    #m:请求方式 "g"et 或者 "p"ost
    with ThreadPoolExecutor(max_workers=50) as pool:
        [pool.submit(getFile,item,m) for item in fileList]

if __name__ == '__main__':
    outfilename,imgContent = getFile()
    outfile = open(outfilename,'wb')
    outfile.write(imgContent)
    outfile.close()
    print(outfilename,' be saved')
