# from threading import Thread, currentThread, Lock
# from uuid import uuid4 as uid, UUID
# from .datasheet import Datasheet
# from LocalLogging.logger import LoggerBase

# class Doc:
#    def __init__(self, sheet: Datasheet) -> None:
#       self.id = uid()
#       self.sheet = sheet
#       self.thread: Thread = None

#    def openDoc(self):
#       self.thread = Thread(target=)

#    def __eq__(self, o: object) -> bool:
#       if isinstance(o, Doc):
#          if o.sheet != None:
#             if o.sheet.name == self.sheet.name:
#                return True
#       else:
#          False

#    def __ne__(self, o: object) -> bool:
#       if isinstance(o, Doc):
#          if o.sheet == None:
#             return True
#          elif o.sheet.name != self.sheet.name:
#             return False
#       else:
#          True

# class DocManager:
#    def __init__(self, logger: LoggerBase) -> None:
#       self.logger = logger
#       self.docs: list[Doc] = []

#    def open(self, sheet: Datasheet) -> UUID:
#       try:
#          newDoc = Doc(sheet)
#          for doc in self.docs:
#             if doc != newDoc:
#                return None
#          newDoc.openDoc()
#       except Exception as e:
#          self.logger.error(e, 'Open Doc Error')