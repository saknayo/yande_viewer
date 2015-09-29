#meo.py
import re
import httplib2
import time
import os.path,os
from bs4 import BeautifulSoup

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
    def __init__(self,imgpageurl):
        self.req_status,self.req_content=autoRetryHttpRequest(imgpageurl)
        #self.req_content=imgpageurl
        self.decoded_content=self.req_content.decode('utf-8')
        self.soup=BeautifulSoup(self.decoded_content)
        self.get_info()
        self.get_related_posts()


    def get_info(self):
        p=self.soup.find('div',id="post-view").script.text
        pp=re.findall( 'Post[.]register_resp[(](.+)[)];',p )[0]
        true=True
        false=False
        null=None
        self.imginfo=eval( pp )

    def get_related_posts(self):
        self.previous=None
        self.next=None
        for a in self.soup.find('h5' ,text='Related Posts').parent.find_all('a') :
            if a.text.find('Previous')!=-1 :
                self.previous=a['href']
            if a.text.find('Next')!=-1 :
                self.next=a['href']

class Postpp:
    def __init__(self,imgpageurl):
        #self.req_status,self.req_content=autoRetryHttpRequest(imgpageurl)
        self.req_content=imgpageurl
        self.decoded_content=self.req_content.decode('utf-8')
        self.soup=BeautifulSoup(self.decoded_content)
        self.get_list()
        self.get_related_page()

    def get_list(self):
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



iurl=r'C:\Python34\pack\GUI\picbro\001\#324063_yande_re.htm'
with open(iurl,'rb') as bf:
    icont=bf.read()

#iurl=r'https://yande.re/post/show/332138'
tt=Postpp(iurl)
