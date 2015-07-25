#-*_coding:utf8-*-
import requests
import codecs
import re
# import sys
# reload(sys)
# # sys.setdefualencoding("utf-8")
# url = ''
# # headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
#
# # html.encoding = 'utf8'
# # print html.text
# data = {
#
# }
# html = requests.post(url,data=data)
# print html.text
# title = re.findall('class="card-title">(.*?)</div>',html.text,re.S)
# for each in title:
#     print each
class spider(object):
    def __init__(self):
        print u'正在爬取内容……'

    def getsource(self,url):
        html = requests.get(url)
        return html.text

    def changepage(self, url , totalpage):
        nowpage = int(re.search('pageNum=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(nowpage,totalpage+1):
            link = re.sub('pageNum=(\d+)','pageNum=%s'%i,url,re.S)
            page_group.append(link)
        return page_group

    def geteveryclass(self,source):
        everyclass = re.findall('(<li id=".*?</li>)',source,re.S)
        return everyclass

    def getinfo(self,eachclass):
        info = {}
        info['title'] = re.search('class="lessonimg" title="(.*?)" alt',eachclass,re.S).group(1)
        info['content'] = re.search('none;">(.*?)</p>',eachclass,re.S).group(1).strip()
        timeandlevel = re.findall('<em>(.*?)</em>',eachclass,re.S)
        info['classtime'] = timeandlevel[0]
        info['classlevel'] = timeandlevel[1]
        info['learnnum'] = re.search('"learn-number">(.*?)</em>',eachclass,re.S).group(1)
        return info

    def saveinfo(self,classinfo):
        f = codecs.open('info.txt','a','utf-8')
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('content:' + each['content'] + '\n')
            f.writelines('classtime:' + each['classtime'] + '\n')
            f.writelines('classlevel:' + each['classlevel'] + '\n')
            f.writelines('learnnum:' + each['learnnum'] + '\n')
            f.writelines('\n')
        f.close()

if __name__ == '__main__':
    classinfo = []
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    jikespider = spider()
    all_links = jikespider.changepage(url,1)
    for link in all_links:
        print u'正在处理页面：' + link
        html = jikespider.getsource(link)
        everyclass = jikespider.geteveryclass(html)
        for each in everyclass:
            info = jikespider.getinfo(each)
            classinfo.append(info)
    jikespider.saveinfo(classinfo)
