# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from lxml import etree
from lxml.etree import XMLParser

class CaseHandler:

    def __init__(self,fn,output):
        self.fn = fn
        self.output = output
        self.Z = 0
        self.total = 0

    def check_type(self,el):
        #1：纯suite
        #2：纯case
        #3：混合
        tlist = []
        for e in el:
            tlist.append(e.tag)
        if 'testsuite' in tlist and not 'testcase' in tlist:
            return 1
        if 'testsuite' in tlist and 'testcase' in tlist:
            return 2
        if not 'testsuite' in tlist and 'testcase' in tlist:
            return 3

    def add_pre(self,el,pri = 3):
        #pri 为优先级筛选 1、低 2、中 3、高
        if el.tag == 'testsuite':
            for j in el:
                if j.tag =='testcase':
                        for k in j:
                            if k.tag == 'importance':
                                if k.text!=str(pri):
                                    j.getparent().remove(j)
                                    self.Z +=1
                        self.total += 1
                if self.check_type(j) !=2:
                    self.add_pre(j,pri)

    def start(self,pri=3):
        with open(self.fn,'r+') as f:
            content = f.read()
        parser = XMLParser(strip_cdata=False)
        case = etree.fromstring(content, parser)
        tree = case.getroottree()
        root = tree.getroot()
        for el in root:
            self.add_pre(el,pri)
        final = etree.tostring(tree, encoding='utf-8', xml_declaration=True)
        with open(self.output,'w+') as f:
            f.write(final)
        print '%s cases total!' % (str(self.total))
        print '%s cases has been found!' % (str(self.total-self.Z))

if __name__ == '__main__':
    fn = 'g:/downloads/abc.xml'
    output = 'g:/a.xml'
    ch = CaseHandler(fn,output)
    ch.start()