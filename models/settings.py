import os.path as Path
from json import dump, dumps, load
from types import MethodType
from typing import Any
from LocalLogging.logger import LoggerBase

class Settings:
   path = '/home/Daxxn/Documents/mySettings/datasheets.json'
   def __init__(self, logger: LoggerBase) -> None:
      self.logger = logger
      self.datasheetsDir = 'test'
      self.verbose = False
      self.console = True

   def __dict__(self):
      output = dict()
      for k in self.__dir__():
         if not k.startswith('_'):
            item = self.__getattr__(k)
            if type(item) != MethodType:
               output[k] = item
      return output

   def __getattr__(self, name: str) -> Any:
      return object.__getattribute__(self, name)

   # def __setattr__(self, name: str, value: Any) -> None:
   #    object.__setattr__(self, name, value)

   def __str__(self):
      return dumps(self.__dict__())

   def setDatasheetsDir(self, newDir: str):
      if Path.isdir(newDir):
         self.datasheetsDir = newDir
         return True
      return False

   def openSettings(self):
      try:
         with open(self.path, 'r') as file:
            data = dict(load(file))
            for k in data.keys():
               setattr(self, k, data[k])
      except Exception as e:
         self.logger.error(e, 'Open Settings Error.')

   def saveSettings(self):
      try:
         if Path.isfile(self.path):
            fileMode = 'w'
         else:
            fileMode = 'x'
         with open(self.path, fileMode) as file:
            data = self.__dict__()
            dump(data, file)
      except Exception as e:
         self.logger.error(e, 'SaveSettings Error')

