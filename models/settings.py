import os.path as Path
from json import dump, dumps, load
from types import MethodType
from typing import Any
from LocalLogging.logger import LoggerBase

class Settings:
   #region Default Props
   path = '/home/Daxxn/Documents/mySettings/datasheets.json'
   #endregion

   #region Init
   def __init__(self, logger: LoggerBase) -> None:
      self.logger = logger
      self.datasheetsDir = 'None'
      self.verbose = False
      self.console = True
      self.metadataPath = 'None'
      self.docViewer = 'evince'
   #endregion

   #region Methods
   def __str__(self):
      return f'SettingsPath: {self.path} Datasheets: {self.datasheetsDir} MetadataFile: {self.metadataPath} DocViewer: {self.docViewer}'

   def setDatasheetsDir(self, newDir: str):
      if Path.isdir(newDir):
         self.datasheetsDir = newDir
         return True
      return False

   #region Json
   def openSettings(self):
      try:
         with open(self.path, 'r') as file:
            data = load(file)
            self.deserialize(data)
      except Exception as e:
         self.logger.error(e, 'Open Settings Error.')

   def saveSettings(self):
      try:
         if Path.isfile(self.path):
            fileMode = 'w'
         else:
            fileMode = 'x'
         with open(self.path, fileMode) as file:
            data = self.serialize()
            dump(data, file, indent=3)
      except Exception as e:
         self.logger.error(e, 'SaveSettings Error')

   def serialize(self):
      output = {}
      output['datasheetsDir'] = self.datasheetsDir
      debug = {}
      debug['console'] = self.console
      debug['verbose'] = self.verbose
      output['debug'] = debug
      output['metadataPath'] = self.metadataPath
      output['docViewer'] = self.docViewer
         
   def deserialize(self, data: dict):
      try:
         self.datasheetsDir = data['datasheetsDir']
         self.metadataPath = data['metadataPath']
      except Exception as e:
         self.logger.error(e, 'datasheetsDir or metadataPath is missing from settings file.')

      if data['docViewer'] != None:
         self.docViewer = data['docViewer']
      else:
         self.logger.warn('No document viewer found in settings file.', 2, data)
      if data['debug'] != None:
         try:
            self.verbose = data['debug']['verbose']
            self.console = data['debug']['console']
         except Exception:
            self.logger.warn('Debug options not found in settings file.', 2, data)
      else:
         self.logger.warn('Debug options not found in settings file.', 2, data)
   #endregion

   def hardSet(self):
      self.datasheetsDir = '/home/Daxxn/Electrical/Docs/Datasheets/'
      self.console = True
      self.verbose = True
      self.metadataPath = '.metadata.json'
      self.docViewer = 'evince'
   #endregion
