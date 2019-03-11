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

  def parseTimeMessage(self):
    s = self.msg
    ret_obj = {}
    ret_obj['status'] = 'complete'
    ret = re.search(self.load_keys['shit'].encode('utf-8'), s)
    if ret:
      ret_obj['status'] = 'failed'
      ret_obj['error'] = self.load_simple_answer['shit'].encode('utf-8')
      ret_json = json.dumps(ret_obj, ensure_ascii=False)
      return ret_json

if __name__ == '__main__':
  s = '傻x'
  ps = ParseTimeMessage(s)
  print(ps.parseTimeMessage())