from types import MethodType
from PySide6.QtCore import QMimeData, QModelIndex, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QTableWidget, QTextEdit, QWidget, QLabel
from models.datasheet import DatasheetCollection
from models.settings import Settings
from LocalLogging.logger import LoggerBase
from models.tags import Tag, TagManager

class TagView(QWidget):
   #region Init
   def __init__(
      self,
      logger: LoggerBase,
      settings: Settings,
      tagManager: TagManager,
      datasheets: DatasheetCollection,
      updateTagsCallback: MethodType,
      parent=None
   ) -> None:
      super(TagView, self).__init__(parent)
      #region Parameters
      self.tagManager: TagManager = tagManager
      self.datasheets = datasheets
      self.settings = settings
      self.logger = logger
      self.selectedTag: Tag = None
      self.updateTagsCallback = updateTagsCallback
      #endregion

      #region Tag List
      self.tagList = QListWidget()
      self.tagList.itemClicked.connect(self.selectedTagChanged)
      # self.updateTags()
      #endregion

      #region Controls
      self.controlsLayout = QHBoxLayout()
      self.addTagBtn = QPushButton(QIcon(), 'Add')
      self.addTagBtn.clicked.connect(self.addTag)
      self.controlsLayout.addWidget(self.addTagBtn)

      self.addText = QLineEdit('')
      self.addText.setPlaceholderText('New Tag')
      self.addText.returnPressed.connect(self.addTag)
      self.controlsLayout.addWidget(self.addText)

      self.removeTagBtn = QPushButton(QIcon(), 'Remove')
      self.removeTagBtn.clicked.connect(self.removeTag)
      self.controlsLayout.addWidget(self.removeTagBtn)
      #endregion

      #region Layout
      self.mainLayout = QGridLayout()
      self.mainLayout.addLayout(self.controlsLayout, 0, 0)
      self.mainLayout.addWidget(self.tagList, 1, 0)
      self.setLayout(self.mainLayout)
      #endregion
   #endregion

   #region Methods
   def updateTags(self):
      tags = self.tagManager.getTags()
      self.tagList.clear()
      for tag in tags:
         newItem = QListWidgetItem(QIcon('./src/Resources/Icons/TagIcon.png'), tag.name)
         self.tagList.addItem(newItem)
      self.updateTagsCallback()

   @Slot()
   def addTag(self):
      self.tagManager.add(self.addText.text())
      self.updateTags()

   @Slot()
   def removeTag(self):
      if self.selectedTag != None:
         self.datasheets.deleteTag(self.selectedTag)
         self.tagManager.remove(self.selectedTag)
         self.updateTags()

   @Slot()
   def selectedTagChanged(self, args: QListWidgetItem):
      self.selectedTag = self.tagManager.find(args.text())
   #endregion