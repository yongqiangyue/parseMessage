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

  def parseTimeMessage(self):
    s = self.msg
    ret_obj = self.__parseShit(s)
    if ret_obj:
     return ret_obj
    
    #todo
    return self.__parseSimpleAnswer(s)
    ret_obj = {}
    ret_obj['status'] = 'complete'
    return ret_obj

if __name__ == '__main__':
  s = '做什么'
  ps = ParseTimeMessage(s)
  print(ps.parseTimeMessage())