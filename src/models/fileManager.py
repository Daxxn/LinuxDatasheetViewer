from json import load
from models.datasheet import Datasheet, DatasheetCollection
from models.settings import Settings
from models.tags import TagManager
from LocalLogging.logger import LoggerBase
import os.path as Path

def openMetadata(
   logger: LoggerBase,
   settings: Settings,
   datasheets: DatasheetCollection,
   tagManager: TagManager
):
   try:
      with open(
         Path.join(settings.datasheetsDir, settings.metadataPath),
         'r'
      ) as file:
         tagManager = datasheets.deserialize(load(file))
         return (datasheets, tagManager)
   except Exception as e:
      logger.error(e, 'Metadata File load error.', 320)

def saveMetadata(
   logger: LoggerBase,
   settings: Settings,
   datasheets: DatasheetCollection,
   tagManager: TagManager
):
   try:
      with open(
         Path.join(settings.datasheetsDir, settings.metadataPath),
         'w'
      ) as file:
         file.write(datasheets.serialize(tagManager))
   except Exception as e:
      logger.error(e, 'Metadata file save error.', 321)