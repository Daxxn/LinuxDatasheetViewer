from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
   QCheckBox,
   QComboBox,
   QGridLayout,
   QHBoxLayout,
   QLabel,
   QLineEdit,
   QRadioButton,
   QTabWidget,
   QWidget,
   QBoxLayout,
   QListWidget,
   QListWidgetItem,
   QPushButton
)
from PySide6.QtCore import Qt, Slot
from LocalLogging.logger import LoggerBase
from models.datasheet import Datasheet, DatasheetCollection
from models.settings import Settings
from models.tags import TagManager
from views.settingsView import SettingsView
from views.tagView import TagView
from enum import Enum

class SearchMode(Enum):
   Name = 0
   Tag = 1
   Desc = 2

   @staticmethod
   def fromInt(num: int):
      if num == 0:
         return SearchMode.Name
      elif num == 1:
         return SearchMode.Tag
      elif num == 2:
         return SearchMode.Desc
      else:
         return None

class MainView(QWidget):
   #region Init
   def __init__(self, logger: LoggerBase, settings: Settings, parent=None) -> None:
      super(MainView, self).__init__(parent)

      #region Parameters
      self.logger = logger
      self.settings = settings
      self.tagManager = TagManager(settings)
      self.tagsView = TagView(logger, settings, self.tagManager, self.updateTagsList)
      self.settingsDialog = SettingsView(logger, self.settings)
      self.datasheets = DatasheetCollection(self.settings)
      self.searchResults = DatasheetCollection(self.settings)
      self.seletedDatasheet: Datasheet = None
      self.searchMode = SearchMode.Name
      self.searchCase = False
      #endregion

      #region View

      #region Search
      self.searchGrid = QGridLayout()

      self.searchText = QLineEdit('search')
      self.searchText.textChanged.connect(self.searchDatasheets)
      self.searchGrid.addWidget(self.searchText, 0, 0, Qt.AlignLeft)

      self.searchTypeCombo = QComboBox()
      self.searchTypeCombo.addItem(QIcon(), 'Name', SearchMode.Name)
      self.searchTypeCombo.addItem(QIcon(), 'Tags', SearchMode.Tag)
      self.searchTypeCombo.addItem(QIcon(), 'Desc', SearchMode.Desc)
      self.searchTypeCombo.currentIndexChanged.connect(self.searchTypeChanged)
      self.searchGrid.addWidget(self.searchTypeCombo, 0, 1)

      self.searchCaseBtn = QRadioButton('Match Case')
      self.searchCaseBtn.toggled.connect(self.searchCaseToggle)
      self.searchGrid.addWidget(self.searchCaseBtn, 0, 2)

      self.searchBtn = QPushButton(QIcon(), 'Search')
      self.searchBtn.clicked.connect(self.searchDatasheets)
      self.searchGrid.addWidget(self.searchBtn, 0, 3, Qt.AlignRight)

      self.searchList = QListWidget()
      self.searchGrid.addWidget(self.searchList, 1, 0, 1, 4)
      self.searchList.setMaximumHeight(400)
      self.searchList.itemClicked.connect(self.selectDatasheet)
      #endregion

      #region Main View Controls
      self.openSettingsButton = QPushButton(QIcon(), 'Settings')
      self.openSettingsButton.clicked.connect(self.openSettingsDialog)
      self.updateButton = QPushButton(QIcon(), 'Update')
      self.updateButton.clicked.connect(self.updateDatasheets)

      self.menuButtonBox = QHBoxLayout()
      self.menuButtonBox.addWidget(self.openSettingsButton)
      self.menuButtonBox.addWidget(self.updateButton)

      #region Datasheet List
      self.datasheetListView = QListWidget()
      self.datasheetListView.itemClicked.connect(self.selectDatasheet)
      #endregion

      #region Selected Item
      self.selectedItemGrid = QGridLayout()
      self.selectedPartText = QLabel()
      self.selectedTypeText = QLabel()
      self.selectedDescText = QLabel()
      self.selectedTagsList = QListWidget()
      self.selectedOpenCheck = QCheckBox()
      self.selectedOpenCheck.stateChanged.connect(self.openCheckChanged)
      self.selectedOpenCheck.setEnabled(False)

      self.selectedItemGrid.addWidget(self.selectedOpenCheck, 1, 1)
      self.selectedItemGrid.addWidget(self.selectedPartText, 2, 1)
      self.selectedItemGrid.addWidget(self.selectedTypeText, 3, 1)
      self.selectedItemGrid.addWidget(self.selectedDescText, 4, 1)
      self.selectedItemGrid.addWidget(self.selectedTagsList, 6, 1, 1, 2)

      #region Labels
      selectedTitle = QLabel()
      selectedTitle.setText('Selected Datasheet')

      selectedNameLabel = QLabel()
      selectedNameLabel.setText('Part')

      selectedTypeLabel = QLabel()
      selectedTypeLabel.setText('File Type')

      selectedDescLabel = QLabel()
      selectedDescLabel.setText('Desc')

      selectedTagsLabel = QLabel()
      selectedTagsLabel.setText('Tags')

      selectedOpenLabel = QLabel()
      selectedOpenLabel.setText('Open')

      self.selectedItemGrid.addWidget(selectedTitle, 0, 0, 1, 2)
      self.selectedItemGrid.addWidget(selectedOpenLabel, 1, 0)
      self.selectedItemGrid.addWidget(selectedNameLabel, 2, 0)
      self.selectedItemGrid.addWidget(selectedTypeLabel, 3, 0)
      self.selectedItemGrid.addWidget(selectedDescLabel, 4, 0)
      self.selectedItemGrid.addWidget(selectedTagsLabel, 5, 0, 1, 2)
      #endregion

      #region Selected Controls
      self.openDatasheetButton = QPushButton(QIcon(), 'Open Datasheet')
      self.openDatasheetButton.clicked.connect(self.openDatasheet)
      self.selectedItemGrid.addWidget(self.openDatasheetButton, 7, 0, 1, 2, Qt.AlignRight)
      #endregion
      #endregion
      #endregion

      #region Grid
      self.grid = QGridLayout()
      self.grid.addLayout(self.menuButtonBox, 0, 0, 1, 2)
      self.grid.addLayout(self.selectedItemGrid, 1, 0, 2, 1)
      self.grid.addWidget(self.datasheetListView, 1, 1)
      self.grid.addLayout(self.searchGrid, 2, 1)
      #endregion

      #region Main View
      self.mainView = QWidget()
      self.mainView.setLayout(self.grid)
      #endregion

      self.tabContainer = QTabWidget()
      self.tabContainer.addTab(self.mainView, QIcon(), 'Datasheets')
      self.tabContainer.addTab(self.tagsView, QIcon(), 'Tags')
      # self.tabContainer.addTab(self.docViewer, QIcon(), 'Doc Viewer')

      # self.setLayout(self.grid)
      self.tempBox = QBoxLayout(QBoxLayout.TopToBottom)
      self.tempBox.addWidget(self.tabContainer)
      self.setLayout(self.tempBox)
      self.logger.log('Main view constructed.')
      #endregion

      self.setMinimumSize(1000, 1000)

      self.updateDatasheets()
   #endregion

   #region Methods
   def buildMainList(self):
      for d in self.datasheets:
         self.datasheetListView.addItem(QListWidgetItem(QIcon(), d.name))

   def buildSearchList(self):
      self.searchList.clear()
      for d in self.searchResults:
         self.searchList.addItem(QListWidgetItem(QIcon(), d.name))

   @Slot(QListWidgetItem)
   def selectDatasheet(self, args: QListWidgetItem):
      if args != None:
         self.selectedDatasheet = self.datasheets.find(args.text())
         # self.selectedNameText.setText(self.selectedDatasheet.name)
         self.logger.log(f'Selected Datasheet Changed: {self.selectedDatasheet.name}')
         self.setSelectedText()

   def setSelectedText(self):
      self.selectedOpenCheck.setChecked(self.selectedDatasheet.isOpen)
      self.selectedPartText.setText(self.selectedDatasheet.name)
      self.selectedTypeText.setText(self.selectedDatasheet.fileType)
      self.selectedDescText.setText(self.selectedDatasheet.desc)
      self.setSelectedTagsList()

   def setSelectedTagsList(self):
      tags = [tag.name for tag in self.selectedDatasheet.tags]
      self.selectedTagsList.clear()
      self.selectedTagsList.addItems(tags)
      # for tag in self.selectedDatasheet.tags:

   @Slot()
   def openSettingsDialog(self):
      self.logger.log('Opening Settings')
      self.settingsDialog.show(self.settings)
      # print(self.settings.datasheetsDir)
      self.logger.log(f'Settings Changed: {self.settings}')
      try:
         self.updateDatasheets()
      except Exception as e:
         self.logger.error(e, 'Settings Error')

   @Slot()
   def updateDatasheets(self):
      self.datasheets.load(self.settings.datasheetsDir)
      self.buildMainList()

   @Slot()
   def openDatasheet(self):
      if self.selectedDatasheet != None:
         if not self.selectedDatasheet.isOpen:
            self.selectedDatasheet.openDatasheet(self.settings.docViewer, self.updateOpen)
         else:
            self.logger.log('Datasheet already open')
         self.updateOpen()

   def updateOpen(self):
      self.selectedOpenCheck.setChecked(self.selectedDatasheet.isOpen)

   @Slot()
   def updateTagsList(self):
      tags = self.tagManager.getTags()
      self.searchList.clear()
      for tag in tags:
         newItem = QListWidgetItem(QIcon(), tag.name)
         self.searchList.addItem(newItem)

   #region Search Methods
   @Slot(str)
   def searchDatasheets(self, text: str):
      self.searchResults.clear()
      tempText = text
      if not self.searchCase:
         tempText = text.lower()
      if text != '':
         if self.searchMode == SearchMode.Tag:
            tag = self.tagManager.find(text)
            for ds in self.datasheets:
               if ds.tags.index(tag) != -1:
                  self.searchResults.add(ds)
         elif self.searchMode == SearchMode.Name:
            for ds in self.datasheets:
               tempName = ds.name
               if not self.searchCase:
                  tempName = tempName.lower()
               if tempName.find(tempText) != -1:
                  self.searchResults.add(ds)
         elif self.searchMode == SearchMode.Desc:
            for ds in self.datasheets:
               tempName = ds.name
               if not self.searchCase:
                  tempName = tempName.lower()
               if tempName.find(tempText) != -1:
                  self.searchResults.add(ds)
      self.buildSearchList()

   @Slot(int)
   def searchTypeChanged(self, index: int):
      if index != -1:
         print(type(index))
         self.searchMode = SearchMode.fromInt(index)
         self.searchDatasheets(self.searchText.text())

   @Slot(bool)
   def searchCaseToggle(self, state: bool):
      self.searchCase = state
      self.searchDatasheets(self.searchText.text())

   @Slot(bool)
   def openCheckChanged(self, state: bool):
      self.selectedOpenCheck.setChecked(self.selectedDatasheet.isOpen)
   #endregion
   #endregion