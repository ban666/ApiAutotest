# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import requests
from bs4 import BeautifulSoup
import xlsxwriter
from datetime import datetime


class LjSpider:

    def __init__(self,crawl_page=10,region='donghugaoxin',price='p4',room='l3',order='co32l3p4'):
        self.region = region
        self.price = price
        self.room = room
        self.order = order
        self.crwal_page = crawl_page
        self.url='https://m.lianjia.com/wh/ershoufang/%s/%s/%s/%s/pg%s/'
        self.result = []

    def crwal(self,url):
        html = requests.get(url).content
        lj=BeautifulSoup(html,'html.parser')
        house_info = lj.find_all('li',attrs={'class':'pictext'})
        for house in house_info:
            base_info = house.find_all('div',attrs={'class':'item_other text_cut'})[0].text
            room_type,room_size,room_way,xiaoqu_name = base_info.split('/')
            total = house.find_all('span',attrs={'class':'price_total'})[0].text
            unit = house.find_all('span',attrs={'class':'unit_price'})[0].text
            # print house.find_all('a',attrs={'class':'a_mask'})[0].href
            tags = ''
            for tag in house.find_all('div',attrs={'class':'tag_box'}):
                tags = tags + tag.text + ','
            tags = tags.replace('\n','')
            tags = tags[:-1]
            ret = [xiaoqu_name,room_type,room_size,room_way,total,unit,tags]
            # print ret
            self.result.append(ret)

    def start(self):
        if self.crwal_page>1:
            for i in range(1,self.crwal_page):
                url = self.url % (self.region,self.price,self.room,self.order,str(i))
                self.crwal(url)
            self.write_to_excel(self.result)
        else:
            url = self.url % (self.region,self.price,self.room,self.order,str(1))
            self.result.append(self.crwal(url))
            self.write_to_excel(self.result)

    def write_to_excel(self,data,folder='g:/ljdata/'):
        import os
        if not os.path.exists(folder):
            os.mkdir(folder)
        fname = folder+self.region + datetime.now().strftime( '%Y%m%d%H%M%S')+'.xlsx'
        wb = xlsxwriter.Workbook(fname)
        ws = wb.add_worksheet()
        data = [x for x in data if not isinstance(x,type(None))]
        unit_size = len(data[0])
        ws.set_column(0,unit_size,22)
        for i in range(len(data)):
            for j in range(unit_size):
                content = self.ensure_writeble(data[i][j])
                ws.write(i+1,j,content)
        wb.close()

    def ensure_writeble(self,content):
        try:
            content = content.decode('utf-8')
        except:
            pass
        return content
    
if __name__ == '__main__':
    LjSpider(10).start()