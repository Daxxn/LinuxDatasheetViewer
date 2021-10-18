from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
   QComboBox,
   QGridLayout,
   QHBoxLayout,
   QLabel,
   QLineEdit,
   QListWidget,
   QListWidgetItem,
   QPushButton,
   QSplitter,
   QSplitterHandle,
   QVBoxLayout,
   QWidget)
from models.settings import Settings
from models.datasheet import Datasheet, DatasheetCollection
from models.tags import Tag, TagManager
from LocalLogging.logger import LoggerBase
import os.path as Path

class EditorView(QWidget):
   #region Init
   def __init__(
      self,
      settings: Settings,
      logger: LoggerBase,
      datasheets: DatasheetCollection,
      tags: TagManager,
      updateCallback,
      parent: QWidget = None
   ) -> None:
      super().__init__(parent)

      #region Props
      self.settings = settings
      self.logger = logger
      self.tagManager = tags
      self.updateCallback = updateCallback
      self.datasheets = datasheets

      self.selectedDatasheet: Datasheet = None
      self.newSelectedTag: Tag = None
      self.selectedTag: Tag = None
      self.newTag: Tag = None
      #endregion

      #region View

      #region List
      self.datasheetListView = QListWidget()
      self.datasheetListView.itemClicked.connect(self.selectDatasheet)
      #endregion

      #region Controls
      self.controlsBox = QHBoxLayout()

      self.setNamesBtn = QPushButton(QIcon(), 'Set Part Names')
      self.setNamesBtn.clicked.connect(self.setAllPartNames)
      self.controlsBox.addWidget(self.setNamesBtn)

      self.saveBtn = QPushButton(QIcon(), 'Save')
      self.saveBtn.clicked.connect(self.saveDatasheets)
      self.controlsBox.addWidget(self.saveBtn)
      #endregion

      #region Selected View
      self.selectedDSGrid = QGridLayout()

      #region Labels
      selectedDSTitle = QLabel('Selected Datasheet')
      partNameLabel = QLabel('Part')
      fileTypeLabel = QLabel('File Type')
      descLabel = QLabel('Desc')
      tagsLabel = QLabel('Tags')
      self.selectedDSGrid.addWidget(selectedDSTitle, 0, 0, 1, 2)
      self.selectedDSGrid.addWidget(partNameLabel, 1, 0)
      self.selectedDSGrid.addWidget(fileTypeLabel, 2, 0)
      self.selectedDSGrid.addWidget(descLabel, 3, 0)
      self.selectedDSGrid.addWidget(tagsLabel, 4, 0, 1, 2)

      #region Tags Controls
      self.selectedTagsList = QListWidget()
      self.selectedTagsList.itemClicked.connect(self.selectedTagChanged)
      tagsBox = QVBoxLayout()
      tagControlsBox = QHBoxLayout()

      # self.newTagText = QLineEdit('NewTag')
      # tagControlsBox.addWidget(self.newTagText)
      self.newTagCB = QComboBox()
      for t in self.tagManager.tags:
         self.newTagCB.addItem(QIcon(), t.name, t)
      self.newTagCB.setEditText('newTag')
      self.newTagCB.setEditable(True)
      self.newTagCB.activated.connect(self.newTagCBActivated)
      tagControlsBox.addWidget(self.newTagCB)

      self.newTagBtn = QPushButton(QIcon(), 'Add')
      self.newTagBtn.clicked.connect(self.newTagClick)
      tagControlsBox.addWidget(self.newTagBtn)

      self.delTagBtn = QPushButton(QIcon(), 'Remove')
      self.delTagBtn.clicked.connect(self.delTagClick)
      tagControlsBox.addWidget(self.delTagBtn)

      tagsBox.addLayout(tagControlsBox)
      tagsBox.addWidget(self.selectedTagsList)
      self.selectedDSGrid.addLayout(tagsBox, 5, 0, 1, 2)
      #endregion
      #endregion

      self.selectedPartText = QLineEdit('')
      self.selectedTypeText = QLabel('')
      self.selectedDescText = QLineEdit('')
      self.selectedPartText.textChanged.connect(self.updatePart)
      self.selectedDescText.textChanged.connect(self.updateDesc)
      self.selectedDSGrid.addWidget(self.selectedPartText, 1, 1)
      self.selectedDSGrid.addWidget(self.selectedTypeText, 2, 1)
      self.selectedDSGrid.addWidget(self.selectedDescText, 3, 1)
      #endregion

      #region Grid
      self.grid = QGridLayout()
      datasheetListBox = QVBoxLayout()
      self.openDatasheetBtn = QPushButton(QIcon(), 'Open Datasheet')
      self.openDatasheetBtn.clicked.connect(self.openDatasheet)
      datasheetListBox.addWidget(self.datasheetListView)
      datasheetListBox.addWidget(self.openDatasheetBtn)
      self.grid.addLayout(datasheetListBox, 0, 0, 2, 1)

      self.grid.addLayout(self.selectedDSGrid, 0, 1)
      self.grid.addLayout(self.controlsBox, 1,1)
      self.setLayout(self.grid)
      #endregion

      #endregion
   #endregion

   #region Methods
   def updateDatasheets(self):
      self.updateCallback(self.datasheets)

   def getDatasheets(self, datasheets: DatasheetCollection):
      self.datasheets = datasheets
      self.buildMainList()
   
   def buildMainList(self):
      for d in self.datasheets:
         self.datasheetListView.addItem(QListWidgetItem(QIcon('./src/Resources/Icons/FileIcon.png'), d.name))

   @Slot()
   def openDatasheet(self):
      if self.selectedDatasheet != None:
         if not self.selectedDatasheet.isOpen:
            self.selectedDatasheet.openDatasheet(self.settings.docViewer, lambda : print(f'Opening {self.selectedDatasheet.name}'))
         else:
            self.logger.log('Datasheet already open')

   @Slot(QListWidgetItem)
   def selectDatasheet(self, args: QListWidgetItem):
      if args != None:
         self.selectedDatasheet = self.datasheets.find(args.text())
         self.logger.log(f'Selected Datasheet Changed: {self.selectedDatasheet.name}')
         self.setSelectedText()
         # self.setTags()

   @Slot(QListWidgetItem)
   def selectTag(self, args: QListWidgetItem):
      if args != None:
         if self.selectedDatasheet != None:
            self.selectedTag = self.datasheets.find(args.text())

   def setSelectedText(self):
      self.selectedPartText.setText(self.selectedDatasheet.partName)
      self.selectedTypeText.setText(self.selectedDatasheet.fileType)
      self.selectedDescText.setText(self.selectedDatasheet.desc)
      self.setSelectedTagsList()
      # self.setTags()

   def setSelectedTagsList(self):
      self.selectedTagsList.clear()
      for tag in self.selectedDatasheet.tags:
         self.selectedTagsList.addItem(QListWidgetItem(QIcon('./src/Resources/Icons/TagIcon.png'), tag.name))

   #region Text Updates
   @Slot(str)
   def updateDesc(self, text: str):
      self.selectedDatasheet.desc = text

   @Slot(str)
   def updatePart(self, text: str):
      self.selectedDatasheet.partName = text
   #endregion

   #region Tags
   @Slot(QListWidgetItem)
   def selectedTagChanged(self, tagItem: QListWidgetItem):
      self.selectedTag = self.tagManager.findTag(tagItem.text())

   # @Slot(int)
   # def newTagChanged(self, index: int):
   #    self.newTag = self.newTagCB.currentData()


   @Slot()
   def newTagClick(self):
      if self.selectedDatasheet != None:
         if self.newSelectedTag != None:
            self.selectedDatasheet.addTag(self.newSelectedTag)
         else:
            tag = self.tagManager.add(self.newTagCB.currentText())
            self.selectedDatasheet.addTag(tag)
            self.updateCallback()
         self.setSelectedText()

   @Slot()
   def delTagClick(self):
      self.selectedDatasheet.remTag(self.selectedTag)
      self.setSelectedText()

   # @Slot(str)
   # def filterTagNames(self, text: str):
   #    self.newTagText = text
   #    tags = self.tagManager.filter(text)

   @Slot(str)
   def updateNewTagText(self, text):
      self.newTagText = text
      tag = self.tagManager.findTag(text)
      if tag != None:
         self.newSelectedTag = tag

   @Slot(int)
   def newTagCBActivated(self, index: int):
      tempTag = self.newTagCB.currentData()
      self.newSelectedTag = tempTag

   def setTags(self, tags: list[Tag] = None):
      if tags == None:
         if self.tagManager.tags != None:
            if len(self.tagManager.tags) > 0:
               self.newTagCB.clear()
               for tag in self.tagManager.getTags():
                  self.newTagCB.addItem(QIcon('./src/Resources/Icons/TagIcon.png'), tag.name, tag)
      else:
         self.newTagCB.clear()
         for tag in self.tagManager.getTags():
            self.newTagCB.addItem(QIcon('./src/Resources/Icons/TagIcon.png'), tag.name, tag)
   #endregion

   @Slot()
   def setAllPartNames(self):
      if self.datasheets != None:
         for ds in self.datasheets:
            if ds.partName == '':
               ds.partName = ds.name

   def saveDatasheets(self):
      try:
         with open(Path.join(self.settings.datasheetsDir, self.settings.metadataPath), 'w') as file:
            data = self.datasheets.serialize(self.tagManager)
            file.write(data)
      except Exception as e:
         self.logger.error(e, 'Datasheet Save Error')
   #endregion
