#! encoding=utf-8
import re
import datetime
import json
import sys
import argparse
import parseTimeMessage

class ParseMessage(object):
    def __init__(self, msg):
        self.msg = msg

    '''将字符串中的大写数字转换为小写数字'''
    def __parseDigit(self, s):
        s = re.sub(r'一',  '1', s)
        s = re.sub(r'二',  '2', s)
        s = re.sub(r'三',  '3', s)
        s = re.sub(r'四',  '4', s)
        s = re.sub(r'五',  '5', s)
        s = re.sub(r'六',  '6', s)
        s = re.sub(r'七',  '7', s)
        s = re.sub(r'八',  '8', s)
        s = re.sub(r'九',  '9', s)
        ret = re.search('[\d]+十', s)
        if ret:
            s1 = s[0: ret.span()[0]]
            s2 = s[ret.span()[1] - 1:]
            s = ''.join([s1, s2])
        s = re.sub(r'十',  '1', s)
        return s

    def __parseYearInner(self, s):
        # 今,本,当,去,前,大前
        s = re.sub(r'今',  str(datetime.datetime.now().year), s)
        s = re.sub(r'本',  str(datetime.datetime.now().year), s)
        s = re.sub(r'当',  str(datetime.datetime.now().year), s)
        s = re.sub(r'去',  str(datetime.datetime.now().year-1), s)
        s = re.sub(r'大前',  str(datetime.datetime.now().year-3), s)
        s = re.sub(r'前',  str(datetime.datetime.now().year-2), s)
        return s

    def __parseYear(self, s):
        tuple_s = s.partition('年')
        if tuple_s[1] == '年':
            s1 = self.__parseDigit(tuple_s[0])
            s1 = self.__parseYearInner(s1)
            s = ''.join([s1, tuple_s[1], tuple_s[2]])
        return s

    def __parseMonthInner(self, s):
        # 这,当,这个,上,上个,上上，上上个
        s = re.sub(r'这',  str(datetime.datetime.now().month), s)
        s = re.sub(r'这个',  str(datetime.datetime.now().month), s)
        s = re.sub(r'当',  str(datetime.datetime.now().month), s)
        s = re.sub(r'上上个',  str(datetime.datetime.now().month-2), s)
        s = re.sub(r'上上',  str(datetime.datetime.now().month-2), s)
        s = re.sub(r'上个',  str(datetime.datetime.now().month-1), s)
        s = re.sub(r'上',  str(datetime.datetime.now().month-1), s)
        return s

    def __parseMonth(self, s):
        tuple_s = s.partition('月')
        if tuple_s[1] == '月':
            s1 = self.__parseDigit(tuple_s[0])
            s1 = self.__parseMonthInner(s1)
            s = ''.join([s1, tuple_s[1], tuple_s[2]])
        return s

    def __parseDayInner(self, s):
        # 今,昨,前,大前
        s = re.sub(r'今',  str(datetime.datetime.now().day), s)
        s = re.sub(r'昨',  str(datetime.datetime.now().day - 1), s)
        s = re.sub(r'大前',  str(datetime.datetime.now().day - 3), s)
        s = re.sub(r'前',  str(datetime.datetime.now().day - 2), s)
        return s

    def __parseDay(self, s):
        tuple_s = s.partition('日')
        if tuple_s[1] == '日':
            s1 = self.__parseDigit(tuple_s[0])
            s1 = self.__parseDayInner(s1)
            s = ''.join([s1, tuple_s[1], tuple_s[2]])
        tuple_s = s.partition('天')
        if tuple_s[1] == '天':
            s1 = self.__parseDigit(tuple_s[0])
            s1 = self.__parseDayInner(s1)
            s = ''.join([s1, '日', tuple_s[2]])
        return s

    def __parseType(self, s, ret_obj):
        #照片,图,图片,picture,photo,jpg,tif,bmp,gif
        ret = re.split(r'(照片|图|图片|picture|photo|jpg|tif|bmp|gif)', s)
        if len(ret) > 1:
            ret_obj['search_type'] = 'picture'
            ret_obj['notes'] = '填写搜索种类为照片，进入搜索'
            return ret[0]
        #视频,录像,video,mp4,avi,mkv,wmv,m4v
        ret = re.split(r'(视频|录像|video|mp4|avi|mkv|wmv|m4v)', s)
        if len(ret) > 1:
            ret_obj['search_type'] = 'video'
            ret_obj['notes'] = '填写搜索种类为视频，进入搜索'
            return ret[0]

        #文件,文档,file,txt,doc,ppt
        ret = re.split(r'(文件|文档|file|txt|doc|ppt)', s)
        if len(ret) > 1:
            ret_obj['search_type'] = 'file'
            ret_obj['notes'] = '填写搜索种类为文档，进入搜索'
            return ret[0]
        #音乐，媒体，music,media,mp3,wma,m4a,
        ret = re.split(r'(音乐|媒体|music|media|mp3|wma|m4a)', s)
        if len(ret) > 1:
            ret_obj['search_type'] = 'music'
            ret_obj['notes'] = '填写搜索种类为音乐，进入搜索'
            return ret[0]

            #搜,找,查,search,lookfor,
        ret = re.split(r'(搜|找|查|search|lookfor)', s)
        if len(ret) > 1:
            ret_obj['search_type'] = 'search'
            ret_obj['notes'] = '进入搜索条件输入'
            return ret[0]
        #浏览,看,读,阅,look,watch,see,browse,
        ret = re.split(r'(浏览|看|读|阅|look|watch|see|browse)', s)
        if len(ret) > 1:
            ret_obj['search_type'] = 'look'
            ret_obj['notes'] = '进入NAS浏览'
            return ret[0]
        ret_obj['status'] = 'failed'
        ret_obj['error'] = '我现在还看不懂你的话，以后我会更聪明的。'
        return None

    # 将匹配的数字乘以 2
    def __year_fun(self, matched):
        value = matched.group('year')
        int_year = int(value)
        if len(value) == 2:
            str_year = str(datetime.datetime.now().year)
            int_year_now = int(str_year[2:])

            if int_year > int_year_now:
                int_year += 1900
            else:
                int_year += 2000
        return ''.join([str(int_year), '年'])

    '''
    {
              "search_type": "picture|video|file|music|search|label|look",
              "date_time": "2018年4月19日",
              "status": "failed/complete",
              "error": "素质！请注意素质！",
              "label_content": [],
              "notes":"注释"
    }
    '''
    def parseMessage(self):
        s = self.msg
        ret_obj = {}
        ret_obj['status'] = 'complete'
        # Case1 ：傻逼,2逼,傻X,妈逼,鸡巴,屌,fuck,shit,。。。等脏话关键词
        # 发送信息给用户：素质！请注意素质！break；
        ret = re.search(r'(傻逼|2逼|二逼|妈逼|鸡巴|屌|fuck|shit)', s)
        if ret:
            ret_obj['status'] = 'failed'
            ret_obj['error'] = '素质！请注意素质！'
            ret_json = json.dumps(ret_obj, ensure_ascii=False)
            return ret_json
        # 查询类型
        s = self.__parseType(s, ret_obj)
        if s is not None:
            s = self.__parseYear(s)
            s = self.__parseMonth(s)
            s = self.__parseDay(s)
            ret = re.findall(r'\d{2,4}年|\d{1,2}月|\d{2,4}日', s)
            if ret:
                ret[0] = re.sub(r'(?P<year>\d+)年', self.__year_fun, ret[0])
                ret_obj['date_time'] = ''.join(ret)
        ret_json = json.dumps(ret_obj, ensure_ascii=False)
        return ret_json

if __name__ == '__main__':
    # s = '搜索'
    # s = '去年照片'
    # s = '我要看看去年的照片'
    # s = '我想搜索去年12月照片'
    # s = '看看'
    # s = '查看14年照片'
    # s = '找一五年照片'
    # s = '看看89年照片'
    # s = '你二逼吧'
    # s = '2000年视频'
    # s = '你妈'
    # if len(sys.argv) > 1:
    #     s = str(sys.argv[1])
    # print(sys.argv)
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--msg', type=str, default=None)
    args = parser.parse_args()
    #s = args.msg.decode('GB2312').encode('utf-8')
    s = args.msg
    ps = ParseMessage(s)
    ret = ps.parseMessage()
    print(ret)
    tm = parseTimeMessage.ParseTimeMessage(s)
    ret = tm.parseTimeMessage()
    print(ret)
