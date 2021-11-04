from os import name
from bs4 import BeautifulSoup
import re
Matcher = re.compile("(\d+)-?(\d+)*")

class TableParser():
    __soup = None
    __Daily = {
        1:[],
        2:[],
        3:[],
        4:[],
        5:[],
        6:[],
        7:[],
    }
    def __init__(self,filename):
        self.__getHandleFile(filename)
        self.__getTable()
    def __getHandleFile(self,filename):
        text = ""
        with open(filename,"r",encoding="utf8") as f:
            for line in f.readlines():
                text+=line
        self.__soup = BeautifulSoup(text,"lxml")
    def __getTable(self):
        if self.__soup == None:
            raise Exception("文件获取错误")
        soup = self.__soup
        mainTable = soup.select_one("#kblist_table")
        for i in range(1,8):
            subTableId = "#xq_"+str(i)
            subTable = mainTable.select_one(subTableId)
            trs = subTable.find_all("tr")
            self.__Daily[i] = self.__handleDay(trs)

    def getDay(self,day):
        return self.__Daily[day]


    def __handleDay(self,trs):
        if len(trs) <= 1:
            return []
        ls = []
        lastTd = ""
        for idx,tr in enumerate(trs):
            if idx == 0:
                continue
            tds = tr.select("td")
            td = tds[0] if len(tds) < 2 else tds[1]
            lastTd = during = lastTd if len(tds) < 2 else tds[0].text
            title = td.select_one(".title").text.strip()
            week = td.select("p font")[0].text.strip()
            ls.extend(self.__extractInfo(during,title,week))
        return ls

    def __extractInfo(self,during,title,week):
        rtl = []
        during = Matcher.findall(during)
        weeks = Matcher.findall(week)
        for wk in weeks:
            rtl.append({
                "title":title,
                "startTime": during[0][0],
                "endTime":during[0][1] if during[0][1]!="" else during[0][0],
                "startWeek":wk[0],
                "endWeek":wk[1] if wk[1]!="" else wk[0],
            })
        return rtl

    def getALLDay(self):
        return self.__Daily

        



        
if __name__ == "__main__":
    tb = TableParser("./table.htm")
    print(tb.getALLDay())

