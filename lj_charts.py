# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from echarts import Echart, Legend, Bar, Axis


class Charts:

    def __init__(self,x,y,title='GDP',desc='',table=''):
        self.title = title
        self.desc = desc
        self.table = table
        self.x = x
        self.y = y

    def draw(self):
        chart = Echart(self.title,self.desc)
        chart.use(Bar(self.table, self.y))
        chart.use(Legend(self.title))
        chart.use(Axis('category', 'bottom', data=self.x))
        chart.plot()

if __name__ == '__main__':
    chart = Charts(['Nov', 'Dec', 'Jan', 'Feb'], [2, 10, 4, 5])
    chart.draw()