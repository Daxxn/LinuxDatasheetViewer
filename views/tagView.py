from types import MethodType
from PySide6.QtCore import QMimeData, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QTableWidget, QTextEdit, QWidget, QLabel
from models.settings import Settings
from LocalLogging.logger import LoggerBase
from models.tags import Tag, TagManager

class TagView(QWidget):
   def __init__(
      self,
      logger: LoggerBase,
      settings: Settings,
      tagManager: TagManager,
      updateTagsCallback: MethodType,
      parent=None
   ) -> None:
      super(TagView, self).__init__(parent)
      self.tagManager: TagManager = tagManager
      self.settings = settings
      self.logger = logger
      self.tempName = 'New Name'
      self.selectedTag: Tag = None
      self.updateTagsCallback = updateTagsCallback

      self.tagList = QListWidget()
      self.tagList.itemClicked.connect(self.selectedTagChanged)
      # self.updateTags()

      self.controlsLayout = QHBoxLayout()
      self.addTagBtn = QPushButton(QIcon(), 'Add')
      self.addTagBtn.clicked.connect(self.addTag)
      # self.addTagBtn.clicked.connect(self.updateTagsCallback)
      self.controlsLayout.addWidget(self.addTagBtn)

      self.addText = QLineEdit(self.tempName)
      self.controlsLayout.addWidget(self.addText)

      self.removeTagBtn = QPushButton(QIcon(), 'Remove')
      self.removeTagBtn.clicked.connect(self.removeTag)
      # self.removeTagBtn.clicked.connect(self.updateTagsCallback)
      self.controlsLayout.addWidget(self.removeTagBtn)

      self.mainLayout = QGridLayout()
      self.mainLayout.addLayout(self.controlsLayout, 0, 0)
      self.mainLayout.addWidget(self.tagList, 1, 0)
      self.setLayout(self.mainLayout)

   def updateTags(self):
      tags = self.tagManager.getTags()
      self.tagList.clear()
      mime = QMimeData()
      for tag in tags:
         newItem = QListWidgetItem(QIcon(), tag.name)
         self.tagList.addItem(newItem)
      self.updateTagsCallback()

   @Slot()
   def addTag(self):
      self.tagManager.add(self.addText.text())
      self.updateTags()

   @Slot()
   def removeTag(self):
      if self.selectedTag != None:
         self.tagManager.remove(self.selectedTag)
         self.updateTags()

   @Slot()
   def selectedTagChanged(self, args: QListWidgetItem):
      self.selectedTag = self.tagManager.find(args.text())