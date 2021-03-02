"""
This is a sample Spider
"""

from urllib import request
import re


class Spider:
    url = "https://www.huya.com/g/wzry"
    root_pattern = r'<li class="game-live-item" gid="[\d]+" data-lp="[\d]+">([\s\S]+?)</li>'
    name_pattern = r'<i class="nick" title="[\s\S]*?">([\s\S]*?)</i>'
    number_pattern = r'<i class="js-num">([\s\S]*?)</i>'

    @classmethod
    def __fetch_content(cls):
        r = request.urlopen(cls.url)
        htmls = r.read()
        htmls = str(htmls, 'utf-8')
        return htmls

    @classmethod
    def __analysis(cls, htmls):
        list_html = re.findall(cls.root_pattern, htmls)
        anchors = []
        for html in list_html:
            name = re.findall(cls.name_pattern, html)
            number = re.findall(cls.number_pattern, html)
            anchor = {
                'name': name[0].strip(),
                'number': number[0].strip(),
            }
            anchors.append(anchor)
        return anchors

    @staticmethod
    def __refine(anchors):
        return anchors

    @classmethod
    def __sort(cls, anchors):
        anchors = sorted(anchors, key=cls.__sort_seed, reverse=True)
        return anchors

    @staticmethod
    def __sort_seed(anchor):
        number_str = anchor["number"]
        r = re.findall(r"[1-9]\d*\.?\d*", number_str)
        number = float(r[0])
        if '万' in number_str:
            number *= 10000
        return number

    @staticmethod
    def __show(anchors):
        for rank in range(0, len(anchors)):
            anchor = anchors[rank]
            print('rank ' + str(rank) + ":\t" + anchor["name"] + "\t" + anchor["number"])

    @classmethod
    def go(cls):
        htmls = cls.__fetch_content()
        anchors = cls.__analysis(htmls)
        anchors = cls.__refine(anchors)
        anchors = cls.__sort(anchors)
        cls.__show(anchors)


if __name__ == '__main__':
    Spider.go()
