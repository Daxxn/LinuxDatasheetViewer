import os.path as Path
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QDialog, QFileDialog, QHBoxLayout, QLineEdit, QPushButton
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
      self.openFolderButton = QPushButton(QIcon(), 'Open Folder')
      self.openFolderButton.clicked.connect(self.selectDatasheetDir)
      self.fileDialog = QFileDialog(self, 'Select Datasheet Folder', self.settings.datasheetsDir if self.settings.datasheetsDir != '' else '~/Documents/')
      self.fileDialog.setFileMode(QFileDialog.FileMode.Directory)
      self.datasheetsDirText = QLineEdit(self.settings.datasheetsDir)

      self.box = QBoxLayout(QBoxLayout.TopToBottom)
      self.datasheetsDirLayout = QHBoxLayout()
      self.datasheetsDirLayout.addWidget(self.datasheetsDirText)
      self.datasheetsDirLayout.addWidget(self.openFolderButton)

      self.box.addLayout(self.datasheetsDirLayout)
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
      # self.settings.datasheetsDir = args

   def getSettings(self):
      return self.settings

   def show(self, currentSettings: Settings):
      self.settings = currentSettings
      self.exec()
   #endregion
