from threading import Thread
from models.tags import Tag
from uuid import uuid4 as uid
from json import dumps
import os.path as Path
import os

class Datasheet:
   def __init__(self, path: str, name: str = None) -> None:
      self.id = uid()
      self.path = path
      self.isOpen = False
      self.thread: Thread = None
      self.desc: str = ''
      self.tags: list[Tag] = []
      self.partName: str = ''
      self.fileType: str = '.pdf'
      if Path.isfile(path):
         self.name = name if name != None else Path.basename(path)
      else:
         self.name = None

   def __str__(self):
      return dumps(self, indent=3)

   def open(self):
      os.system(f'evince \"{self.path}\"')
      self.isOpen = False

   def openDatasheet(self):
      if not self.isOpen:
         self.isOpen = True
         self.thread = Thread(target=self.open)
         self.thread.start()

   def closeDatasheet(self):
      if self.isOpen:
         self.thread.ident

class DatasheetCollection:
   index: int = -1
   def __init__(self, root: str, sheets: list[Datasheet] = None) -> None:
      self.datasheets = sheets
      self.rootDir = root

   def add(self, sheet: Datasheet):
      if not self.datasheets.__contains__(sheet):
         self.datasheets.append(sheet)

   def remove(self, sheet):
      if self.datasheets.__contains__(sheet):
         self.datasheets.remove(sheet)

   def load(self, rootPath: str):
      try:
         if Path.isdir(rootPath):
            self.rootDir = rootPath
            self.datasheets = []
            files = os.listdir(self.rootDir)
            for file in files:
               fileName, ext = Path.splitext(file)
               if ext.lower() == '.pdf':
                  self.datasheets.append(Datasheet(Path.join(rootPath, file), fileName))
      except Exception as e:
         print(str(e))

   def find(self, value: str):
      if len(self.datasheets) > 0:
         if value != None:
            for ds in self.datasheets:
               if ds.name == value:
                  return ds
      return None

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
