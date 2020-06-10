#! python3
# -*- coding: UTF-8 -*-

#coding: UTF-8
#获取帖子列表网页中的每个帖子的链接
#v0.5 python2.7 add https://bt.aisex.com
#使用线程池TheadPoolExecutor或进程池ProcessPoolExecutor,方法用map(fn,*iterable)或submit(fn,*arg)

import time,os
from importlib import reload
from colorama import init,Fore,Back,Style #控制台彩色输出用
from bs4 import BeautifulSoup
import bencode  #解码torrent
import io, sys, re
import random

import getpagelink4
#import gettorrentlink3, gettorrent3
from getImg4 import getImg,getImgs
#from getFiles import getFiles
from getFileLinks4 import getTrAndImgs

user_agent = [ 
	"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)", 
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", 
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)", 
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", 
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)", 
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)", 
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)", 
	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)", 
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)", 
	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6", 
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1", 
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0", 
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5", 
	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6", 
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11", 
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20", 
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
] 

HEADER = { 
'User-Agent': random.choice(user_agent),  # ä¯ÀÀÆ÷Í·²¿
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', # ¿Í»§¶ËÄÜ¹»½ÓÊÕµÄÄÚÈÝÀàÐÍ
'Accept-Language': 'en-US,en;q=0.5', # ä¯ÀÀÆ÷¿É½ÓÊÜµÄÓïÑÔ
'Connection': 'keep-alive', # ±íÊ¾ÊÇ·ñÐèÒª³Ö¾ÃÁ¬½Ó
}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

def main():
    start_time = time.time()
    reload(sys)
    #print u'系统默认编码：',sys.getdefaultencoding() #获取系统默认编码
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码

    #sys.setdefaultencoding("utf-8")
    #print u'现在编码：',sys.getdefaultencoding()

    init(autoreset = True)

    #调用时使用gettorrent.get_torrent()
    #或者 from getpagelink import *
    #from gettorrentlink import *
    #from gettorrent import *
    #调用时直接使用 get_torrent

    torrentsPath = 'torrents'
    if not os.path.exists(torrentsPath):
        os.makedirs(torrentsPath)

    enable_proxy = False
    if enable_proxy:
        print('proxy enabled\n\n')
    else:
        print('proxy disabled\n\n')
    '''
    if enable_proxy:
        print Fore.GREEN + 'proxy enabled\n\n'
    else:
        print Fore.GREEN + 'proxy disabled\n\n'
    '''
    proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}
    user_agent = 'Mozilla/5.0'

    if len(sys.argv) > 1:
        firstpage_number = int(sys.argv[1])
        total_pages = int(sys.argv[2])
    else:
        firstpage_number = 1
        total_pages = 1

    page_host = u'bt.aisex.com'
    pagelink_pre = u'https://' + page_host + u'/bt/thread.php?fid=16&page='
##    link_dict = {} #link_dict:  {pagenumber:{fulllink:torrentfilename}}
##    link_count = 0
##    torrentItemList = []
    #获取indexPageC个索引页内的条目链接，返回值里的'title'后期没有使用
    linksList = getpagelink4.getLinksLists(indexPageNS = firstpage_number,indexPageC = total_pages)#返回值[{'title':torrenttitle,'link':btpagefull_link},]
##    link_count = link_count + len(link_dict[mypage_number])
    print('Total links:', len(linksList))
    '''
    print Fore.YELLOW + 'link_dict length is: '+str(len(link_dict)) + '\n'
    print Fore.CYAN + 'Total links: ', link_count, '\n'
    '''

    #以线程方式下载
    getTrAndImgs(linksList,torrentsPath)
    
