#meo.py
import re
import httplib2
import time
import os.path,os
from bs4 import BeautifulSoup
import json
from pprint import pprint

http = httplib2.Http()
def autoRetryHttpRequest(link,times=5):
    header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}
    time.sleep(0.5)
    for i in range(times):
        try :
            response,content = http.request(link,headers=header)
            #return http.request(link)
        except :
            print('****retry****')
            time.sleep(3)
            continue
        else:
            return response,content

class Imgpp:
    def __init__(self,imgpageurl,window_=None):
        self.req_status,self.req_content=autoRetryHttpRequest(imgpageurl)
        #self.req_content=imgpageurl
        self.decoded_content=self.req_content.decode('utf-8')
        self.soup=BeautifulSoup(self.decoded_content)
        self.get_info()
        self.get_related_posts()
        self.window=window_

        if self.window :
            self.update_displayed_info()


    def get_info(self):
        p=self.soup.find('div',id="post-view").script.text
        pp=re.findall( 'Post[.]register_resp[(](.+)[)];',p )[0]
        self.imginfo=json.loads( pp )

    def get_related_posts(self):
        self.previous=None
        self.next=None
        for a in self.soup.find('h5' ,text='Related Posts').parent.find_all('a') :
            if a.text.find('Previous')!=-1 :
                self.previous=a['href']
            if a.text.find('Next')!=-1 :
                self.next=a['href']

    def update_displayed_info(self):
        self.window.update(self.imginfo)
        pass

    def go_next_img(self,mode='default'):
        self.window.current_object=Imgpp(self.next,self.window)

class Postpp:
    def __init__(self,imgpageurl):
        self.req_status,self.req_content=autoRetryHttpRequest(imgpageurl)
        #self.req_content=imgpageurl
        self.decoded_content=self.req_content.decode('utf-8')
        self.soup=BeautifulSoup(self.decoded_content)
        self.get_post_list()
        self.get_related_page()

    def get_post_list(self):
        for sc in self.soup.find_all('script', type="text/javascript"):
            if sc.text.find('Post.register') !=-1 :   
                self.poolcc=[json.loads(x) for x in re.findall('Post.register[(]([{].+[}])[)]',sc.text)]

        '''
        self.post_list=[]
        for li in self.soup.find('ul',id="post-list-posts").find_all('li'):
            if li.find('span',class_="plid") :
                self.post_list.append({})
                self.post_list[-1]['plid' ]=li.find('span',class_="plid").text
                self.post_list[-1]['id'   ]=li['id']
                self.post_list[-1]['title'         ]=li.find('img',class_="preview")['title']
                self.post_list[-1]['preview_url'   ]=li.find('img',class_="preview")['src']   #full path
                self.post_list[-1]['preview_width' ]=li.find('img',class_="preview")['width']
                self.post_list[-1]['preview_height']=li.find('img',class_="preview")['height']
        '''
    def get_related_page(self):
        self.next_page=None
        self.preview_page=None
        for a in self.soup.find('div', id="paginator").find_all('a'):
            if  a.has_attr('href') and a.has_attr('class'):
                if a['class']=="next_page" :
                    self.next_page=a['href']
            elif  a.has_attr('href') and a.has_attr('class'):
                if a['class']=="previous_page" :
                    self.next_page=a['href']


class Poolpp:
    def __init__(self,imgpageurl):
        self.req_status,self.req_content=autoRetryHttpRequest(imgpageurl)
        #self.req_content=imgpageurl
        self.decoded_content=self.req_content.decode('utf-8')
        self.soup=BeautifulSoup(self.decoded_content)
        self.get_pool_list()

    def get_pool_list(self):
        self.pool_post_list=[]
        for sc in self.soup.find_all('script', type="text/javascript"):
            if sc.text.find('Post.register_resp') !=-1 :   
                self.poolcc=json.loads( re.findall('Post.register_resp[(]([{].+[}])[)];',sc.text)[0] )             


poolurl=r'https://yande.re/pool/show/3875'
poolt=Poolpp(poolurl)

imgurl=r'https://yande.re/post/show/332370'
imgt=Imgpp(imgurl)

posturl=r'https://yande.re/post'
postt=Postpp(posturl)


'''
poolfile=r'C:\APP_O\python3\GUI\yande_viewer\yande_viewer\Cinderella-time  yande_re.htm'
with open(poolfile,'rb') as bf:
    icont=bf.read()
    poolt=Poolpp(icont)

imgfile=r'C:\APP_O\python3\GUI\yande_viewer\yande_viewer\img#303561  yande_re.htm'
with open(imgfile,'rb') as bf:
    icont=bf.read()
    imgt=Imgpp(icont)

postfile=r'C:\APP_O\python3\GUI\yande_viewer\yande_viewer\-  Page 2  yande_re.htm'
with open(postfile,'rb') as bf:
    icont=bf.read()
    postt=Postpp(icont)
'''