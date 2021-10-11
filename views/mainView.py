from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLayout, QSpacerItem, QWidget, QBoxLayout, QListWidget, QListWidgetItem, QPushButton
from PySide6.QtCore import Slot
from LocalLogging.logger import LoggerBase
from models.datasheet import Datasheet, DatasheetCollection
from models.settings import Settings
from views.settingsView import SettingsView

class MainViewBox(QWidget):
   def __init__(self, parent=None) -> None:
      super(MainViewBox, self).__init__(parent)
      self.box = QBoxLayout(QBoxLayout.TopToBottom)

      self.listView = QListWidget()
      self.buildTestList()
      self.listView.itemClicked.connect(self.selectTest)
      print(self.listView.actions())

      self.button = QPushButton('Test')
      self.button.clicked.connect(self.clickTest)

      self.box.addWidget(self.listView)
      self.box.addWidget(self.button)
      self.setLayout(self.box)

   def buildTestList(self):
      testData = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
      for data in testData:
         self.listView.addItem(QListWidgetItem(QIcon(), data))

   @Slot()
   def clickTest(self):
      print('Hello')

   @Slot()
   def selectTest(self, args: QListWidgetItem):
      print(args.text())

class MainView(QWidget):
   def __init__(self, logger: LoggerBase, settings: Settings, parent=None) -> None:
      super(MainView, self).__init__(parent)
      self.logger = logger
      self.settings = settings
      self.settingsDialog = SettingsView(logger, self.settings)
      self.datasheets = DatasheetCollection(self.settings.datasheetsDir)
      self.seletedDatasheet: Datasheet = None

      self.grid = QGridLayout()

      self.openSettingsButton = QPushButton(QIcon(), 'Settings')
      self.openSettingsButton.clicked.connect(self.openSettingsDialog)
      self.updateButton = QPushButton(QIcon(), 'Update')
      self.updateButton.clicked.connect(self.updateDatasheets)

      self.menuButtonBox = QHBoxLayout()
      self.menuButtonBox.addWidget(self.openSettingsButton)
      self.menuButtonBox.addWidget(self.updateButton)

      self.datasheetListView = QListWidget()
      self.datasheetListView.itemClicked.connect(self.selectDatasheet)

      self.selectedNameText = QLabel()
      self.selectedViewBox = QBoxLayout(QBoxLayout.TopToBottom)
      self.openDatasheetButton = QPushButton(QIcon(), 'Open Datasheet')
      self.openDatasheetButton.clicked.connect(self.openDatasheet)
      self.selectedViewBox.addWidget(self.selectedNameText)
      self.selectedViewBox.addSpacerItem(QSpacerItem(0, 20))
      self.selectedViewBox.addWidget(self.openDatasheetButton)

      self.grid.addLayout(self.menuButtonBox, 0, 0, 1, 2)
      self.grid.addLayout(self.selectedViewBox, 1, 0)
      self.grid.addWidget(self.datasheetListView, 1, 1)
      self.setLayout(self.grid)
      self.logger.log('Main view constructed.')

      self.setMinimumSize(1000, 1000)

      self.updateDatasheets()

   def buildTestList(self):
      testData = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
      for data in testData:
         self.datasheetListView.addItem(QListWidgetItem(QIcon(), data))

   def buildList(self):
      if len(self.datasheets) > 0:
         self.datasheetListView.clear()
         for d in self.datasheets:
            self.datasheetListView.addItem(QListWidgetItem(QIcon(), d.name))

   @Slot()
   def selectDatasheet(self, args: QListWidgetItem):
      if args != None:
         self.selectedDatasheet = self.datasheets.find(args.text())
         self.selectedNameText.setText(self.selectedDatasheet.name)
         self.logger.log(f'Selected Datasheet Changed {self.selectedNameText}')

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
      self.buildList()

   @Slot()
   def openDatasheet(self):
      if self.selectedDatasheet != None:
         if not self.selectedDatasheet.isOpen:
            self.selectedDatasheet.openDatasheet()
         else:
            self.logger.log('Datasheet already open')