##      #顺序下载方式-------start-------------
####    btsList = []
####    imgsList = []
##    n = 0
##    for tp in linksList:
##        btsList = []
##        imgsList = []
##        n=n+1
##        print(n,tp['link'])
##        tResDict = gettorrentlink3.get_torrentlink(myreq_url = str(tp['link']), enable_proxy = enable_proxy, proxy_string = proxy_string)
##        for imgLink in tResDict['imgsList']:
##            outfilename =imgLink[imgLink.rfind('/')+1:len(imgLink)]
##            a = {'link':imgLink,'ofile':outfilename,'oDir':str(torrentsPath + r'/' +tResDict['title'])}
##            imgsList.append(a)
##        if tResDict['btCode'] != 'notExist':
##            b = {'link':tResDict['btCode'],'ofile':str(tResDict['title'])+'.torrent','oDir':str(torrentsPath + r'/' +tResDict['title'])}
##            btsList.append(b)
##            
##        if len(imgsList) >0:
##            getFiles(fileList=imgsList,m='g')
##        if len(btsList) >0:
##            getFiles(fileList=btsList,m='p')
##
####    for item in imgsList:
####        print(item)
####    print()
####    for item in btsList:
####        print(item)
####    print()
##
####    if len(imgsList) >0:
####        getFiles(fileList=imgsList,m='g')
####    if len(btsList) >0:
####        getFiles(fileList=btsList,m='p')
##      #顺序下载方式-------End-------------
##
####    n = 0
####    link_nu = 1
####    for btItem in btsList:
####        print('page',link_nu)
####        for link,lTitle in link_dict[link_nu].items():
####            title = ''
####            imglinklist = []
####
####            n = n+1
####            print(Fore.GREEN + Style.BRIGHT + str(n),'page:',str(link))
####            #print(Fore.GREEN + Style.BRIGHT + str(n),'page:',link)
####            #print u'name 的编码形式: ',name.__class__ #获取name的编码形式
####            print(Fore.YELLOW + Style.BRIGHT + '     Title: ' + '\"' + lTitle + '\"')
####
####            '''
####            #去除文件名中的问号
####            symbol_remove = re.compile(r'["?"]')
####            lTitle = symbol_remove.sub('',lTitle)
####            symbol_remove = re.compile("['\u2764','\u3099','\u266a']")
####            lTitle = symbol_remove.sub('',lTitle)
####            '''
####            outfile_name = str(btItem['title'] + '.torrent')
####            outdir = str(torrentsPath + r'/' + btItem['title'])
####            if not os.path.exists(outdir):
####                os.makedirs(outdir)
####            outfile_full_path = str(outdir + r'/' + outfile_name)
####
####            if os.path.exists(outfile_full_path) and os.path.isfile(outfile_full_path) and os.access(outfile_full_path,os.R_OK):
####                print(Fore.RED + Style.BRIGHT + 'this torrent file already exist, skip.\n')
####            else:
####                #获取torrent代码
####                torrent_code,title,imglinklist = gettorrentlink3.get_torrentlink(myreq_url = link, enable_proxy = enable_proxy, proxy_string = proxy_string)
####                print('     CODE:', torrent_code)
####                print(title,imglinklist)
####                print('total ',len(imglinklist),' pics.')
####
######                torrent_item = {'tCode':torrent_code,'tTitle':title,'imgLinkList':imglinklist}
####                torrentItemList.append(torrent_item)
####
######                fileList = []
######                for imgLink in imglinklist:
######                    outdir = str(torrentsPath + r'/' + title)
######                    ifilename = imgLink[imgLink.rfind('/')+1:len(imgLink)]
######                    fileList.append({link:imgLink,ofile:ifilename})
####
####
####                #保存图片
####                getImgs(imglinklist,outdir)
######                if len(imglinklist) > 0:
######                    for imglink in imglinklist:
######                        picname,imgContent = getImg(imgLink = imglink)
######                        if len(imgContent) > 0:
######                            picFullpath = (outdir + r'/' + picname)
######                            ofile = open(picFullpath,'wb')
######                            ofile.write(imgContent)
######                            ofile.close()
####
####
####                #获取torrent内容
####                if torrent_code != 'notExist':
####                    torrent_content = gettorrent3.get_torrent(torrent_name_code = torrent_code, enable_proxy = enable_proxy, proxy_string = proxy_string)
####                    if b'<html>' not in torrent_content:
####                        #解码torrent
####                        try:
####                            btinfo = bencode.bdecode(torrent_content)
####                        except Exception as detail:
####                            print(Fore.RED + Style.BRIGHT + "     ERROR4: ",detail)
####                            print()
####                            continue
####                        #print '     decode torrent finished'
####
####
####                        '''
####                        info_list = []
####                        for i in btinfo:
####                            info_list.append(i)
####                            print(i)
####
####                        print("bt announce(tracker服务器列表):",btinfo[b'announce'].decode())
####                        print("bt announce-list(备用tracker列表):",btinfo[b'announce-list'].decode())
####                        lin_list=[]
####                        for udp_list in btinfo[b'announce-list']:
####                            for lin in udp_list:
####                                lin_list.append(lin.decode())
####                                print(lin.decode())
####                        print("bt comment:",btinfo[b'comment'].decode())
####                        print("bt creator:",btinfo[b'created by'].decode())
####                        print("bt 编码方式encoding:",btinfo[b'encoding'].decode())
####                        print("bt info:",btinfo[b'info'].decode())
####                        for k in btinfo[b'info'].keys():
####                            value = btinfo[b'info'][k]
####                            if k == b'files':
####                                print("total %d files"%len(value))
####                                for v_list_dic in value:
####                                    print(v_list_dic)
####                                    for files_k,files_v in v_list_dic.items():
####                                        print(files_k,files_v)
####                            elif k == b'name':
####                                print("file name:",value.decode())
####                            elif k == b'md5sum':
####                                print("md5:",value)
####                            elif k == b'length':
####                                print("file size:",value)
####                            elif k == b'path':
####                                print("file path name:",value)
####                            elif k == b'piece length':
####                                print("每个块的大小:",value)
####                            elif k == b'pieces':
####                                print("每个块的20个字节的SHA1 Hash的值（二进制格式）:",str(value))
####                        print("nodes的数据类型：",type(btinfo[b'nodes']))
####                        print(btinfo[b'nodes'])
####                        '''
####
####
####                        info = btinfo[b'info']
####                        btlist = {}
####                        fsize = 0
####                        for bfile in info[b'files']:
####                            if len(bfile[b'path']) > 1:
####                                fname0 = str(bfile[b'path'][0])+'/'+str(bfile[b'path'][1])
####                            else:
####                                fname0 = bfile[b'path'][0]
####                            btlist[bfile[b'path'][0]] = {'path':fname0,'size':bfile[b'length']} #生成新字典{path:{'path':path,'size':size}}
####
####                            if bfile[b'length'] > fsize:
####                                fname = fname0
####                                fsize = bfile[b'length']
####
####                        '''
####                        fsize = 0
####                        for key,val in btlist.items():
####                            if val['size'] > fsize:
####                                fsize = val['size']
####                                temppath = val['path']
####                                '''
####                        print('     files:',len(btlist))
####                        try:
####                            print('     the MAX file in the torrent is: ', fname.decode('utf-8'), ' size:', str(fsize))
####                        except Exception as detail:
####                            print('     Error5: ',detail)
####
####                        #输出torrent文件
####                        print('    save file to:', outfile_full_path)
####                        print()
####                        outFile = open(outfile_full_path,'wb')
####                        outFile.write(torrent_content)
####                        outFile.close()
####                        #time.sleep(1)
####                    else:
####                        print('torrent not exist!')
####                else:
####                    print('torrent_code not exist!')
####
####    print(torrentItemList)
    end_time = time.time()
    print('over',end_time-start_time,'s')

if __name__ == '__main__':
    #print __name__
    main()
