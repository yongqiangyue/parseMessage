#! encoding=utf-8

import re
import datetime
import json
import arrow

class ParseTimeMessage(object):
  def __init__(self, msg):
    self.msg = msg
    self._haveYear = False
    self._haveMonth = False
    self._haveDay = False
    self._year = 0
    self._month = 0
    self._day = 0
    with open("./keys.json", 'r') as load_f:
      self.load_keys = json.load(load_f)
    with open("./simpleAnswer.json", 'r') as load_f:
      self.load_simple_answer = json.load(load_f)

  def __parseSimple(self, s, key):
    ret_obj = {}
    ret_obj['status'] = 'complete'
    ret = re.search(self.load_keys[key].encode('utf-8'), s)
    if ret:
      ret_obj['status'] = 'failed'
      ret_obj['error'] = self.load_simple_answer[key].encode('utf-8')
      ret_json = json.dumps(ret_obj, ensure_ascii=False)
      return ret_json
    return None

  def __parseShit(self, s):
    # 文明用语
    return self.__parseSimple(s, 'shit')

  def __parseSimpleAnswer(self, s):
    # 简单问答
    ret_obj = self.__parseSimple(s, 'broken')
    if ret_obj:
      return ret_obj
    ret_obj = self.__parseSimple(s, 'kill')
    if ret_obj:
      return ret_obj
    ret_obj = self.__parseSimple(s, 'hello')
    if ret_obj:
      return ret_obj
    ret_obj = self.__parseSimple(s, 'dowhat')
    if ret_obj:
      return ret_obj
    ret_obj = self.__parseSimple(s, 'good')
    if ret_obj:
      return ret_obj
    ret_obj = self.__parseSimple(s, 'fool')
    if ret_obj:
      return ret_obj
    return self.__parseSimple('default', 'default')

  def __preParseMessage(self, s):
    s = re.sub(r' |1，|,', "", s)
    return s

  '''将字符串中的大写数字转换为小写数字'''

  def __parseDigit(self, s):
    s = re.sub(r'一', '1', s)
    s = re.sub(r'二', '2', s)
    s = re.sub(r'三', '3', s)
    s = re.sub(r'四', '4', s)
    s = re.sub(r'五', '5', s)
    s = re.sub(r'六', '6', s)
    s = re.sub(r'七', '7', s)
    s = re.sub(r'八', '8', s)
    s = re.sub(r'九', '9', s)
    s = re.sub(r'零|〇', '0', s)
    ret = re.match("(.*?)([\d]*?)十([\d]*)(.*)", s)
    if ret:
      s1 = ret.group(1) + ret.group(2)
      if ret.group(2):
        s1 += '0'
      else:
        s1 += '1'
        if not ret.group(3).isdigit():
          s1 += '0'
      s2 = ret.group(3) + ret.group(4)
      s = ''.join([s1, s2])
    return s

  def __parseType(self, s, ret_obj):
    # 搜索 “照片”“图片”“picture”如果存在就认为定位在照片。变量定位=“照片”
    ret = re.split(r'(照片|图|图片|picture)', s)
    if len(ret) > 1:
      ret_obj['search_type'] = 'picture'
      ret_obj['notes'] = '照片'
      return
    # 搜索“视频”“video”如果存在就认为定位在视频。变量定位=“视频”
    ret = re.split(r'(视频|video)', s)
    if len(ret) > 1:
      ret_obj['search_type'] = 'video'
      ret_obj['notes'] = str('视频')
      return

    # 搜索“文档”“document”如果存在就认为定位在其他。变量定位=“文档”
    ret = re.split(r'(文档|document)', s)
    if len(ret) > 1:
      ret_obj['search_type'] = 'file'
      ret_obj['notes'] = '文档'
      return
    ret_obj['search_type'] = 'all'
    ret_obj['notes'] = '全部文件'
    return

  def __parseDayInner(self, s):
    # 前天
    # 昨天|昨日|前日|前1天
    # 今天|今日|当天|当日|本日|本天|此日|此天
    # 大前天
    ret = re.search(r'前天', s)
    if ret:
      _date = datetime.datetime.now().date() - datetime.timedelta(days=2)
      self._day = _date.day
      self._month = _date.month
      self._year = _date.year
      self._haveDay = True
      return
    ret = re.search(r'昨天|昨日|前日|前1天', s)
    if ret:
      _date = datetime.datetime.now().date() - datetime.timedelta(days=1)
      self._day = _date.day
      self._month = _date.month
      self._year = _date.year
      self._haveDay = True
      return
    ret = re.search(r'今天|今日|当天|当日|本日|本天|此日|此天', s)
    if ret:
      self._day = datetime.datetime.now().day
      self._month = datetime.datetime.now().month
      self._haveDay = True
      return
    ret = re.search(r'大前天', s)
    if ret:
      _date = datetime.datetime.now().date() - datetime.timedelta(days=3)
      self._day = _date.day
      self._month = _date.month
      self._year = _date.year
      self._haveDay = True
      return
    return

  def __parseDay(self, s):
    tuple_s = s.partition('日')
    if tuple_s[1] == '日':
      self.__parseDayInner(s)
    tuple_s = s.partition('天')
    if tuple_s[1] == '天':
      self.__parseDayInner(s)

  def __parseMonthInner(self, s):
    # 这个月|这月|当月|本月|此月
    # 上个月|上月|前月|前个月|前1月
    ret = re.search(r'这个月|这月|当月|本月|此月', s)
    if ret:
      self._month = datetime.datetime.now().month
      self._haveMonth = True
      self._year = datetime.datetime.now().year
      return
    ret = re.search(r'上个月|上月|前月|前个月|前1月', s)
    if ret:
      _tmpMonth = arrow.now()
      self._month = _tmpMonth.shift(months=-1).date().month
      self._haveMonth = True
      self._year = _tmpMonth.shift(months=-1).date().year
      return
    return

  def __parseMonth(self, s):
    tuple_s = s.partition('月')
    # self._month = 0
    if tuple_s[1] == '月':
      self.__parseMonthInner(s)

    return

  def __parseYearInner(self, s):
    # 今年|当年|本年|这年|这1年
    # 去年|上年|前1年|上1年
    ret = re.search(r'今年|当年|本年|这年|这1年', s)
    if ret:
      self._haveYear = True
      self._year = datetime.datetime.now().year
      return
    ret = re.search(r'去年|上年|前1年|上1年', s)
    if ret:
      self._haveYear = True
      self._year = datetime.datetime.now().year - 1
      return
    ret = re.search(r'前年', s)
    if ret:
      self._haveYear = True
      self._year = datetime.datetime.now().year - 2
      ret = re.search(r'大前年', s)
      if ret:
        self._haveYear = True
        self._year = datetime.datetime.now().year - 3
      return
    ret = re.search(r'大前年', s)
    if ret:
      self._haveYear = True
      self._year = datetime.datetime.now().year - 3
      return
    return

  def __parseYear(self, s):
    tuple_s = s.partition('年')
    if tuple_s[1] == '年':
      self.__parseYearInner(s)
    return

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
    return str(int_year)

  def parseTimeMessage(self):
    s = self.msg
    ret_obj = self.__parseShit(s)
    if ret_obj:
      return ret_obj
    # 去掉全部空格，全部英文逗号，中文逗号，中文空格
    s = self.__preParseMessage(s)
    # print(s)
    ret_obj = {}
    ret_obj['status'] = 'complete'
    s = self.__parseDigit(s)
    self.__parseType(s, ret_obj)
    # 时间解析:日
    self.__parseDay(s)
    # 时间解析:月
    self.__parseMonth(s)
    # print(s)
    # 时间解析:年
    self.__parseYear(s)

    ret = re.match(r'(.*?)([\d]{2,4}年)(.*)', s)
    if ret:
      if not self._haveYear and ret.group(2):
        _tmpYear = re.sub(r'(?P<year>\d+)年', self.__year_fun, ret.group(2))
        self._year = int(_tmpYear)

    ret = re.match(r'(.*?)([\d]{1,2})月(.*)', s)
    if ret:
      if not self._haveMonth and ret.group(2):
        self._month = ret.group(2)

    ret = re.match(r'(.*?)([\d]{1,2})日(.*)', s)
    if ret:
      if not self._haveDay and ret.group(2):
        self._day = ret.group(2)
    else:
      ret = re.match(r'(.*?)([\d]{1,2})号(.*)', s)
      if ret:
        if not self._haveDay and ret.group(2):
          self._day = ret.group(2)
    # print('year:' + str(self._year))
    # print('month:' + str(self._month))
    # print('day:' + str(self._day))
    # print('hvaeyear:' + str(self._haveYear))
    # print('havemonth:' + str(self._haveMonth))
    # print('haveday:' + str(self._haveDay))
    if self._year > 0 and self._month == 0 and self._day > 0:
      ret_obj['status'] = 'failed'
      ret_obj['error'] = str(self._year) + '年里' + str(self._day) + '号多了去了，您到底要找哪个月的内容呀？'
    elif (not self._haveDay) and (self._day > 0):
      if (not self._haveYear) and self._year == 0:
        self._year = datetime.datetime.now().year
      if (not self._haveMonth) and self._month == 0:
        self._month = datetime.datetime.now().month
    elif (not self._haveMonth) and self._month > 0:
      if (not self._haveYear) and self._year == 0:
        self._year = datetime.datetime.now().year
      if self._year == datetime.datetime.now().year and self._month > datetime.datetime.now().month:
        self._year -= 1

    # print('year:' + str(self._year))
    # print('month:' + str(self._month))
    # print('day:' + str(self._day))
    # print('hvaeyear:' + str(self._haveYear))
    # print('havemonth:' + str(self._haveMonth))
    # print('haveday:' + str(self._haveDay))
    if self._year == 0 and self._month == 0 and self._day == 0:
      return self.__parseSimpleAnswer(s)

    if self._year > 0 and self._month > 0 and self._day > 0:
      ret_obj['date_time'] = "{0}年{1}月{2}日".format(self._year, self._month, self._day)
    elif self._month > 0 and self._day == 0:
      ret_obj['date_time'] = "{0}年{1}月".format(self._year, self._month)
    elif self._month == 0 and self._day == 0:
      ret_obj['date_time'] = "{0}年".format(self._year)
    ret_json = json.dumps(ret_obj, ensure_ascii=False)
    return ret_json


if __name__ == '__main__':
  # s = '前天的照片'
  # s = '去年的今天的照片'
  s = '18年1月照片'
  # s = '13年2月文件'
  # s = '上个月6号的视频'
  # s = '昨天的文档'
  # s = '大前年的今天的照片'
  # s = '上个月的昨天的视频'
  # s = '前年12号的文件'
  ps = ParseTimeMessage(s)
  ret = ps.parseTimeMessage()
  print(ret)
