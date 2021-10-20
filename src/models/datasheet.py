from threading import Thread
from models.settings import Settings
from models.tags import Tag, TagManager
from uuid import uuid4 as uid
from json import dumps
import os.path as Path
import os

#region Close
class CloseException(Exception):
   def __init__(self) -> None:
      super().__init__()
#endregion

#region Datasheet
class Datasheet:
   #region Init
   def __init__(self, path: str, partName: str = None) -> None:
      self.id = uid()
      self.path = path
      self.partName = partName
      self.isOpen = False
      self.thread: Thread = None
      self.viewer: str = ''
      self.desc: str = ''
      self.tags: list[Tag] = []
      self.fileType: str = '.pdf'
      if Path.isfile(path):
         self.name = Path.basename(path)
      else:
         self.name = None
   #endregion

   #region Methods
   def addTag(self, tag: Tag):
      if not self.tags.__contains__(tag):
         self.tags.append(tag)

   def remTag(self, tag: Tag):
      if self.tags.__contains__(tag):
         self.tags.remove(tag)

   def __str__(self):
      temp = {}
      temp['path'] = self.path
      temp['desc'] = self.desc
      temp['partName'] = self.partName
      temp['fileType'] = self.fileType
      temp['tags'] = TagManager.serialize(self.tags)
      return dumps(temp, indent=3)
         
   def open(self):
      '''Opens the file viewer'''
      os.system(f'{self.viewer} \"{self.path}\"')
      self.isOpen = False
      self.updateCallback()

   def openDatasheet(self, viewer: str, updateCallback):
      '''Starts a new thread if the file is not open and starts the viewer'''
      if not self.isOpen:
         self.isOpen = True
         self.viewer = viewer
         self.updateCallback = updateCallback
         self.thread = Thread(target=self.open)
         self.thread.start()

   def closeDatasheet(self):
      '''I dont think im going to be able to do this..'''
      if self.isOpen:
         print('Not implemented.')
         # self.thread.
         # os.kill(self.thread.native_id, 1)

   def serialize(self):
      temp = {}
      temp['path'] = self.path
      temp['desc'] = self.desc
      temp['partName'] = self.partName
      temp['fileType'] = self.fileType
      temp['tags'] = TagManager.serialize(self.tags)
      return temp

   @staticmethod
   def deserialize(tagManager: TagManager, data: dict):
      newDatasheet = Datasheet(data['path'], data['partName'])
      newDatasheet.desc = data['desc']
      newDatasheet.tags = tagManager.deserialize(data['tags'])
      return newDatasheet
   #endregion
#endregion

#region Datasheet Collection
class DatasheetCollection:
   #region Default Props
   index: int = -1
   #endregion

   #region Init
   def __init__(self, settings: Settings, sheets: list[Datasheet] = None) -> None:
      self.datasheets = sheets
      self.settings = settings
   #endregion

   #region Methods
   def add(self, sheet: Datasheet):
      if not self.datasheets.__contains__(sheet):
         self.datasheets.append(sheet)

   def remove(self, sheet):
      if self.datasheets.__contains__(sheet):
         self.datasheets.remove(sheet)

   def deleteTag(self, tag: Tag):
      for ds in self.datasheets:
         ds.remTag(tag)

   def clear(self):
      self.datasheets = []

   # def load(self, rootPath: str):
   #    try:
   #       if Path.isdir(rootPath):
   #          self.rootDir = rootPath
   #          self.datasheets = []
   #          files = os.listdir(self.rootDir)
   #          for file in files:
   #             fileName, ext = Path.splitext(file)
   #             if ext.lower() == '.pdf':
   #                self.datasheets.append(Datasheet(Path.join(rootPath, file), fileName))
   #    except Exception as e:
   #       print(str(e))
   
   def loadNew(self):
      if Path.isdir(self.settings.datasheetsDir):
         datasheets: list[Datasheet] = []
         files = os.listdir(self.settings.datasheetsDir)
         for file in files:
            fileName, ext = Path.splitext(file)
            if ext.lower() == '.pdf':
               datasheets.append(Datasheet(Path.join(self.settings.datasheetsDir, file), fileName))

         for ds in datasheets:
            alreadyExists = False
            for d in self.datasheets:
               if ds.name == d.name:
                  alreadyExists = True
                  break
            if not alreadyExists:
               self.datasheets.append(ds)


   def find(self, value: str):
      if len(self.datasheets) > 0:
         if value != None:
            for ds in self.datasheets:
               if ds.name == value:
                  return ds
      return None

   def serialize(self, tagManager: TagManager):
      output = {}
      output['data'] = []
      for ds in self.datasheets:
         output['data'].append(ds.serialize())

      output['tags'] = tagManager.serializeAll()

      try:
         return dumps(output, indent=3)
      except Exception as e:
         print(str(e))

   def deserialize(self, data: dict):
      tagManager = TagManager(self.settings, TagManager.deserializeAll(data['tags']))
   
      newDatasheets: list[Datasheet] = []

      for ds in data['data']:
         newDatasheets.append(Datasheet.deserialize(tagManager, ds))

      self.datasheets = newDatasheets
      return tagManager

   def __iter__(self):
      return self

   def __next__(self):
      self.index += 1

      if self.index >= len(self.datasheets):
         self.index = -1
         raise StopIteration

      return self.datasheets[self.index]

   def __len__(self) -> int:
      return len(self.datasheets)
   #endregion
#endregion
