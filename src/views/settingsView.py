import os.path as Path
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QCheckBox, QDialog, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from LocalLogging.logger import LoggerBase

from models.settings import Settings

class SettingsView(QDialog):
   #region Init
   def __init__(self, logger: LoggerBase, currentSettings: Settings = None, parent = None) -> None:
      super(SettingsView, self).__init__(parent)
      #region Parameters
      self.logger = logger
      self.settings = currentSettings if currentSettings != None else Settings()
      #endregion

      #region View

      #region Datasheet Dir Controls
      self.openFolderButton = QPushButton(QIcon(), 'Open Folder')
      self.openFolderButton.clicked.connect(self.selectDatasheetDir)
      self.fileDialog = QFileDialog(
         self,
         'Select Datasheet Folder',
         self.settings.datasheetsDir if self.settings.datasheetsDir != '' else '~/Documents/'
      )
      self.fileDialog.setFileMode(QFileDialog.FileMode.Directory)
      self.datasheetsDirText = QLineEdit(self.settings.datasheetsDir)
      self.datasheetsDirText.textChanged.connect(self.updateDatasheetDir)

      self.box = QBoxLayout(QBoxLayout.TopToBottom)
      datasheetsDirLayout = QHBoxLayout()
      datasheetsDirLayout.addWidget(QLabel('Datasheet Folder'))
      datasheetsDirLayout.addWidget(self.datasheetsDirText)
      datasheetsDirLayout.addWidget(self.openFolderButton)
      self.box.addLayout(datasheetsDirLayout)

      #endregion

      #region Doc Viewer
      docBox = QHBoxLayout()
      docBox.addWidget(QLabel('Doc Viewer Command'))
      self.docViewerText = QLineEdit(self.settings.docViewer)
      self.docViewerText.textChanged.connect(self.updateDocViewer)
      docBox.addWidget(self.docViewerText)
      self.box.addLayout(docBox)
      #endregion

      #region Metadata
      metaBox = QHBoxLayout()
      metaBox.addWidget(QLabel('Metadata File Name'))
      self.metadataText = QLineEdit(self.settings.metadataPath)
      self.metadataText.textChanged.connect(self.updateMetadata)
      metaBox.addWidget(self.metadataText)
      self.box.addLayout(metaBox)
      #endregion

      #region Debug
      debugBox = QBoxLayout(QBoxLayout.TopToBottom)
      debugLabel = QLabel('Debug')
      # debugLabel.setAlignment(Qt.AlignCenter)
      debugBox.addWidget(debugLabel)

      #region Verbose
      self.verboseCheck = QCheckBox('Verbose')
      self.verboseCheck.setChecked(self.settings.verbose)
      self.verboseCheck.clicked.connect(self.updateVerbose)
      debugBox.addWidget(self.verboseCheck)
      #endregion

      #region Console
      self.consoleCheck = QCheckBox('Console')
      self.consoleCheck.setChecked(self.settings.console)
      self.consoleCheck.clicked.connect(self.updateConsole)
      debugBox.addWidget(self.consoleCheck)
      #endregion

      self.box.addLayout(debugBox)
      #endregion

      self.box.setSpacing(5)
      self.setLayout(self.box)
      #endregion
   #endregion

   #region Methods
   @Slot()
   def selectDatasheetDir(self):
      if self.fileDialog.exec():
         selected = self.fileDialog.selectedFiles()[0]
         if Path.isdir(selected):
            self.settings.datasheetsDir = selected
            self.datasheetsDirText.setText(self.settings.datasheetsDir)

   def getSettings(self):
      return self.settings

   def show(self, currentSettings: Settings):
      self.settings = currentSettings
      self.exec()

   #region Update
   @Slot(str)
   def updateDatasheetDir(self, text: str):
      self.settings.datasheetsDir = text

   @Slot(str)
   def updateMetadata(self, text: str):
      self.settings.metadataPath = text

   @Slot(str)
   def updateDocViewer(self, text: str):
      self.settings.docViewer = text

   @Slot(bool)
   def updateVerbose(self, state: bool):
      self.settings.verbose = state

   @Slot(str)
   def updateConsole(self, state: bool):
      self.settings.console = state
   #endregion
   #endregion
