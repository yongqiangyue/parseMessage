#! encoding=utf-8

import re
import datetime
import json
import sys

class ParseTimeMessage(object):
  def __init__(self, msg):
    self.msg = msg
    with open("./keys.json",'r') as load_f:
      self.load_keys = json.load(load_f)
    with open("./simpleAnswer.json",'r') as load_f:
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
    return self.__parseSimple(s, 'default')

  def __preParseMessage(self, s):
    s = re.sub(r' |1，|,',  "", s)
    return s

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
    s = re.sub(r'零|〇',  '0', s)
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
      # print(s)
      # print(ret.group())
      # print(ret.group(1))
      # print(ret.group(2))
      # print(ret.group(3))
      # print(ret.group(4))
      # s1 = s[0: ret.span()[0]]
      # print(ret.span())
      # print(ret.span()[1])
      # s2 = s[ret.span()[1] - 2:]
      # print(s2)
      # s = ''.join([s1, s2])
    # s = re.sub(r'十',  '1', s)
    return s

  def __parseType(self, s, ret_obj):
    #搜索 “照片”“图片”“picture”如果存在就认为定位在照片。变量定位=“照片”
    ret = re.split(r'(照片|图|图片|picture)', s)
    if len(ret) > 1:
      ret_obj['search_type'] = 'picture'
      ret_obj['notes'] = '照片'
      return
    #搜索“视频”“video”如果存在就认为定位在视频。变量定位=“视频”
    ret = re.split(r'(视频|video)', s)
    if len(ret) > 1:
      ret_obj['search_type'] = 'video'
      ret_obj['notes'] = str('视频')
      return

    #搜索“文档”“document”如果存在就认为定位在其他。变量定位=“文档”
    ret = re.split(r'(文档|document)', s)
    if len(ret) > 1:
      ret_obj['search_type'] = 'file'
      ret_obj['notes'] = '文档'
      return
    ret_obj['search_type'] = 'all'
    ret_obj['notes'] = '全部文件'
    return

  def parseTimeMessage(self):
    s = self.msg
    ret_obj = self.__parseShit(s)
    if ret_obj:
     return ret_obj
    #去掉全部空格，全部英文逗号，中文逗号，中文空格
    s = self.__preParseMessage(s)
    # print(s)
    ret_obj = {}
    ret_obj['status'] = 'complete'
    s = self.__parseDigit(s)
    self.__parseType(s, ret_obj)

    # print(s)
    # return self.__parseSimpleAnswer(s)
    return ret_obj

if __name__ == '__main__':
  s = 'a十0b'
  print(s)
  ps = ParseTimeMessage(s)
  ret = ps.parseTimeMessage()
  print(ret)
